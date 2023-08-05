"""
Module containing the spacing functions for the binarycpython package
"""


import numpy as np


def const(min_bound, max_bound, steps):
    """
    Samples a range linearly. Uses numpy linspace.
    """

    return np.linspace(min_bound, max_bound, steps)
