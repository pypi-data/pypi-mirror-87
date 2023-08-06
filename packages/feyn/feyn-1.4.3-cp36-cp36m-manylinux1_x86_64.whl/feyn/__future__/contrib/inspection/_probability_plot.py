import numpy as np
import matplotlib.pyplot as plt


def _pos_neg_classes(y_true, y_pred):
    """Finds the probability distribution
    of the positive and negative classes.
    Order of truth and prediction matters.

    Arguments:
        y_true {array_like} -- Expected values (Truth)
        y_pred {array_like} -- Predicted values
    """

    # Hits and non-hits
    hits = y_pred[np.round(y_pred) == y_true]  # TP and TN
    non_hits = y_pred[np.round(y_pred) != y_true]  # FP and FN

    # Positive and Negative classes:
    pos_class = np.append(hits[np.round(hits) == 1],
                          non_hits[np.round(non_hits) == 0])  # TP and FN
    neg_class = np.append(hits[np.round(hits) == 0],
                          non_hits[np.round(non_hits) == 1])  # TN and FP

    return pos_class, neg_class


def _hist_args_styler(data, nbins):
    """Styler for histograms. It gives them
    an edge and transparency.

    Arguments:
        data {array_like} -- data array
        nbins {int} -- number of bins
    """
    range_t = (np.min(data), np.max(data))
    bin_edges = np.histogram_bin_edges(data, bins=nbins, range=range_t)

    h_args = {
        'bins': bin_edges,
        'range': range_t,
        'edgecolor': 'k',
        'lw': 1.5,
        'alpha': 0.7
    }

    return h_args


def plot_probability_scores(y_true, y_pred, title='', nbins=10, h_args=None):
    """Plots the histogram of probability scores in binary
    classification problems, highlighting the negative and
    positive classes. Order of truth and prediction matters.

    Arguments:
        y_true {array_like} -- Expected values (Truth)
        y_pred {array_like} -- Predicted values

    Keyword Arguments:
        title {str} -- plot title (default: {''})
        nbins {int} -- number of bins (default: {10})
        h_args {dict} -- histogram kwargs (default: {None})
    """

    pos_class, neg_class = _pos_neg_classes(y_true, y_pred)

    if h_args is None:
        unip_data = np.linspace(0., 1., 100)
        h_args = _hist_args_styler(unip_data, nbins)

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.hist(neg_class, label='Negative Class', **h_args)
    ax.hist(pos_class, label='Positive Class', **h_args)

    ax.legend(loc='upper center', fontsize=12)
    ax.set_ylabel('Number of ocurrences', fontsize=14)
    ax.set_xlabel('Probability Score', fontsize=14)
    ax.set_title(title, fontsize=14)

    return ax
