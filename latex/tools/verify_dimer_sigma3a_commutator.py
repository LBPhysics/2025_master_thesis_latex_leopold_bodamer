#!/usr/bin/env python3
"""Verify the sigma_31 / sigma_32 field terms in the four-level dimer backend.

This check reconstructs the field-driven part of the RWA equations from the
commutators

    dot(rho)|_field = i E(t) [mu_+, rho] + i E*(t) [mu_-, rho]

in the basis |0>, |1>, |2>, |3> with

    mu_+ = mu_10 |1><0| + mu_20 |2><0| + mu_31 |3><1| + mu_32 |3><2|
    mu_- = mu_10 |0><1| + mu_20 |0><2| + mu_31 |1><3| + mu_32 |2><3|

The goal is to verify explicitly that the (3,1) and (3,2) entries contain the
upper-manifold population rho_33, i.e.

    [mu_+, rho]_(3,1) = mu_31 (rho_11 - rho_33) + mu_32 rho_21
    [mu_+, rho]_(3,2) = mu_32 (rho_22 - rho_33) + mu_31 rho_12

which are the structures used in a01_numerical_implementation.tex.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, Tuple


DIM = 4
Index = Tuple[int, int]
Expr = Counter[str]
Matrix = Dict[Index, Expr]


def atom(symbol: str) -> Expr:
    return Counter({symbol: 1})


def canonical_product(left: str, right: str) -> str:
    factors = []
    for term in (left, right):
        factors.extend(part for part in term.split("*") if part and part != "1")
    factors.sort()
    return "*".join(factors) if factors else "1"


def clean(expr: Expr) -> Expr:
    return Counter({term: coeff for term, coeff in expr.items() if coeff})


def matmul(left: Matrix, right: Matrix) -> Matrix:
    out: Matrix = {}
    for i in range(DIM):
        for j in range(DIM):
            cell: Expr = Counter()
            for k in range(DIM):
                left_expr = left.get((i, k))
                right_expr = right.get((k, j))
                if not left_expr or not right_expr:
                    continue
                for left_term, left_coeff in left_expr.items():
                    for right_term, right_coeff in right_expr.items():
                        product = canonical_product(left_term, right_term)
                        cell[product] += left_coeff * right_coeff
            cell = clean(cell)
            if cell:
                out[(i, j)] = cell
    return out


def subtract(left: Matrix, right: Matrix) -> Matrix:
    out: Matrix = {}
    keys = set(left) | set(right)
    for key in keys:
        cell = Counter()
        cell.update(left.get(key, Counter()))
        cell.subtract(right.get(key, Counter()))
        cell = clean(cell)
        if cell:
            out[key] = cell
    return out


def commutator(left: Matrix, right: Matrix) -> Matrix:
    return subtract(matmul(left, right), matmul(right, left))


def format_expr(expr: Expr) -> str:
    if not expr:
        return "0"

    def term_key(item: Tuple[str, int]) -> Tuple[int, str]:
        term, coeff = item
        return (0 if coeff > 0 else 1, term)

    pieces = []
    for term, coeff in sorted(expr.items(), key=term_key):
        sign = "+" if coeff > 0 else "-"
        magnitude = abs(coeff)
        if magnitude == 1:
            pieces.append(f"{sign} {term}")
        else:
            pieces.append(f"{sign} {magnitude}*{term}")
    text = " ".join(pieces)
    return text[2:] if text.startswith("+ ") else text


def expected_expr(*terms: Tuple[int, str]) -> Expr:
    expr: Expr = Counter()
    for coeff, monomial in terms:
        expr[monomial] += coeff
    return clean(expr)


def build_mu_plus() -> Matrix:
    return {
        (1, 0): atom("mu10"),
        (2, 0): atom("mu20"),
        (3, 1): atom("mu31"),
        (3, 2): atom("mu32"),
    }


def build_mu_minus() -> Matrix:
    return {
        (0, 1): atom("mu10"),
        (0, 2): atom("mu20"),
        (1, 3): atom("mu31"),
        (2, 3): atom("mu32"),
    }


def build_rho() -> Matrix:
    return {(i, j): atom(f"rho{i}{j}") for i in range(DIM) for j in range(DIM)}


def verify() -> None:
    mu_plus = build_mu_plus()
    mu_minus = build_mu_minus()
    rho = build_rho()

    comm_plus = commutator(mu_plus, rho)
    comm_minus = commutator(mu_minus, rho)

    checks = [
        ("[mu_+, rho]_(3,1)", comm_plus[(3, 1)], expected_expr(
            (1, "mu31*rho11"),
            (1, "mu32*rho21"),
            (-1, "mu31*rho33"),
        )),
        ("[mu_+, rho]_(3,2)", comm_plus[(3, 2)], expected_expr(
            (1, "mu31*rho12"),
            (1, "mu32*rho22"),
            (-1, "mu32*rho33"),
        )),
        ("[mu_-, rho]_(3,1)", comm_minus[(3, 1)], expected_expr(
            (-1, "mu10*rho30"),
        )),
        ("[mu_-, rho]_(3,2)", comm_minus[(3, 2)], expected_expr(
            (-1, "mu20*rho30"),
        )),
    ]

    print("Field-driven commutator check for the four-level dimer backend\n")
    for label, actual, expected in checks:
        print(f"{label} = {format_expr(actual)}")
        if actual != expected:
            raise AssertionError(
                f"{label} does not match the expected expression.\n"
                f"Actual:   {format_expr(actual)}\n"
                f"Expected: {format_expr(expected)}"
            )

    print("\nVerified consequences for the envelope equations:")
    print("sigma31 receives  i E(t)  [mu31*(rho11-rho33) + mu32*rho21]")
    print("                   -i E*(t) mu10*sigma30")
    print("sigma32 receives  i E(t)  [mu32*(rho22-rho33) + mu31*rho12]")
    print("                   -i E*(t) mu20*sigma30")
    print("\nConclusion: the rho33 terms do appear in both sigma3a equations.")


if __name__ == "__main__":
    verify()
