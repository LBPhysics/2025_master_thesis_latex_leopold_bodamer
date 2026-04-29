# Dimer Redfield Tensor vs Paper Liouvillian

- `|omega_21| = 2.028805864040e-01 fs^-1`
- `dw_min` used internally by QuTiP for the secular cutoff is `1.014402932020e-01 fs^-1`.
- Difference threshold for counting mismatched entries: `1.0e-10`.

## Full secularization (1e-5)

- Input `sec_cutoff = 1.000000000000e-05`.
- Effective QuTiP cutoff `= sec_cutoff * dw_min = 1.014402932020e-06 fs^-1`.
- `max(|R - L0|) = 4.950882008532e-17`
- `||R - L0||_F = 1.981789105853e-16`
- `mean(|R - L0|) = 3.167771048494e-18`
- `n(|R - L0| > 1.0e-10) = 0`

Top differing entries:
- `23 <- 13`: `|diff| = 4.950882e-17`
- `13 <- 23`: `|diff| = 4.950882e-17`
- `02 <- 01`: `|diff| = 4.950882e-17`
- `12 <- 11`: `|diff| = 4.950882e-17`
- `12 <- 22`: `|diff| = 4.950882e-17`
- `22 <- 21`: `|diff| = 4.950882e-17`
- `22 <- 12`: `|diff| = 4.950882e-17`
- `32 <- 31`: `|diff| = 4.950882e-17`

## Half-gap cutoff

- Input `sec_cutoff = 1.014402932020e-01`.
- Effective QuTiP cutoff `= sec_cutoff * dw_min = 1.029013308491e-02 fs^-1`.
- `max(|R - L0|) = 4.950882008532e-17`
- `||R - L0||_F = 1.981789105853e-16`
- `mean(|R - L0|) = 3.167771048494e-18`
- `n(|R - L0| > 1.0e-10) = 0`

Top differing entries:
- `23 <- 13`: `|diff| = 4.950882e-17`
- `13 <- 23`: `|diff| = 4.950882e-17`
- `02 <- 01`: `|diff| = 4.950882e-17`
- `12 <- 11`: `|diff| = 4.950882e-17`
- `12 <- 22`: `|diff| = 4.950882e-17`
- `22 <- 21`: `|diff| = 4.950882e-17`
- `22 <- 12`: `|diff| = 4.950882e-17`
- `32 <- 31`: `|diff| = 4.950882e-17`

## No secularization

- `sec_cutoff = -1` disables the secular approximation.
- `max(|R - L0|) = 2.497777454500e-03`
- `||R - L0||_F = 4.885451659467e-03`
- `mean(|R - L0|) = 5.770598926047e-05`
- `n(|R - L0| > 1.0e-10) = 16`

Top differing entries:
- `12 <- 21`: `|diff| = 2.497777e-03`
- `21 <- 12`: `|diff| = 2.497777e-03`
- `21 <- 22`: `|diff| = 1.998222e-03`
- `12 <- 22`: `|diff| = 1.998222e-03`
- `13 <- 23`: `|diff| = 7.760747e-04`
- `31 <- 32`: `|diff| = 7.760747e-04`
- `01 <- 02`: `|diff| = 7.760747e-04`
- `10 <- 20`: `|diff| = 7.760747e-04`
