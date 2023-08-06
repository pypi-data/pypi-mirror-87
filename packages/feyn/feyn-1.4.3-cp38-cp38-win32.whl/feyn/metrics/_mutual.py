"""
Code for calculating the mutual information (MI)
between several random variables.
"""

from logging import raiseExceptions
from os.path import join
import numpy as np
from functools import reduce

from typing import Iterable, Union, Tuple

def calculate_mi(rv_samples: Iterable[Iterable], target: Iterable, float_bins: int = 100) -> float:
    """
    Numpy-based implementation of mutual information for joint distribution of n random variables and a target variable. This can be used for both categorical (discrete) and continuous variables, you can have as many as you want of each for the joint distribution.

    Arguments:
        rv_samples {Iterable[Iterable]} -- Samples from random variables given inside an iterable. In the traditional ML sense, these would be the data of the input features.
        target {Iterable} -- Samples from target random variable

    Keyword Arguments:        
        float_bins {Union[Tuple[int], int]} -- Number of bins in which to count numerical random variables.

    Returns:
        float -- The mutual information between the joint distributino of random variables and the target.
    """

    # Construct samples and bins
    bins = []
    rv_input = []

    # Adding the target variable
    rv_samples_tar = [rv for rv in rv_samples]
    rv_samples_tar.append(target)
    
    for rv in rv_samples_tar:

        if type(rv).__name__ == "Series":
            sample = rv.iloc[0]
        else:
            sample = rv[0]

        if isinstance(sample, np.float) or isinstance(sample, float):
            bins.append(float_bins)
            rv_input.append(rv)
        else:
            if isinstance(sample, np.integer) or isinstance(sample, int):
                # All but the last (righthand-most) bin is half-open.
                # So one extra bin at the end ensures correct dist
                bins.append(len(np.unique(rv))+1)
                rv_input.append(rv)
            else:
                rv_encoded, ncats = _encode(rv)
                rv_input.append(rv_encoded)
                bins.append(ncats)

    joint_dist = _normalize_hist(np.histogramdd(rv_input, bins=bins)[0])
    nz_idx = np.nonzero(joint_dist)
    nz_joint = joint_dist[nz_idx]

    target_axis = joint_dist.ndim - 1
    marginal_input = joint_dist.sum(axis=target_axis)
    marginal_target = _integrate_to(joint_dist, target_axis)

    nz_mar_input = marginal_input[nz_idx[0:target_axis]]
    nz_mar_target = marginal_target[nz_idx[target_axis]]
    nz_outer = nz_mar_input * nz_mar_target

    return np.sum(nz_joint * (np.log(nz_joint) - np.log(nz_outer)))

def _integrate_to(arr, axis):
    """
    Given an n-dim array arr and an axis, sum all other axes to that one.
    """
    all_axes = range(arr.ndim)
    sum_these = tuple(ax for ax in all_axes if ax != axis)
    return arr.sum(axis=sum_these)

def _normalize_hist(arr):
    """
    Given an n-d array arr that represents a histogram, move from talking about counts to talking about probabilities (not probability densities).
    """
    return arr / arr.sum()

def _encode(discrete_rv):
    """
    Encode a 1D discrete random variable that does not contain integers to one that does.
    """
    ret = discrete_rv.copy()
    elems = np.unique(discrete_rv)

    for int_label, elem in enumerate(elems):
        ret[discrete_rv == elem] = int_label

    return ret.astype(int), len(elems)
