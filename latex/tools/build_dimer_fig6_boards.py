#!/usr/bin/env python3
"""Build combined dimer Figure-6 full-panel SVG boards from rerun folders.

This script scans a source directory for files named:
- time_all_signals_real_imag_abs_dimer_fig6_TXXX_paper_eqs.svg
- freq_all_signals_real_imag_abs_dimer_fig6_TXXX_paper_eqs.svg

It then builds two vertically stacked boards that keep the full source figures:
1) one time-domain board
2) one frequency-domain board
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
DEFAULT_SOURCE_ROOT = Path(
    "C:/Users/leopo/.vscode/thesis_python/jobs/dimer/150426_use_those_in_thesis/n_inh_1000"
)

TIME_RE = re.compile(r"^time_all_signals_real_imag_abs_dimer_fig6_T(?P<t>\d{3})_paper_eqs\.svg$")
FREQ_RE = re.compile(r"^freq_all_signals_real_imag_abs_dimer_fig6_T(?P<t>\d{3})_paper_eqs\.svg$")

NUMBER_RE = re.compile(r"[-+]?\d*\.?\d+")
URL_RE = re.compile(r"url\(#([^)]+)\)")

MARGIN_X = 30.0
MARGIN_Y = 24.0
ROW_GAP = 28.0
TEXT_GAP = 10.0
PANEL_WIDTH = 980.0

FONT_FAMILY = "Arial, Helvetica, sans-serif"
TEXT_COLOR = "#222"
ROW_FONT = 20.0


@dataclass(frozen=True)
class PanelPair:
    token: str
    wait_fs: int
    time_svg: Path
    freq_svg: Path


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


def create_text(parent: ET.Element, x: float, y: float, text: str, font_size: float) -> None:
    text_elem = ET.SubElement(
        parent,
        "text",
        {
            "x": f"{x:.3f}",
            "y": f"{y:.3f}",
            "font-family": FONT_FAMILY,
            "font-size": f"{font_size:.3f}",
            "fill": TEXT_COLOR,
            "text-anchor": "middle",
            f"{{{XML_NS}}}space": "preserve",
        },
    )
    text_elem.text = text


def discover_panel_pairs(source_root: Path) -> list[PanelPair]:
    grouped: dict[str, dict[str, Path]] = {}

    for svg_path in source_root.rglob("*.svg"):
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


def build_domain_board(
    pairs: list[PanelPair],
    domain: str,
    output_path: Path,
) -> None:
    if domain not in {"time", "freq"}:
        raise ValueError(f"Unsupported domain: {domain}")
    if not pairs:
        raise ValueError("No panel pairs were discovered")

    svg_paths = [pair.time_svg if domain == "time" else pair.freq_svg for pair in pairs]
    sizes = [parse_svg_size(ET.parse(svg_path).getroot()) for svg_path in svg_paths]

    row_heights = [(height * PANEL_WIDTH / width) for width, height in sizes]
    canvas_width = MARGIN_X * 2 + PANEL_WIDTH
    center_x = canvas_width / 2.0

    svg_root = ET.Element("svg", {"version": "1.1"})
    cursor_y = MARGIN_Y

    for row_index, pair in enumerate(pairs):
        cursor_y += ROW_FONT
        create_text(svg_root, center_x, cursor_y, f"T = {pair.wait_fs} fs", ROW_FONT)
        cursor_y += line_height(ROW_FONT) - ROW_FONT + TEXT_GAP

        svg_path = pair.time_svg if domain == "time" else pair.freq_svg
        source_root = copy.deepcopy(ET.parse(svg_path).getroot())
        prefix_tree_ids(source_root, f"{output_path.stem}_r{row_index + 1}")

        width, height = sizes[row_index]
        scale = PANEL_WIDTH / width
        dest_x = MARGIN_X
        dest_y = cursor_y

        panel_group = ET.SubElement(
            svg_root,
            "g",
            {
                "transform": f"translate({dest_x:.3f}, {dest_y:.3f}) scale({scale:.9f})"
            },
        )
        for child in filtered_root_children(source_root):
            panel_group.append(child)

        cursor_y += row_heights[row_index]
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
        help="Source root with Figure-6 rerun subfolders",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEST_ROOT,
        help="Destination folder for generated SVG boards",
    )
    parser.add_argument(
        "--prefix",
        default="results_dimer_fig6_paper_eqs_homogeneous",
        help="Output filename prefix",
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
        raise RuntimeError("No matching Figure-6 time/freq SVG pairs were found")

    outputs = {
        "time": dest_root / f"{args.prefix}_time_all_components.svg",
        "freq": dest_root / f"{args.prefix}_freq_all_components.svg",
    }
    for domain, output_path in outputs.items():
        build_domain_board(pairs=pairs, domain=domain, output_path=output_path)
        print(f"Built: {output_path}")


if __name__ == "__main__":
    main()
