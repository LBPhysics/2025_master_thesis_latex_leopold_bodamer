# Monomer Removed `paper_eqs` Paths

This file records the monomer comparison pairs that use the same thesis-side parameter set and differ only by solver backend (`paper_eqs` vs. `lindblad`).

The paths below are the extensionless base paths used in the LaTeX macros in `latex/chapters/c40_results.tex`. The figure loader resolves them to `.png`, `.pdf`, or `.jpg`.

## Main-text duplicate pairs

These are the two duplicate `paper_eqs` panels that were removed from the main monomer discussion in `latex/chapters/c40_results.tex`.

1. Fig. 2 homogeneous time-domain validation
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114405_monomer_fig2_homogeneous_paper_eqs/time_all_signals_real_imag_abs_monomer_fig2_homogeneous_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/time_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad`
2. Fig. 2 homogeneous frequency-domain validation
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114405_monomer_fig2_homogeneous_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig2_homogeneous_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/08_114400_monomer_fig2_homogeneous_lindblad/freq_all_signals_real_imag_abs_monomer_fig2_homogeneous_lindblad`

## Same-parameter solver-only pairs in the monomer atlas

These are the remaining monomer `paper_eqs`/`lindblad` comparison pairs defined in `latex/chapters/c40_results.tex` and used in `latex/appendices/a06_paper_eqs_reference_atlas.tex`.

### Fig. 2 inhomogeneous 1D time-domain

1. `N_inhom = 10`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114130_monomer_fig2_inhomogeneous_paper_eqs_n10/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n10`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172159_monomer_fig2_inhomogeneous_lindblad_n10/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10`
2. `N_inhom = 100`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114210_monomer_fig2_inhomogeneous_paper_eqs_n100/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n100`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172209_monomer_fig2_inhomogeneous_lindblad_n100/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n100`
3. `N_inhom = 1000`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_120126_monomer_fig2_inhomogeneous_paper_eqs_n1000/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n1000`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_165352_monomer_fig2_inhomogeneous_lindblad_n1000/time_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n1000`

### Fig. 2 inhomogeneous 1D frequency-domain

1. `N_inhom = 10`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114130_monomer_fig2_inhomogeneous_paper_eqs_n10/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n10`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172159_monomer_fig2_inhomogeneous_lindblad_n10/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n10`
2. `N_inhom = 100`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_114210_monomer_fig2_inhomogeneous_paper_eqs_n100/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n100`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172209_monomer_fig2_inhomogeneous_lindblad_n100/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n100`
3. `N_inhom = 1000`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_120126_monomer_fig2_inhomogeneous_paper_eqs_n1000/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_paper_eqs_n1000`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_165352_monomer_fig2_inhomogeneous_lindblad_n1000/freq_all_signals_real_imag_abs_monomer_fig2_inhomogeneous_lindblad_n1000`

### Fig. 3 homogeneous waiting-time series, 2D time-domain

1. `T = 0 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111423_monomer_fig3_T000_paper_eqs/time_all_signals_real_imag_abs_monomer_fig3_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172218_monomer_fig3_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T000_lindblad`
2. `T = 20 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111427_monomer_fig3_T020_paper_eqs/time_all_signals_real_imag_abs_monomer_fig3_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172229_monomer_fig3_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T020_lindblad`
3. `T = 40 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_110420_monomer_fig3_T040_paper_eqs/time_all_signals_real_imag_abs_monomer_fig3_T040_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172238_monomer_fig3_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig3_T040_lindblad`

### Fig. 3 homogeneous waiting-time series, 2D frequency-domain

1. `T = 0 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111423_monomer_fig3_T000_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig3_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172218_monomer_fig3_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T000_lindblad`
2. `T = 20 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111427_monomer_fig3_T020_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig3_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172229_monomer_fig3_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T020_lindblad`
3. `T = 40 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_110420_monomer_fig3_T040_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig3_T040_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172238_monomer_fig3_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig3_T040_lindblad`

### Fig. 4 inhomogeneous waiting-time series, 2D time-domain

1. `T = 0 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111432_monomer_fig4_T000_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172248_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
2. `T = 20 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111438_monomer_fig4_T020_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172302_monomer_fig4_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T020_lindblad`
3. `T = 40 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111444_monomer_fig4_T040_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T040_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172315_monomer_fig4_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T040_lindblad`

### Fig. 4 inhomogeneous waiting-time series, 2D frequency-domain

1. `T = 0 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111432_monomer_fig4_T000_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172248_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
2. `T = 20 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111438_monomer_fig4_T020_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172302_monomer_fig4_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T020_lindblad`
3. `T = 40 fs`
   - `paper_eqs`: `figures/svgs/monomer_essential_results/08_111444_monomer_fig4_T040_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T040_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/07_172315_monomer_fig4_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T040_lindblad`

## Legacy higher-field sensitivity pairs

These older comparison pairs also differ only by `paper_eqs` vs. `lindblad`, but they belong to the supplementary stronger-field sensitivity archive rather than the standardized main monomer atlas.

1. Fig. 4, `T = 0 fs`, `N_inhom = 10`, time-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_181830_monomer_fig4_T000_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_181835_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
2. Fig. 4, `T = 0 fs`, `N_inhom = 10`, frequency-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_181830_monomer_fig4_T000_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_181835_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
3. Fig. 4, `T = 0 fs`, `N_inhom = 100`, time-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_184012_monomer_fig4_T000_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_184018_monomer_fig4_T000_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
4. Fig. 4, `T = 0 fs`, `N_inhom = 100`, frequency-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_184012_monomer_fig4_T000_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T000_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_184018_monomer_fig4_T000_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T000_lindblad`
5. Fig. 4, `T = 20 fs`, `N_inhom = 100`, time-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_184031_monomer_fig4_T020_paper_eqs/time_all_signals_real_imag_abs_monomer_fig4_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_184037_monomer_fig4_T020_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T020_lindblad`
6. Fig. 4, `T = 20 fs`, `N_inhom = 100`, frequency-domain
   - `paper_eqs`: `figures/svgs/monomer_essential_results/01_184031_monomer_fig4_T020_paper_eqs/freq_all_signals_real_imag_abs_monomer_fig4_T020_paper_eqs`
   - `lindblad`: `figures/svgs/monomer_essential_results/01_184037_monomer_fig4_T020_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T020_lindblad`

## Unpaired legacy case

This related legacy run does not have a `paper_eqs` counterpart defined in `c40_results.tex`, so it is not part of the solver-only duplicate list above.

- Fig. 4, `T = 40 fs`, `N_inhom = 100`, time-domain
  - `lindblad` only: `figures/svgs/monomer_essential_results/01_184055_monomer_fig4_T040_lindblad/time_all_signals_real_imag_abs_monomer_fig4_T040_lindblad`
- Fig. 4, `T = 40 fs`, `N_inhom = 100`, frequency-domain
  - `lindblad` only: `figures/svgs/monomer_essential_results/01_184055_monomer_fig4_T040_lindblad/freq_all_signals_real_imag_abs_monomer_fig4_T040_lindblad`
