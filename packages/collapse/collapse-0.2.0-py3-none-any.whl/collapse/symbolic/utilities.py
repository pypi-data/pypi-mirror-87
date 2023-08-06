"""Miscellaneous symbolic utilities"""

import functools
from typing import Tuple

from sympy import Rational, Expr, Matrix, simplify
from sympy.diffgeom import TensorProduct
from sympy.tensor.tensor import Tensor

from collapse.symbolic import constants


def tensor_pow(x: Tensor, n: int) -> Tensor:
    """Shorthand for computing reflexive tensor products of order n

    Args:
        x:
            Tensor, to be raised to power
        n:
            int, power to raise tensor

    Returns:
        Tensor, T^n
    """
    return functools.reduce(TensorProduct, n * [x])


def matrix_to_twoform(matrix: Matrix, base_forms: Tuple[Expr, ...]) -> Expr:
    """Logical inverse of sympy.diffgeom.twoform_to_matrix

    Args:
        matrix:
            Matrix, the matrix representation of the twoform to produce
        base_forms:
            Tuple[Expr], tuple of oneforms representing a basis of the cotangent bundle

    Returns:
        Expression of the twoform of the matrix in terms of the base oneforms
    """
    return sum([(1 if i == j else Rational(1, 2)) * TensorProduct(dx_i, dx_j) * matrix[i, j]
                for i, dx_i in enumerate(base_forms) for j, dx_j in enumerate(base_forms)])


def clean_expr(e: Expr, natural: bool = True) -> Expr:
    """Helper function to compute clean expression

    Args:
        e:
            Expr, expression to clean

    Returns:
        Expr, cleaned expression
    """
    if natural:
        e = constants.subs_natural(e)
    return simplify(e.doit())
