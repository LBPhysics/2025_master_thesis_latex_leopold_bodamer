#!/usr/bin/env python3
"""Build combined dimer Figure-4 SVG boards from rerun folders.

This script scans a source directory for files named:
- time_all_signals_real_imag_abs_dimer_fig4_TXXX_paper_eqs.svg
- freq_all_signals_real_imag_abs_dimer_fig4_TXXX_paper_eqs.svg

It then builds:
1) One all-components waiting-time board (time vs freq columns).
2) Three component-only waiting-time boards by clipping each source SVG to
    the corresponding subplot row (rephasing/nonrephasing/absorptive).
"""

from __future__ import annotations

import argparse
import copy
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEST_ROOT = REPO_ROOT / "latex" / "figures" / "svgs"
DEFAULT_SOURCE_ROOT = Path("C:/Users/leopo/.vscode/thesis_python/jobs/dimer/new_runs_eom_fixed")

TIME_RE = re.compile(r"^time_all_signals_real_imag_abs_dimer_fig4_T(?P<t>\d{3})_paper_eqs\.svg$")
FREQ_RE = re.compile(r"^freq_all_signals_real_imag_abs_dimer_fig4_T(?P<t>\d{3})_paper_eqs\.svg$")

NUMBER_RE = re.compile(r"[-+]?\d*\.?\d+")
URL_RE = re.compile(r"url\(#([^)]+)\)")

MARGIN_X = 28.0
MARGIN_Y = 24.0
COL_GAP = 24.0
ROW_GAP = 30.0
TEXT_GAP = 10.0
TOP_BLOCK_GAP = 12.0
PANEL_WIDTH = 620.0

FONT_FAMILY = "Arial, Helvetica, sans-serif"
TEXT_COLOR = "#222"
TOP_FONT = 22.0
COLUMN_FONT = 20.0
ROW_FONT = 18.0


@dataclass(frozen=True)
class PanelPair:
    token: str
    wait_fs: int
    time_svg: Path
    freq_svg: Path


@dataclass(frozen=True)
class CropSpec:
    label: str
    row_index: int | None


CROP_ALL = CropSpec(label="all", row_index=None)
CROP_REPHASING = CropSpec(label="rephasing", row_index=0)
CROP_NONREPHASING = CropSpec(label="nonrephasing", row_index=1)
CROP_ABSORPTIVE = CropSpec(label="absorptive", row_index=2)


@dataclass(frozen=True)
class SvgLayout:
    width: float
    height: float
    row_bands: tuple[tuple[float, float], ...]
    content_x_bounds: tuple[float, float] | None


def local_name(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def parse_length(value: str | None) -> float | None:
    if not value:
        return None
    match = NUMBER_RE.search(value)
    return float(match.group(0)) if match else None


def parse_svg_size(root: ET.Element) -> tuple[float, float]:
    width = parse_length(root.get("width"))
    height = parse_length(root.get("height"))
    if width and height:
        return width, height

    view_box = root.get("viewBox")
    if view_box:
        parts = view_box.replace(",", " ").split()
        if len(parts) == 4:
            return float(parts[2]), float(parts[3])

    raise ValueError("Could not determine SVG size")


def parse_patch_bounds(path_d: str) -> tuple[float, float, float, float] | None:
    values = [float(value) for value in NUMBER_RE.findall(path_d)]
    if len(values) < 8:
        return None

    x_values = values[0::2]
    y_values = values[1::2]
    return min(x_values), min(y_values), max(x_values), max(y_values)


def extract_plot_bands(root: ET.Element) -> tuple[tuple[tuple[float, float], ...], tuple[float, float] | None]:
    patches: list[tuple[float, float, float, float, float]] = []

    for axes_group in root.iter():
        if local_name(axes_group.tag) != "g":
            continue
        group_id = axes_group.get("id", "")
        if not group_id.startswith("axes_"):
            continue

        patch_path: ET.Element | None = None
        for child in axes_group:
            if local_name(child.tag) != "g":
                continue
            child_id = child.get("id", "")
            if not child_id.startswith("patch_"):
                continue
            for maybe_path in child:
                if local_name(maybe_path.tag) == "path":
                    patch_path = maybe_path
                    break
            if patch_path is not None:
                break

        if patch_path is None:
            continue

        bounds = parse_patch_bounds(patch_path.get("d", ""))
        if bounds is None:
            continue
        x_min, y_min, x_max, y_max = bounds
        patches.append((x_max - x_min, x_min, x_max, y_min, y_max))

    if not patches:
        return (), None

    max_patch_width = max(width for width, _, _, _, _ in patches)
    # Colorbar axes are much narrower than plot panels. Keep only wide plot axes.
    wide_patches = [
        (x_min, x_max, y_min, y_max)
        for width, x_min, x_max, y_min, y_max in patches
        if width >= 0.8 * max_patch_width
    ]

    if not wide_patches:
        return (), None

    unique_bands = sorted(
        {(round(y0, 3), round(y1, 3)) for _, _, y0, y1 in wide_patches},
        key=lambda item: item[0],
    )

    x_min = min(item[0] for item in wide_patches)
    x_max = max(item[1] for item in wide_patches)
    return (
        tuple((float(y0), float(y1)) for y0, y1 in unique_bands),
        (float(x_min), float(x_max)),
    )


def analyse_svg_layout(svg_path: Path) -> SvgLayout:
    root = ET.parse(svg_path).getroot()
    width, height = parse_svg_size(root)
    row_bands, content_x_bounds = extract_plot_bands(root)
    return SvgLayout(width=width, height=height, row_bands=row_bands, content_x_bounds=content_x_bounds)


def resolve_crop_bounds(layout: SvgLayout, crop: CropSpec) -> tuple[float, float] | None:
    if crop.row_index is None:
        return 0.0, layout.height

    if crop.row_index < len(layout.row_bands):
        return layout.row_bands[crop.row_index]

    return None


def resolve_crop_x_bounds(layout: SvgLayout, crop: CropSpec) -> tuple[float, float]:
    # Keep the all-components board visually unchanged.
    if crop.label == "all" or layout.content_x_bounds is None:
        return 0.0, layout.width
    return layout.content_x_bounds


def replace_url_refs(text: str, id_map: dict[str, str]) -> str:
    return URL_RE.sub(lambda m: f"url(#{id_map.get(m.group(1), m.group(1))})", text)


def prefix_tree_ids(root: ET.Element, prefix: str) -> None:
    id_map: dict[str, str] = {}
    for elem in root.iter():
        old_id = elem.get("id")
        if old_id:
            new_id = f"{prefix}_{old_id}"
            id_map[old_id] = new_id
            elem.set("id", new_id)

    if not id_map:
        return

    href_attrs = {f"{{{XLINK_NS}}}href", "href"}
    for elem in root.iter():
        for attr, value in list(elem.attrib.items()):
            if not value:
                continue
            if attr in href_attrs and value.startswith("#"):
                ref_id = value[1:]
                if ref_id in id_map:
                    elem.set(attr, f"#{id_map[ref_id]}")
                continue
            updated = replace_url_refs(value, id_map)
            if updated != value:
                elem.set(attr, updated)


def filtered_root_children(root: ET.Element) -> list[ET.Element]:
    children: list[ET.Element] = []
    for child in root:
        if local_name(child.tag) in {"namedview", "metadata"}:
            continue
        children.append(child)
    return children


def line_height(font_size: float) -> float:
    return font_size * 1.25


def create_text(parent: ET.Element, x: float, y: float, text: str, font_size: float, anchor: str = "middle") -> None:
    text_elem = ET.SubElement(
        parent,
        "text",
        {
            "x": f"{x:.3f}",
            "y": f"{y:.3f}",
            "font-family": FONT_FAMILY,
            "font-size": f"{font_size:.3f}",
            "fill": TEXT_COLOR,
            "text-anchor": anchor,
            f"{{{XML_NS}}}space": "preserve",
        },
    )
    text_elem.text = text


def discover_panel_pairs(source_root: Path) -> list[PanelPair]:
    grouped: dict[str, dict[str, Path]] = {}

    for svg_path in source_root.rglob("*.svg"):
        # Only use direct run folders: <run_name>/figures/<file>.svg
        # This skips nested archives that can contain duplicate T tokens.
        rel_parts = svg_path.relative_to(source_root).parts
        if len(rel_parts) != 3 or rel_parts[1] != "figures":
            continue

        name = svg_path.name
        time_match = TIME_RE.match(name)
        freq_match = FREQ_RE.match(name)
        if not time_match and not freq_match:
            continue

        token = (time_match or freq_match).group("t")
        bucket = grouped.setdefault(token, {})
        key = "time" if time_match else "freq"

        if key in bucket:
            raise ValueError(
                f"Duplicate {key} SVG for T{token}:\n"
                f"  first: {bucket[key]}\n"
                f"  second: {svg_path}"
            )
        bucket[key] = svg_path

    missing = [
        token
        for token, bucket in grouped.items()
        if "time" not in bucket or "freq" not in bucket
    ]
    if missing:
        missing_sorted = ", ".join(sorted(missing, key=int))
        raise ValueError(f"Missing time/freq partner SVGs for T tokens: {missing_sorted}")

    pairs = [
        PanelPair(
            token=token,
            wait_fs=int(token),
            time_svg=bucket["time"],
            freq_svg=bucket["freq"],
        )
        for token, bucket in grouped.items()
    ]
    return sorted(pairs, key=lambda pair: pair.wait_fs)


def build_board(
    pairs: list[PanelPair],
    output_path: Path,
    title: str,
    crop: CropSpec,
) -> None:
    if not pairs:
        raise ValueError("No panel pairs were discovered")

    size_cache: dict[Path, SvgLayout] = {}
    for pair in pairs:
        for svg_path in (pair.time_svg, pair.freq_svg):
            size_cache[svg_path] = analyse_svg_layout(svg_path)

    col_labels = ("Time domain", "Frequency domain")

    def pair_svg(pair: PanelPair, col_index: int) -> Path:
        return pair.time_svg if col_index == 0 else pair.freq_svg

    if crop.label == "all":
        active_cols = [0, 1]
    else:
        active_cols = []
        for col_index in (0, 1):
            has_data = any(
                resolve_crop_bounds(size_cache[pair_svg(pair, col_index)], crop) is not None
                for pair in pairs
            )
            if has_data:
                active_cols.append(col_index)

    if not active_cols:
        raise RuntimeError(f"No matching plot rows were found for crop '{crop.label}'")

    row_heights: list[float] = []
    for pair in pairs:
        scaled = []
        for col_index in active_cols:
            svg_path = pair_svg(pair, col_index)
            layout = size_cache[svg_path]
            bounds = resolve_crop_bounds(layout, crop)
            if bounds is None:
                continue

            crop_x0, crop_x1 = resolve_crop_x_bounds(layout, crop)
            crop_w = crop_x1 - crop_x0
            if crop_w <= 0:
                continue

            cropped_height = bounds[1] - bounds[0]
            scaled.append(cropped_height * PANEL_WIDTH / crop_w)

        if not scaled:
            raise RuntimeError(f"No source row data available for T={pair.wait_fs} fs and crop '{crop.label}'")
        row_heights.append(max(scaled))

    canvas_width = MARGIN_X * 2 + PANEL_WIDTH * len(active_cols) + COL_GAP * (len(active_cols) - 1)
    center_x = canvas_width / 2.0
    col_centers = [
        MARGIN_X + display_col * (PANEL_WIDTH + COL_GAP) + PANEL_WIDTH / 2.0
        for display_col in range(len(active_cols))
    ]

    svg_root = ET.Element("svg", {"version": "1.1"})
    defs = ET.SubElement(svg_root, "defs")

    cursor_y = MARGIN_Y

    cursor_y += TOP_FONT
    create_text(svg_root, center_x, cursor_y, title, TOP_FONT)
    cursor_y += line_height(TOP_FONT) - TOP_FONT + TOP_BLOCK_GAP

    cursor_y += COLUMN_FONT
    for display_col, col_index in enumerate(active_cols):
        create_text(svg_root, col_centers[display_col], cursor_y, col_labels[col_index], COLUMN_FONT)
    cursor_y += line_height(COLUMN_FONT) - COLUMN_FONT + TOP_BLOCK_GAP

    for row_index, pair in enumerate(pairs):
        cursor_y += ROW_FONT
        create_text(svg_root, center_x, cursor_y, f"T = {pair.wait_fs} fs", ROW_FONT)
        cursor_y += line_height(ROW_FONT) - ROW_FONT + TEXT_GAP

        row_top = cursor_y
        row_height = row_heights[row_index]

        for display_col, col_index in enumerate(active_cols):
            svg_path = pair_svg(pair, col_index)
            source_root = copy.deepcopy(ET.parse(svg_path).getroot())
            prefix_tree_ids(source_root, f"{output_path.stem}_r{row_index + 1}c{display_col + 1}")

            layout = size_cache[svg_path]
            bounds = resolve_crop_bounds(layout, crop)
            if bounds is None:
                continue

            crop_x, crop_x_end = resolve_crop_x_bounds(layout, crop)
            crop_w = crop_x_end - crop_x
            if crop_w <= 0:
                continue

            crop_y, crop_y_end = bounds
            crop_h = crop_y_end - crop_y

            scale = PANEL_WIDTH / crop_w
            scaled_h = crop_h * scale

            y_offset = (row_height - scaled_h) / 2.0
            dest_x = MARGIN_X + display_col * (PANEL_WIDTH + COL_GAP)
            dest_y = row_top + y_offset

            group_attrs = {
                "transform": (
                    f"translate({dest_x - crop_x * scale:.3f}, {dest_y - crop_y * scale:.3f}) "
                    f"scale({scale:.9f})"
                )
            }

            if crop.label != "all":
                clip_id = f"clip_{output_path.stem}_{row_index + 1}_{display_col + 1}"
                clip_path = ET.SubElement(defs, "clipPath", {"id": clip_id})
                ET.SubElement(
                    clip_path,
                    "rect",
                    {
                        "x": f"{dest_x:.3f}",
                        "y": f"{dest_y:.3f}",
                        "width": f"{PANEL_WIDTH:.3f}",
                        "height": f"{scaled_h:.3f}",
                    },
                )
                group_attrs["clip-path"] = f"url(#{clip_id})"

            panel_group = ET.SubElement(svg_root, "g", group_attrs)
            for child in filtered_root_children(source_root):
                panel_group.append(child)

        cursor_y += row_height
        if row_index != len(pairs) - 1:
            cursor_y += ROW_GAP

    canvas_height = cursor_y + MARGIN_Y
    svg_root.set("width", f"{canvas_width:.3f}")
    svg_root.set("height", f"{canvas_height:.3f}")
    svg_root.set("viewBox", f"0 0 {canvas_width:.3f} {canvas_height:.3f}")

    background = ET.Element(
        "rect",
        {
            "x": "0",
            "y": "0",
            "width": f"{canvas_width:.3f}",
            "height": f"{canvas_height:.3f}",
            "fill": "#ffffff",
        },
    )
    svg_root.insert(0, background)

    tree = ET.ElementTree(svg_root)
    ET.indent(tree, space="  ")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE_ROOT,
        help="Source root with Figure-4 rerun subfolders",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEST_ROOT,
        help="Destination folder for generated SVG boards",
    )
    parser.add_argument(
        "--prefix",
        default="rslts_dimer_fig4_paper_eqs_waiting_time",
        help="Output filename prefix",
    )
    parser.add_argument(
        "--only-all",
        action="store_true",
        help="Build only the all-components board",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_root = args.source.resolve()
    dest_root = args.dest.resolve()

    if not source_root.exists():
        raise FileNotFoundError(f"Source directory not found: {source_root}")

    pairs = discover_panel_pairs(source_root)
    if not pairs:
        raise RuntimeError("No matching Figure-4 time/freq SVG pairs were found")

    all_output = dest_root / f"{args.prefix}_all_components.svg"
    build_board(
        pairs=pairs,
        output_path=all_output,
        title="Dimer Figure 4 paper_eqs waiting-time board (all components)",
        crop=CROP_ALL,
    )
    print(f"Built: {all_output}")

    if args.only_all:
        return

    # If the all-components board exists, also build component-only boards.
    if all_output.exists():
        variants = [
            (CROP_REPHASING, "rephasing"),
            (CROP_NONREPHASING, "nonrephasing"),
            (CROP_ABSORPTIVE, "absorptive"),
        ]
        for crop_spec, suffix in variants:
            output = dest_root / f"{args.prefix}_{suffix}.svg"
            build_board(
                pairs=pairs,
                output_path=output,
                title=f"Dimer Figure 4 paper_eqs waiting-time board ({suffix})",
                crop=crop_spec,
            )
            print(f"Built: {output}")


if __name__ == "__main__":
    main()
