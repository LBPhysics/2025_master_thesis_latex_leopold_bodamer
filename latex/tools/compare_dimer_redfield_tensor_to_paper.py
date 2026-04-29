#!/usr/bin/env python3
"""Compare QuTiP's Bloch-Redfield tensor to the rate-based paper Liouvillian.

The comparison is done for the field-free four-level dimer generator

    L0 (paper rates)  vs.  R_BR (QuTiP Bloch-Redfield tensor)

using the same dimer configuration and the same bath-coupling operators as the
production Redfield solver path in ``thesis_python``.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


THESIS_PYTHON_DEFAULT = Path(r"C:\Users\leopo\.vscode\thesis_python")
CONFIG_DEFAULT = THESIS_PYTHON_DEFAULT / "scripts" / "simulation_configs" / "dimer.yaml"
OUT_DIR_DEFAULT = Path("tmp") / "redfield_tensor_vs_paper"


@dataclass
class ComparisonCase:
    name: str
    display_name: str
    cutoff_input: float
    effective_cutoff_fs: float | None
    br_tensor: Any
    diff_tensor: Any
    max_abs_diff: float
    fro_norm_diff: float
    mean_abs_diff: float
    n_diff_gt_tol: int
    top_diffs: list[dict[str, Any]]


def _configure_import_paths(repo_root: Path) -> None:
    qspectro = repo_root / "packages" / "qspectro2d" / "src"
    plotstyle = repo_root / "packages" / "plotstyle" / "src"
    for path in (qspectro, plotstyle):
        as_str = str(path)
        if as_str not in sys.path:
            sys.path.insert(0, as_str)


def _superoperator_labels(dim: int, stacked_index) -> list[str]:
    entries = sorted((stacked_index(dim, i, j), i, j) for i in range(dim) for j in range(dim))
    return [f"{i}{j}" for _, i, j in entries]


def _complex_payload(value: complex) -> dict[str, float]:
    return {"re": float(np.real(value)), "im": float(np.imag(value))}


def _top_differences(
    diff: np.ndarray,
    br: np.ndarray,
    paper: np.ndarray,
    labels: list[str],
    *,
    count: int = 12,
) -> list[dict[str, Any]]:
    ranked = np.dstack(np.unravel_index(np.argsort(np.abs(diff).ravel())[::-1], diff.shape))[0]
    top_entries: list[dict[str, Any]] = []
    for row, col in ranked[:count]:
        top_entries.append(
            {
                "row": int(row),
                "col": int(col),
                "row_label": labels[int(row)],
                "col_label": labels[int(col)],
                "abs_diff": float(np.abs(diff[row, col])),
                "br": _complex_payload(complex(br[row, col])),
                "paper": _complex_payload(complex(paper[row, col])),
                "diff": _complex_payload(complex(diff[row, col])),
            }
        )
    return top_entries


def _dw_min(hamiltonian) -> float:
    eigvals = np.asarray(hamiltonian.eigenenergies(), dtype=float)
    dw_min = float("inf")
    for i in range(len(eigvals)):
        for j in range(i + 1, len(eigvals)):
            diff = abs(float(eigvals[j] - eigvals[i]))
            if diff > 0.0:
                dw_min = min(dw_min, diff)
    if not np.isfinite(dw_min):
        raise ValueError("Failed to determine a nonzero minimal eigenvalue spacing.")
    return dw_min


def _cutoff_text(cutoff_input: float, effective_cutoff_fs: float | None) -> str:
    if cutoff_input < 0:
        return "sec_cutoff = -1 (non-secular)"
    return (
        f"sec_cutoff = {cutoff_input:.6g}"
        f"\neffective cutoff = {effective_cutoff_fs:.6e} fs^-1"
    )


def _save_figure(fig: plt.Figure, out_base: Path, *, figsize: tuple[float, float] = (6, 6)) -> None:
    from plotstyle import save_fig

    save_fig(fig, out_base, formats=("png", "pdf", "svg"), figsize=figsize)


def _build_markdown_summary(
    *,
    summary_path: Path,
    cases: list[ComparisonCase],
    gap_w21: float,
    dw_min: float,
    tolerance: float,
) -> None:
    lines = [
        "# Dimer Redfield Tensor vs Paper Liouvillian",
        "",
        f"- `|omega_21| = {gap_w21:.12e} fs^-1`",
        f"- `dw_min` used internally by QuTiP for the secular cutoff is `{dw_min:.12e} fs^-1`.",
        f"- Difference threshold for counting mismatched entries: `{tolerance:.1e}`.",
        "",
    ]

    for case in cases:
        lines.append(f"## {case.display_name}")
        lines.append("")
        if case.cutoff_input < 0:
            lines.append("- `sec_cutoff = -1` disables the secular approximation.")
        else:
            lines.append(f"- Input `sec_cutoff = {case.cutoff_input:.12e}`.")
            lines.append(
                "- Effective QuTiP cutoff "
                f"`= sec_cutoff * dw_min = {case.effective_cutoff_fs:.12e} fs^-1`."
            )
        lines.append(f"- `max(|R - L0|) = {case.max_abs_diff:.12e}`")
        lines.append(f"- `||R - L0||_F = {case.fro_norm_diff:.12e}`")
        lines.append(f"- `mean(|R - L0|) = {case.mean_abs_diff:.12e}`")
        lines.append(f"- `n(|R - L0| > {tolerance:.1e}) = {case.n_diff_gt_tol}`")
        lines.append("")
        lines.append("Top differing entries:")
        for entry in case.top_diffs[:8]:
            lines.append(
                "- "
                f"`{entry['row_label']} <- {entry['col_label']}`: "
                f"`|diff| = {entry['abs_diff']:.6e}`"
            )
        lines.append("")

    summary_path.write_text("\n".join(lines), encoding="utf-8")


def _plot_comparison_grid(
    *,
    paper_tensor,
    cases: list[ComparisonCase],
    labels: list[str],
    out_base: Path,
    basis_caption: str,
) -> None:
    from qutip.visualization import matrix_histogram

    paper_abs_max = float(np.max(np.abs(paper_tensor.full())))
    br_abs_max = max(float(np.max(np.abs(case.br_tensor.full()))) for case in cases)
    diff_abs_max = max(float(np.max(np.abs(case.diff_tensor.full()))) for case in cases)
    common_abs_max = max(paper_abs_max, br_abs_max)
    if diff_abs_max == 0.0:
        diff_abs_max = 1.0

    plt.rcParams.update(
        {
            "font.size": 8,
            "axes.titlesize": 10,
            "figure.titlesize": 14,
        }
    )

    fig = plt.figure(figsize=(20, 18))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.94, bottom=0.05, wspace=0.16, hspace=0.24)
    cmap = plt.get_cmap("twilight")
    col_titles = [
        "Paper Liouvillian $L_0$",
        "QuTiP Bloch-Redfield tensor $R$",
        "Difference $R-L_0$",
    ]

    for row, case in enumerate(cases):
        tensors = [paper_tensor, case.br_tensor, case.diff_tensor]
        limits = [[0.0, common_abs_max], [0.0, common_abs_max], [0.0, diff_abs_max]]

        for col, (tensor, limit) in enumerate(zip(tensors, limits, strict=True)):
            ax = fig.add_subplot(len(cases), 3, row * 3 + col + 1, projection="3d")
            matrix_histogram(
                tensor,
                x_basis=labels,
                y_basis=labels,
                limits=limit,
                bar_style="abs",
                color_limits=[-math.pi, math.pi],
                color_style="phase",
                cmap=cmap,
                colorbar=(col == 2),
                fig=fig,
                ax=ax,
            )
            if row == 0:
                ax.set_title(col_titles[col], pad=14)
            ax.view_init(azim=-55, elev=45)
            ax.tick_params(axis="x", labelsize=6, pad=-2)
            ax.tick_params(axis="y", labelsize=6, pad=-2)
            ax.tick_params(axis="z", labelsize=7, pad=0)

        y_pos = 0.92 - row * 0.315
        fig.text(
            0.012,
            y_pos,
            "\n".join(
                [
                    case.display_name,
                    _cutoff_text(case.cutoff_input, case.effective_cutoff_fs),
                    f"max |R-L0| = {case.max_abs_diff:.3e}",
                    f"||R-L0||_F = {case.fro_norm_diff:.3e}",
                    f"n(|diff| > tol) = {case.n_diff_gt_tol}",
                ]
            ),
            ha="left",
            va="top",
            bbox={"facecolor": "white", "edgecolor": "0.82", "boxstyle": "round,pad=0.35"},
        )

    fig.suptitle(
        "Dimer: QuTiP Redfield tensor vs rate-based paper Liouvillian\n"
        "bars show |entry|, colors show phase",
        y=0.985,
    )
    fig.text(0.5, 0.015, basis_caption, ha="center", va="bottom", fontsize=9)
    _save_figure(fig, out_base)
    plt.close(fig)


def _plot_difference_focus(
    *,
    cases: list[ComparisonCase],
    labels: list[str],
    out_base: Path,
    basis_caption: str,
) -> None:
    from qutip import Qobj
    from qutip.visualization import hinton

    selected_names = {"nonsecular"}
    focus_cases = [case for case in cases if case.name in selected_names]
    if not focus_cases:
        return

    case = focus_cases[0]
    diff_array = np.asarray(case.diff_tensor.full(), dtype=np.complex128)
    diff_matrix = Qobj(
        np.real(diff_array),
        dims=[[diff_array.shape[0]], [diff_array.shape[1]]],
    )

    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=False)
    hinton(
        diff_matrix,
        x_basis=labels,
        y_basis=labels,
        color_style="scaled",
        cmap=plt.get_cmap("RdBu"),
        colorbar=True,
        fig=fig,
        ax=ax,
    )
    colorbar_ax = next((other_ax for other_ax in fig.axes if other_ax is not ax), None)
    main_pos = [0.14, 0.11, 0.68, 0.68]
    ax.set_position(main_pos)
    tick_positions = 0.5 + np.arange(len(labels))
    tick_fontsize = (
        ax.xaxis.get_ticklabels()[0].get_fontsize()
        if ax.xaxis.get_ticklabels()
        else float(matplotlib.rcParams["font.size"])
    )
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(labels, rotation=0, fontsize=tick_fontsize)
    ax.yaxis.set_visible(False)
    ax.tick_params(
        axis="x",
        top=True,
        labeltop=True,
        bottom=False,
        labelbottom=False,
        pad=1,
        length=4,
        width=0.8,
    )
    for y_pos, label in zip(tick_positions, reversed(labels), strict=True):
        ax.plot([-0.16, 0.0], [y_pos, y_pos], color="black", lw=0.8, clip_on=False)
        ax.text(
            -0.34,
            y_pos,
            label,
            ha="right",
            va="center",
            clip_on=False,
            fontsize=tick_fontsize,
        )
    if colorbar_ax is not None:
        cbar_height = main_pos[3] * 0.72
        cbar_y0 = main_pos[1] + 0.5 * (main_pos[3] - cbar_height)
        colorbar_ax.set_position([main_pos[0] + main_pos[2] + 0.055, cbar_y0, 0.024, cbar_height])
        colorbar_ax.tick_params(labelsize=tick_fontsize)
        colorbar_ax.yaxis.get_offset_text().set_size(tick_fontsize)
    ax.set_xlabel("")
    ax.set_ylabel("")
    _save_figure(fig, out_base, figsize=(4, 4))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare the dimer paper Liouvillian against QuTiP's Bloch-Redfield tensor.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--thesis_python_root",
        type=Path,
        default=THESIS_PYTHON_DEFAULT,
        help="Absolute path to the thesis_python repository.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_DEFAULT,
        help="Dimer config used for the comparison.",
    )
    parser.add_argument(
        "--out_dir",
        type=Path,
        default=OUT_DIR_DEFAULT,
        help="Directory where plots and metrics will be written.",
    )
    parser.add_argument(
        "--diff_tol",
        type=float,
        default=1.0e-10,
        help="Absolute threshold used when counting differing tensor entries.",
    )
    args = parser.parse_args()

    repo_root = args.thesis_python_root.resolve()
    config_path = args.config.resolve()
    out_dir = args.out_dir.resolve()

    _configure_import_paths(repo_root)

    from qutip import Qobj, stacked_index
    from qutip.core.blochredfield import bloch_redfield_tensor
    from plotstyle import init_style

    from qspectro2d.config.config import resolve_config
    from qspectro2d.config.factory import load_simulation
    from qspectro2d.core.simulation.paper_solver import paper_liouvillian_l0

    init_style()

    cfg = resolve_config(config_path, emit_runtime_warnings=False)
    cfg["config"]["solver"] = "redfield"
    sim = load_simulation(cfg, emit_runtime_warnings=False)

    paper_tensor = paper_liouvillian_l0(sim)
    paper_array = np.asarray(paper_tensor.full(), dtype=np.complex128)
    dims = paper_tensor.dims

    dw_min = _dw_min(sim.H0_diagonalized)
    gap_w21 = abs(float(sim.system.omega_ij(2, 1)))

    cutoff_specs = [
        ("full_secular", "Full secularization (1e-5)", 1.0e-5),
        ("half_gap", "Half-gap cutoff", 0.5 * gap_w21),
        ("nonsecular", "No secularization", -1.0),
    ]

    labels = _superoperator_labels(4, stacked_index)
    basis_caption = (
        "Superoperator basis order: "
        + ", ".join(labels)
        + " (labels denote vectorized density-matrix elements rho_ij)."
    )

    cases: list[ComparisonCase] = []
    for name, display_name, cutoff in cutoff_specs:
        br_tensor = bloch_redfield_tensor(
            sim.H0_diagonalized,
            sim.decay_channels,
            sec_cutoff=float(cutoff),
            fock_basis=True,
        )
        br_array = np.asarray(br_tensor.full(), dtype=np.complex128)
        diff_array = br_array - paper_array
        diff_tensor = Qobj(diff_array, dims=dims, superrep="super")

        effective_cutoff_fs = None if cutoff < 0 else float(cutoff * dw_min)
        max_abs_diff = float(np.max(np.abs(diff_array)))
        fro_norm_diff = float(np.linalg.norm(diff_array))
        mean_abs_diff = float(np.mean(np.abs(diff_array)))
        n_diff_gt_tol = int(np.count_nonzero(np.abs(diff_array) > args.diff_tol))

        cases.append(
            ComparisonCase(
                name=name,
                display_name=display_name,
                cutoff_input=float(cutoff),
                effective_cutoff_fs=effective_cutoff_fs,
                br_tensor=br_tensor,
                diff_tensor=diff_tensor,
                max_abs_diff=max_abs_diff,
                fro_norm_diff=fro_norm_diff,
                mean_abs_diff=mean_abs_diff,
                n_diff_gt_tol=n_diff_gt_tol,
                top_diffs=_top_differences(diff_array, br_array, paper_array, labels),
            )
        )

    plot_base = out_dir / "dimer_redfield_tensor_vs_paper_matrix_histograms"
    diff_focus_base = out_dir / "dimer_redfield_tensor_vs_paper_difference_focus"
    metrics_path = out_dir / "dimer_redfield_tensor_vs_paper_metrics.json"
    summary_path = out_dir / "dimer_redfield_tensor_vs_paper_summary.md"

    comparison_grid_error: str | None = None
    try:
        _plot_comparison_grid(
            paper_tensor=paper_tensor,
            cases=cases,
            labels=labels,
            out_base=plot_base,
            basis_caption=basis_caption,
        )
    except Exception as exc:
        comparison_grid_error = str(exc)
        print(f"Warning: failed to save comparison grid: {exc}")
    _plot_difference_focus(
        cases=cases,
        labels=labels,
        out_base=diff_focus_base,
        basis_caption=basis_caption,
    )

    payload = {
        "config_path": str(config_path),
        "thesis_python_root": str(repo_root),
        "omega_21_abs_fs": gap_w21,
        "dw_min_fs": dw_min,
        "difference_tolerance": args.diff_tol,
        "cases": [
            {
                "name": case.name,
                "display_name": case.display_name,
                "cutoff_input": case.cutoff_input,
                "effective_cutoff_fs": case.effective_cutoff_fs,
                "max_abs_diff": case.max_abs_diff,
                "fro_norm_diff": case.fro_norm_diff,
                "mean_abs_diff": case.mean_abs_diff,
                "n_diff_gt_tol": case.n_diff_gt_tol,
                "top_diffs": case.top_diffs,
            }
            for case in cases
        ],
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _build_markdown_summary(
        summary_path=summary_path,
        cases=cases,
        gap_w21=gap_w21,
        dw_min=dw_min,
        tolerance=args.diff_tol,
    )

    print("Dimer Redfield tensor vs paper Liouvillian comparison")
    print(f"  config: {config_path}")
    print(f"  |omega_21| = {gap_w21:.12e} fs^-1")
    print(f"  dw_min    = {dw_min:.12e} fs^-1")
    print()
    for case in cases:
        print(case.display_name)
        if case.cutoff_input < 0:
            print("  sec_cutoff = -1 (non-secular)")
        else:
            print(f"  sec_cutoff input    = {case.cutoff_input:.12e}")
            print(f"  effective cutoff    = {case.effective_cutoff_fs:.12e} fs^-1")
        print(f"  max |R-L0|          = {case.max_abs_diff:.12e}")
        print(f"  ||R-L0||_F          = {case.fro_norm_diff:.12e}")
        print(f"  mean |R-L0|         = {case.mean_abs_diff:.12e}")
        print(f"  n(|diff| > tol)     = {case.n_diff_gt_tol}")
        if case.top_diffs:
            top = case.top_diffs[0]
            print(
                "  top differing entry = "
                f"{top['row_label']} <- {top['col_label']} "
                f"(|diff| = {top['abs_diff']:.6e})"
            )
        print()

    if comparison_grid_error is None:
        print(f"Saved plot base: {plot_base}")
    else:
        print(f"Skipped comparison grid export: {comparison_grid_error}")
    print(f"Saved focus plot: {diff_focus_base}")
    print(f"Saved metrics:   {metrics_path}")
    print(f"Saved summary:   {summary_path}")


if __name__ == "__main__":
    main()
