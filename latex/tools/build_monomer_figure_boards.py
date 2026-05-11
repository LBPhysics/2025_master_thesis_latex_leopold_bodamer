#!/usr/bin/env python3
"""Build combined monomer figure boards as editable SVGs and matching PDFs."""

from __future__ import annotations

import argparse
import copy
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

REPO_ROOT = Path(__file__).resolve().parents[2]
SVG_ROOT = REPO_ROOT / "latex" / "figures" / "svgs"
PDF_ROOT = REPO_ROOT / "latex" / "figures"

MARGIN_X = 36.0
MARGIN_Y = 32.0
COL_GAP = 28.0
ROW_GAP = 34.0
TEXT_GAP = 10.0
TOP_BLOCK_GAP = 14.0
BOTTOM_BLOCK_GAP = 14.0
FONT_FAMILY = "Arial, Helvetica, sans-serif"
TEXT_COLOR = "#222"
TOP_FONT = 24.0
COLUMN_FONT = 22.0
ROW_FONT = 20.0
PANEL_FONT = 18.0
BOTTOM_FONT = 18.0

NUMBER_RE = re.compile(r"[-+]?\d*\.?\d+")
URL_RE = re.compile(r"url\(#([^)]+)\)")
MARKUP_RE = re.compile(r"(<sub>.*?</sub>|<sup>.*?</sup>)")


@dataclass(frozen=True)
class FigureSpec:
    basename: str
    panels: tuple[tuple[str, str], ...]
    top_lines: tuple[str, ...] = ()
    column_headers: tuple[str, str] = ()
    row_headers: tuple[str | None, ...] = ()
    panel_headers: tuple[tuple[str | None, str | None], ...] = ()
    bottom_lines: tuple[str, ...] = ()
    extra_side_padding: float = 0.0


FIGURE_SPECS: tuple[FigureSpec, ...] = (
    FigureSpec(
        basename="rslts_monomer_1d_time_hom_inhom",
        panels=(
            (
                "monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/time_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad.svg",
                "monomer_essential_results/08_201210_monomer_fig2_inhomogeneous_lindblad_n10000/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10000.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="rslts_monomer_1d_freq_hom_inhom",
        panels=(
            (
                "monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/freq_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad.svg",
                "monomer_essential_results/08_201210_monomer_fig2_inhomogeneous_lindblad_n10000/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10000.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="rslts_monomer_2d_time_hom_inhom",
        panels=(
            (
                "monomer_essential_results/07_172218_monomer_fig3_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T000_lindblad.svg",
                "monomer_essential_results/07_172248_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad.svg",
            ),
            (
                "monomer_essential_results/07_172229_monomer_fig3_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T020_lindblad.svg",
                "monomer_essential_results/07_172302_monomer_fig4_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T020_lindblad.svg",
            ),
            (
                "monomer_essential_results/07_172238_monomer_fig3_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T040_lindblad.svg",
                "monomer_essential_results/07_172315_monomer_fig4_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T040_lindblad.svg",
            ),
        ),
        column_headers=(
            "Homogeneous, Delta<sub>inh</sub> = 0",
            "Inhomogeneous, Delta<sub>inh</sub> = 200 cm<sup>-1</sup>",
        ),
        row_headers=("T = 0 fs", "T = 20 fs", "T = 40 fs"),
    ),
    FigureSpec(
        basename="rslts_monomer_2d_freq_hom_inhom",
        panels=(
            (
                "monomer_essential_results/07_172218_monomer_fig3_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T000_lindblad_02.svg",
                "monomer_essential_results/07_172248_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T000_lindblad_02.svg",
            ),
            (
                "monomer_essential_results/07_172229_monomer_fig3_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T020_lindblad_02.svg",
                "monomer_essential_results/07_172302_monomer_fig4_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T020_lindblad_02.svg",
            ),
            (
                "monomer_essential_results/07_172238_monomer_fig3_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T040_lindblad_04.svg",
                "monomer_essential_results/07_172315_monomer_fig4_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T040_lindblad_02.svg",
            ),
        ),
        column_headers=(
            "Homogeneous, Delta<sub>inh</sub> = 0",
            "Inhomogeneous, Delta<sub>inh</sub> = 200 cm<sup>-1</sup>",
        ),
        row_headers=("T = 0 fs", "T = 20 fs", "T = 40 fs"),
        extra_side_padding=50.0,
    ),
    FigureSpec(
        basename="rslts_monomer_redfield_examples",
        panels=(
            (
                "monomer_essential_results/08_114410_monomer_fig2_homogeneous_redfield_no_rwa_thermal/time_all_signals_real_imag_abs_monomer_fig2_homogeneous_redfield_no_rwa_thermal.svg",
                "monomer_essential_results/08_114410_monomer_fig2_homogeneous_redfield_no_rwa_thermal/freq_all_signals_real_imag_abs_monomer_fig2_homogeneous_redfield_no_rwa_thermal.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="app_monomer_fig2_hom_lindblad",
        panels=(
            (
                "monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/time_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad.svg",
                "monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/freq_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="app_paper_eqs_monomer_fig2_time",
        panels=(
            (
                "monomer_essential_results/07_172159_monomer_fig2_inhomogeneous_lindblad_n10/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10.svg",
                "monomer_essential_results/07_172209_monomer_fig2_inhomogeneous_lindblad_n100/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n100.svg",
            ),
            (
                "monomer_essential_results/07_165352_monomer_fig2_inhomogeneous_lindblad_n1000/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n1000.svg",
                "monomer_essential_results/08_201210_monomer_fig2_inhomogeneous_lindblad_n10000/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10000.svg",
            ),
        ),
        panel_headers=(
            ("N<sub>inhom</sub> = 10", "N<sub>inhom</sub> = 100"),
            ("N<sub>inhom</sub> = 1000", "N<sub>inhom</sub> = 10000"),
        ),
    ),
    FigureSpec(
        basename="app_paper_eqs_monomer_fig2_freq",
        panels=(
            (
                "monomer_essential_results/07_172159_monomer_fig2_inhomogeneous_lindblad_n10/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10.svg",
                "monomer_essential_results/07_172209_monomer_fig2_inhomogeneous_lindblad_n100/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n100.svg",
            ),
            (
                "monomer_essential_results/07_165352_monomer_fig2_inhomogeneous_lindblad_n1000/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n1000.svg",
                "monomer_essential_results/08_201210_monomer_fig2_inhomogeneous_lindblad_n10000/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10000.svg",
            ),
        ),
        panel_headers=(
            ("N<sub>inhom</sub> = 10", "N<sub>inhom</sub> = 100"),
            ("N<sub>inhom</sub> = 1000", "N<sub>inhom</sub> = 10000"),
        ),
    ),
    FigureSpec(
        basename="app_monomer_legacy_fig4_t0_time",
        panels=(
            (
                "monomer_essential_results/01_181835_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad.svg",
                "monomer_essential_results/01_184018_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad.svg",
            ),
        ),
        top_lines=(
            "Supplementary higher-field Lindblad panels at T = 0 fs, amplitudes (0.005, 0.005, 0.005), time domain",
        ),
        bottom_lines=(
            "Panels shown for N<sub>inhom</sub> = 10 (left) and 100 (right)",
        ),
    ),
    FigureSpec(
        basename="app_monomer_legacy_fig4_t0_freq",
        panels=(
            (
                "monomer_essential_results/01_181835_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_monomer_fig4_T000_lindblad.svg",
                "monomer_essential_results/01_184018_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_monomer_fig4_T000_lindblad.svg",
            ),
        ),
        top_lines=(
            "Supplementary higher-field Lindblad panels at T = 0 fs, amplitudes (0.005, 0.005, 0.005), frequency domain",
        ),
        bottom_lines=(
            "Panels shown for N<sub>inhom</sub> = 10 (left) and 100 (right)",
        ),
    ),
    FigureSpec(
        basename="app_monomer_legacy_fig4_t20",
        panels=(
            (
                "monomer_essential_results/01_184037_monomer_fig4_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T020_lindblad.svg",
                "monomer_essential_results/01_184037_monomer_fig4_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T020_lindblad_02.svg",
            ),
        ),
        top_lines=(
            "Supplementary higher-field Lindblad panels at T = 20 fs, N<sub>inhom</sub> = 100, amplitudes (0.005, 0.005, 0.005)",
        ),
    ),
    FigureSpec(
        basename="app_monomer_legacy_fig4_t40_lindblad",
        panels=(
            (
                "monomer_essential_results/01_184055_monomer_fig4_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T040_lindblad.svg",
                "monomer_essential_results/01_184055_monomer_fig4_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T040_lindblad_02.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="app_monomer_legacy_redfield",
        panels=(
            (
                "monomer_essential_results/03_175155_monomer_fig4_T000_redfield_no_rwa_thermal/time_all_signals_real_imag_abs_monomer_fig4_T000_redfield_no_rwa_thermal_01.svg",
                "monomer_essential_results/03_175155_monomer_fig4_T000_redfield_no_rwa_thermal/freq_all_signals_real_imag_abs_monomer_fig4_T000_redfield_no_rwa_thermal_02.svg",
            ),
        ),
    ),
    FigureSpec(
        basename="rslts_dimer_2d_time_un_coupled",
        panels=(
            (
                "dimer_essential_results/19_222916_dimer_fig3a_uncoupled_paper_eqs/figures/time_all_signals_real_imag_abs_dimer_fig3a_uncoupled_paper_eqs.svg",
                "dimer_essential_results/17_121018_dimer_fig3b_coupled_paper_eqs/figures/time_all_signals_real_imag_abs_dimer_fig3b_coupled_paper_eqs.svg",
            ),
        ),
        top_lines=(
            "Dimer fig3 paper_eqs time-domain board (T = 0 fs)",
        ),
        column_headers=(
            "Uncoupled (fig3a)",
            "Coupled (fig3b)",
        ),
        bottom_lines=(
            "Source folder (left): dimer_essential_results/19_222916_dimer_fig3a_uncoupled_paper_eqs",
            "Source folder (right): dimer_essential_results/17_121018_dimer_fig3b_coupled_paper_eqs",
        ),
    ),
    FigureSpec(
        basename="rslts_dimer_2d_freq_un_coupled",
        panels=(
            (
                "dimer_essential_results/19_222916_dimer_fig3a_uncoupled_paper_eqs/figures/freq_all_signals_real_imag_abs_dimer_fig3a_uncoupled_paper_eqs.svg",
                "dimer_essential_results/17_121018_dimer_fig3b_coupled_paper_eqs/figures/freq_all_signals_real_imag_abs_dimer_fig3b_coupled_paper_eqs.svg",
            ),
        ),
        top_lines=(
            "Dimer fig3 paper_eqs frequency-domain board (T = 0 fs)",
        ),
        column_headers=(
            "Uncoupled (fig3a)",
            "Coupled (fig3b)",
        ),
        bottom_lines=(
            "Source folder (left): dimer_essential_results/19_222916_dimer_fig3a_uncoupled_paper_eqs",
            "Source folder (right): dimer_essential_results/17_121018_dimer_fig3b_coupled_paper_eqs",
        ),
    ),
    FigureSpec(
        basename="rslts_extension_ring_time_overview",
        panels=(
            (
                "extension_results/17_224701_trimer_ring_single/figures/time_all_signals_real_imag_abs_trimer_ring_single.svg",
                "extension_results/17_224610_trimer_ring_double/figures/time_all_signals_real_imag_abs_trimer_ring_double.svg",
            ),
            (
                "extension_results/17_230632_pentamer_ring_single/figures/time_all_signals_real_imag_abs_pentamer_ring_single.svg",
                "extension_results/19_225943_tridecamer_ring_single/figures/time_all_signals_real_imag_abs_tridecamer_ring_single.svg",
            ),
        ),
        top_lines=(
            "N-site extension preview: ring-aggregate time-domain panels (T = 0 fs)",
        ),
        panel_headers=(
            ("Trimer single ring (N = 3)", "Trimer double ring (N = 6)"),
            ("Pentamer single ring (N = 5)", "Tridecamer single ring (N = 13)"),
        ),
        bottom_lines=(
            "Sources: extension_results/17_224701_trimer_ring_single and extension_results/17_224610_trimer_ring_double",
            "Sources: extension_results/17_230632_pentamer_ring_single and extension_results/19_225943_tridecamer_ring_single",
        ),
    ),
    FigureSpec(
        basename="rslts_extension_ring_freq_overview",
        panels=(
            (
                "extension_results/17_224701_trimer_ring_single/figures/freq_all_signals_real_imag_abs_trimer_ring_single.svg",
                "extension_results/17_224610_trimer_ring_double/figures/freq_all_signals_real_imag_abs_trimer_ring_double.svg",
            ),
            (
                "extension_results/17_230632_pentamer_ring_single/figures/freq_all_signals_real_imag_abs_pentamer_ring_single.svg",
                "extension_results/19_225943_tridecamer_ring_single/figures/freq_all_signals_real_imag_abs_tridecamer_ring_single.svg",
            ),
        ),
        top_lines=(
            "N-site extension preview: ring-aggregate frequency-domain panels (T = 0 fs)",
        ),
        panel_headers=(
            ("Trimer single ring (N = 3)", "Trimer double ring (N = 6)"),
            ("Pentamer single ring (N = 5)", "Tridecamer single ring (N = 13)"),
        ),
        bottom_lines=(
            "Sources: extension_results/17_224701_trimer_ring_single and extension_results/17_224610_trimer_ring_double",
            "Sources: extension_results/17_230632_pentamer_ring_single and extension_results/19_225943_tridecamer_ring_single",
        ),
    ),
)


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


def line_height(font_size: float) -> float:
    return font_size * 1.25


def replace_url_refs(text: str, id_map: dict[str, str]) -> str:
    return URL_RE.sub(lambda match: f"url(#{id_map.get(match.group(1), match.group(1))})", text)


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


def create_text(parent: ET.Element, x: float, y: float, text: str, font_size: float, anchor: str) -> None:
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

    parts = MARKUP_RE.split(text)
    first = True
    for part in parts:
        if not part:
            continue
        if part.startswith("<sub>") and part.endswith("</sub>"):
            tspan = ET.SubElement(
                text_elem,
                "tspan",
                {
                    "baseline-shift": "sub",
                    "font-size": f"{font_size * 0.72:.3f}",
                },
            )
            tspan.text = part[5:-6]
        elif part.startswith("<sup>") and part.endswith("</sup>"):
            tspan = ET.SubElement(
                text_elem,
                "tspan",
                {
                    "baseline-shift": "super",
                    "font-size": f"{font_size * 0.72:.3f}",
                },
            )
            tspan.text = part[5:-6]
        else:
            if first:
                text_elem.text = part
                first = False
            else:
                tspan = ET.SubElement(text_elem, "tspan")
                tspan.text = part


def resolve_panel_path(relative_path: str) -> Path:
    path = SVG_ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def compute_panel_sizes(spec: FigureSpec) -> dict[str, tuple[float, float]]:
    sizes: dict[str, tuple[float, float]] = {}
    for row in spec.panels:
        for panel in row:
            path = resolve_panel_path(panel)
            sizes[panel] = parse_svg_size(ET.parse(path).getroot())
    return sizes


def validate_spec(spec: FigureSpec) -> None:
    if any(len(row) != 2 for row in spec.panels):
        raise ValueError(f"{spec.basename}: every row must contain exactly two panels")
    if spec.column_headers and len(spec.column_headers) != 2:
        raise ValueError(f"{spec.basename}: column_headers must contain exactly two entries")
    if spec.row_headers and len(spec.row_headers) != len(spec.panels):
        raise ValueError(f"{spec.basename}: row_headers length mismatch")
    if spec.panel_headers and len(spec.panel_headers) != len(spec.panels):
        raise ValueError(f"{spec.basename}: panel_headers row count mismatch")
    for row in spec.panel_headers:
        if len(row) != 2:
            raise ValueError(f"{spec.basename}: every panel_headers row must contain exactly two entries")


def build_svg(spec: FigureSpec) -> Path:
    validate_spec(spec)
    sizes = compute_panel_sizes(spec)
    panel_width = max(width for width, _height in sizes.values())
    row_heights: list[float] = []
    for row in spec.panels:
        scaled_heights = []
        for panel in row:
            src_width, src_height = sizes[panel]
            scaled_heights.append(src_height * panel_width / src_width)
        row_heights.append(max(scaled_heights))

    canvas_width = MARGIN_X * 2 + panel_width * 2 + COL_GAP + spec.extra_side_padding * 2.0
    canvas_center_x = canvas_width / 2.0
    col_centers = (
        MARGIN_X + spec.extra_side_padding + panel_width / 2.0,
        MARGIN_X + spec.extra_side_padding + panel_width + COL_GAP + panel_width / 2.0,
    )

    svg_root = ET.Element("svg", {"version": "1.1"})
    cursor_y = MARGIN_Y

    if spec.top_lines:
        for line in spec.top_lines:
            cursor_y += TOP_FONT
            create_text(svg_root, canvas_center_x, cursor_y, line, TOP_FONT, "middle")
            cursor_y += line_height(TOP_FONT) - TOP_FONT
        cursor_y += TOP_BLOCK_GAP

    if spec.column_headers:
        cursor_y += COLUMN_FONT
        for idx, header in enumerate(spec.column_headers):
            create_text(svg_root, col_centers[idx], cursor_y, header, COLUMN_FONT, "middle")
        cursor_y += line_height(COLUMN_FONT) - COLUMN_FONT + TOP_BLOCK_GAP

    for row_index, row in enumerate(spec.panels):
        row_header = spec.row_headers[row_index] if spec.row_headers else None
        if row_header:
            cursor_y += ROW_FONT
            create_text(svg_root, canvas_center_x, cursor_y, row_header, ROW_FONT, "middle")
            cursor_y += line_height(ROW_FONT) - ROW_FONT + TEXT_GAP

        panel_header_row = spec.panel_headers[row_index] if spec.panel_headers else (None, None)
        if any(panel_header_row):
            cursor_y += PANEL_FONT
            for idx, header in enumerate(panel_header_row):
                if header:
                    create_text(svg_root, col_centers[idx], cursor_y, header, PANEL_FONT, "middle")
            cursor_y += line_height(PANEL_FONT) - PANEL_FONT + TEXT_GAP

        row_top = cursor_y
        row_height = row_heights[row_index]
        for col_index, panel in enumerate(row):
            panel_path = resolve_panel_path(panel)
            panel_root = copy.deepcopy(ET.parse(panel_path).getroot())
            prefix_tree_ids(panel_root, f"{spec.basename}_r{row_index + 1}c{col_index + 1}")
            src_width, src_height = parse_svg_size(panel_root)
            scale = panel_width / src_width
            scaled_height = src_height * scale
            y_offset = (row_height - scaled_height) / 2.0
            panel_group = ET.SubElement(
                svg_root,
                "g",
                {
                    "transform": (
                        f"translate({MARGIN_X + col_index * (panel_width + COL_GAP):.3f},"
                        f" {row_top + y_offset:.3f}) scale({scale:.9f})"
                    ),
                },
            )
            if spec.extra_side_padding:
                panel_group.set(
                    "transform",
                    (
                        f"translate({MARGIN_X + spec.extra_side_padding + col_index * (panel_width + COL_GAP):.3f},"
                        f" {row_top + y_offset:.3f}) scale({scale:.9f})"
                    ),
                )
            for child in filtered_root_children(panel_root):
                panel_group.append(child)

        cursor_y += row_height
        if row_index != len(spec.panels) - 1:
            cursor_y += ROW_GAP

    if spec.bottom_lines:
        cursor_y += BOTTOM_BLOCK_GAP
        for line in spec.bottom_lines:
            cursor_y += BOTTOM_FONT
            create_text(svg_root, canvas_center_x, cursor_y, line, BOTTOM_FONT, "middle")
            cursor_y += line_height(BOTTOM_FONT) - BOTTOM_FONT

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

    output_path = SVG_ROOT / f"{spec.basename}.svg"
    tree = ET.ElementTree(svg_root)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path


def find_inkscape() -> str:
    candidates = ("inkscape.com", "inkscape")
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError("Could not find Inkscape in PATH")


def export_pdf(svg_path: Path) -> Path:
    pdf_path = PDF_ROOT / f"{svg_path.stem}.pdf"
    inkscape = find_inkscape()
    command = [
        inkscape,
        str(svg_path),
        "--export-type=pdf",
        f"--export-filename={pdf_path}",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Inkscape export failed for {svg_path.name}:\n"
            f"{completed.stdout}\n{completed.stderr}".strip()
        )
    return pdf_path


def build_all(selected: set[str] | None, export_pdfs: bool) -> None:
    for spec in FIGURE_SPECS:
        if selected and spec.basename not in selected:
            continue
        svg_path = build_svg(spec)
        print(f"Built SVG: {svg_path}")
        if export_pdfs:
            pdf_path = export_pdf(svg_path)
            print(f"Built PDF: {pdf_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Limit the build to one or more basenames",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip the PDF export step",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = set(args.only) if args.only else None
    build_all(selected=selected, export_pdfs=not args.no_pdf)


if __name__ == "__main__":
    main()
