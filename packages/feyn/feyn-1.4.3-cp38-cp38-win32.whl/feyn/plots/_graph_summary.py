import numpy as np
import feyn

from typing import Iterable, Optional

from feyn.plots._svg_toolkit import SVGGraphToolkit
from feyn.metrics import get_pearson_correlations, get_mutual_information, get_summary_information

def plot_graph_summary(graph:feyn.Graph, dataframe:Iterable, corr_func:Optional[str]=None, test:Optional[Iterable]=None): # -> "SVG":
    """
    Plot a graph displaying the signal path and summary metrics for the provided feyn.Graph and DataFrame.

    Arguments:
        graph {feyn.Graph}   -- A feyn.Graph we want to describe given some data.
        dataframe {Iterable} -- A Pandas DataFrame for showing metrics.

    Keyword Arguments:
        corr_func {Optional[str]} -- A name for the correlation function to use as the node signal, either 'mi' or 'pearson' are available. (default: {None} defaults to 'mi')
        test {Optional[Iterable]} -- A Pandas DataFrame for showing additional metrics. (default: {None})

    Raises:
        ValueError: Raised if the name of the correlation function is not understood.

    Returns:
        SVG -- SVG of the graph summary.
    """

    gtk = SVGGraphToolkit()

    if corr_func is None or corr_func == "mi":
        # Default to mutual information
        signal_func = get_mutual_information
    elif corr_func == "pearson":
        signal_func = get_pearson_correlations
    else:
        raise ValueError("Correlation function name not understood.")

    node_signal = np.abs(signal_func(graph, dataframe)) # Always use the absolute value of the signal
    summary = get_summary_information(graph, dataframe)

    gtk.add_graph(graph, node_signal=node_signal).add_summary_information(summary, "Metrics")

    if test is not None:
        test_summary = get_summary_information(graph, test)
        gtk.add_summary_information(test_summary, "Test Metrics")

    from IPython.display import HTML
    return HTML(gtk._repr_html_())
