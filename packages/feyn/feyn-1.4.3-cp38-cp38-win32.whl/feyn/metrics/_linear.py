"""Code for operations involving linear models and assumptions."""

import numpy as np

from typing import Union

def calculate_pc(X:np.ndarray, Y:np.ndarray) -> float:
    """ Calculate the Pearson correlation coefficient
    for data sampled from two random variables X and Y.

    Arguments:
        X {np.ndarray} -- First 1D vector of random data.
        Y {np.ndarray} -- First 1D vector of random data.

    Returns:
        float -- The correlation coefficient.
    """    

    n = len(X)

    x_bar = np.mean(X)
    y_bar = np.mean(Y)

    cov_xy = np.sum((X - x_bar) * (Y - y_bar))
    cov_xy = cov_xy / (n-1)

    return cov_xy / (np.std(X) * np.std(Y))
