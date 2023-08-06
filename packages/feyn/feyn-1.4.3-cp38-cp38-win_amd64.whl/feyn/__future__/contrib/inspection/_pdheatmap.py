import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from feyn.insights import KernelShap


def _plot_colorbar(absmax, cmap='RdYlGn'):
    fig, ax = plt.subplots(figsize=(5, 0.5))
    ax.get_yaxis().set_visible(False)
    ax.set_title('Contribution (SHAP)')
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    ax.imshow(gradient, extent=[-absmax, absmax, 0, 1], aspect='auto',
              cmap=plt.get_cmap(cmap))


def _calculating_col_gradient(series, importance_values, absmax, cmap='RdYlGn'):
    """ Parameters:
            series: The series to get the styles for
            importance_values: the values to compute the colors for
            absmax: Highest absolute value
        Returns: styles for a pandas dataframe as a background color gradient"""
    if series.name in importance_values.columns:
        importance_series = importance_values[series.name]
        normalizer = colors.Normalize(-absmax, absmax)
        normed_df = normalizer(importance_series.values)

        colorlist = [colors.rgb2hex(x) for x in plt.cm.get_cmap(cmap)(normed_df)]
        return ['background-color: %s' % color for color in colorlist]
    return ['' for i in range(len(importance_values))]


def _get_percent_color(value, absmax):
    """ Related to a bar chart, returns the percent coloring in either
        direction assuming 50% is the middle
    """
    return 50 + value/absmax*50


def _get_gradient_string(value):
    if value > 50:
        # Try to make sure you can always see the sliver of contribution, even if it's small.
        value = max(53, value)
        return f"background: linear-gradient(90deg, transparent 50.0%, #5fba7d 50.0%, #5fba7d {value}%, transparent {value}%)"
    elif value < 50:
        value = min(47, value)
        return f"background: linear-gradient(90deg, transparent {value}%, #d65f5f {value}%, #d65f5f 50.0%, transparent 50.0%)"
    else:
        return 'background-color: default'


def _calculating_col_gradient_bar(series, importance_values, absmax):
    """ Parameters:
            series: The series to get the styles for
            importance_values: the values to compute the colors for
            absmax: Highest absolute value
        Returns: styles for a pandas dataframe as a bar chart """
    if series.name in importance_values.columns:
        importance_series = importance_values[series.name]
        percentages = [_get_percent_color(v, absmax) for v in importance_series.values]
        return [_get_gradient_string(pct) for pct in percentages]
    return ['' for i in range(len(importance_values))]


def _handle_ensemble(ensembler, dataframe, bg_data, max_ref_samples=100):
    importances = pd.DataFrame([], columns=dataframe.columns)
    bg_importances = pd.DataFrame([], columns=bg_data.columns)

    # We only use the background shap values for the absmax reference in coloring, so no need to be super precise
    # Better to be FAST
    max_ref_samples = max_ref_samples if len(bg_data) > max_ref_samples else len(bg_data)
    bg_samples = bg_data.sample(max_ref_samples)

    # pd.concat will add multiple entries for the same index value
    for graph in ensembler.graphs:
        # Note: We do want the full background data here
        explainer = KernelShap(graph, bg_data)

        # Reset indices to avoid duplicate indices in case they exist as it will contaminate aggregation. Restore index after aggregation.
        bg_imp = explainer.SHAP(bg_samples.reset_index())
        bg_imp = pd.DataFrame(bg_imp, columns=bg_samples.columns)

        imp = explainer.SHAP(dataframe.reset_index())
        imp = pd.DataFrame(imp, columns=dataframe.columns, index=dataframe.index)

        bg_importances = pd.concat([bg_importances, bg_imp], sort=True)
        importances = pd.concat([importances, imp], sort=True)

    # fill NA's with 0, group by the index, and aggregate with the mean to average over each graphs shap value per sample, then restore previous index.
    avg_importances = importances.fillna(0).groupby(by=importances.index).agg('mean').set_index('index', drop=True)
    avg_bg_importances = bg_importances.fillna(0).groupby(by=bg_importances.index).agg('mean').set_index('index', drop=True)

    return avg_importances, avg_bg_importances


def _get_absmax(x):
    return max(x.values.max(), np.abs(x.values.min()))


def plot_importance_dataframe(graph, dataframe, bg_data=None, kind='bar', legend=True, cmap='RdYlGn', max_ref_samples=100):
    """ Paints a Pandas DataFrame according to feature importance in the provided model.

    Arguments:
        graph {feyn.Graph} -- The feyn graph to predict on
        dataframe {pd.DataFrame} -- The dataframe to paint

    Keyword Arguments:
        bg_data {pd.DataFrame} -- The dataframe to use for background data to get more accurate importance scores (default: {None})
        kind {str} -- The kind of coloring. Options: 'fill' or 'bar' (default: {'bar'})
        legend {bool} -- Show a legend (if kind='fill') (default: {True})
        cmap {str} -- The colormap to use (if kind='fill') (default: {'RdYlGn'})
        max_ref_samples {int} -- How many reference samples to take to define the limits of the plot (default: {100})

    Raises:
        Exception: if bad [kind] argument supplied.

    Returns:
        [pd.DataFrame.styling] -- A dataframe styled with colors according to importances
    """
    # Special handle if you're using an ensemble method.
    if 'FeynEnsemble' in str(type(graph)):
        if bg_data is None:
            bg_data = dataframe

        importance_values, bg_importance = _handle_ensemble(graph, dataframe, bg_data, max_ref_samples)
    elif bg_data is not None:
        max_ref_samples = len(bg_data) if max_ref_samples > len(bg_data) else max_ref_samples
        shap_explainer = KernelShap(graph, bg_data)
        bg_importance = shap_explainer.SHAP(bg_data.sample(max_ref_samples))
        importance_values = shap_explainer.SHAP(dataframe)
    else:
        shap_explainer = KernelShap(graph, dataframe)
        importance_values = shap_explainer.SHAP(dataframe)

    # TODO: Still pd-specific...
    importance_values = pd.DataFrame(importance_values, columns=dataframe.columns, index=dataframe.index)

    # TODO: Clean up the if/else statements a bit to reduce duplication.
    # Maybe always set bg_data to dataframe if none and accept double work?

    if bg_data is not None:
        # TODO: Still pd-specific...
        bg_importance = pd.DataFrame(bg_importance, columns=bg_data.columns)

        all_importances = pd.concat([bg_importance, importance_values], sort=True)
        std_dev = all_importances.std()[0]
        # Define the absmax from what it's seen, and the newly predicted values
        absmax = _get_absmax(all_importances)
        # Add a tiny visual buffer if we have uncertain absmax
        absmax = absmax + std_dev if max_ref_samples < len(bg_data) else absmax
    else:
        absmax = _get_absmax(importance_values)

    if kind not in ['bar', 'fill']:
        raise Exception(f"Kind {kind} not recognized. Must be either 'bar' or 'fill'")
    if kind == 'bar':
        painted_df = dataframe.style.apply(_calculating_col_gradient_bar,
                                           importance_values=importance_values,
                                           absmax=absmax)
    elif kind == 'fill':
        painted_df = dataframe.style.apply(_calculating_col_gradient,
                                           importance_values=importance_values,
                                           absmax=absmax,
                                           cmap=cmap)
        if legend:
            _plot_colorbar(absmax, cmap=cmap)

    return painted_df
