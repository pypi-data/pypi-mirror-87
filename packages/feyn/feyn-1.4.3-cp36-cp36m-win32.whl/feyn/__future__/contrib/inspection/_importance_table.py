import numpy as np

from feyn.insights import KernelShap
from feyn.plots._themes import Theme

from feyn.__future__.contrib.inspection._table_writer import TableWriter


class FeatureImportanceTable():
    def __init__(self, graph, dataframe, bg_data=None, max_ref_samples=100, max_rows=10, ensemble=False):
        self.data = dataframe
        self.max_ref_samples = max_ref_samples
        self.max_rows = len(self.data) if max_rows is None or max_rows > len(self.data) else max_rows

        self.has_bg_data = bg_data is not None

        # Just default if nothing supplied
        self.bg_data = bg_data if self.has_bg_data else dataframe

        # Special handle if you're using an ensemble wrapper.
        if ensemble:
            raise NotImplementedError("Not yet implemented")
        else:
            self.importance_values, self.bg_importance = self._get_importances(graph)

        self.max_value = self._calculate_max_value(self.importance_values, self.bg_importance)

    def write_table(self):
        table = ""
        if type(self.data).__name__ == "DataFrame":
            table = TableWriter(self.data,
                                max_rows=self.max_rows,
                                cell_styles=self._calculate_col_gradient_bar_pd)
        else:
            styles = self._calculate_col_gradient_bar()
            table = TableWriter(self.data, max_rows=self.max_rows, cell_styles=styles)
        return table._repr_html_()

    def _repr_html_(self):
        return self.write_table()

    def _get_importances(self, graph):
        shap_explainer = KernelShap(graph, self.bg_data)

        importance_values = shap_explainer.SHAP(self.data)

        if self.has_bg_data:
            max_ref_samples = self.max_ref_samples if len(self.bg_data) > self.max_ref_samples else len(self.bg_data)
            sanitized = _sanitize_dataframe(self.bg_data)
            bg_importance = shap_explainer.SHAP(_short_sample(sanitized, max_ref_samples))
        else:
            bg_importance = importance_values

        return importance_values, bg_importance

    def _handle_ensemble(self, ensembler):
        import pandas as pd
        #TODO: port this code proper and kill the pandas
        importances = pd.DataFrame([], columns=self.data.columns)
        bg_importances = pd.DataFrame([], columns=self.bg_data.columns)

        # pd.concat will add multiple entries for the same index value
        for graph in ensembler.graphs:
            imp, bg_imp = self._get_importances(graph)

            # TODO: kill the pandas
            bg_imp = pd.DataFrame(bg_imp, columns=self.bg_data.columns)
            imp = pd.DataFrame(imp, columns=self.data.columns, index=self.data.index)

            bg_importances = pd.concat([bg_importances, bg_imp], sort=True)
            importances = pd.concat([importances, imp], sort=True)

        # fill NA's with 0, group by the index, and aggregate with the mean to average over each graphs shap value per sample, then restore previous index.
        avg_importances = importances.fillna(0).groupby(by=importances.index).agg('mean').set_index('index', drop=True)
        avg_bg_importances = bg_importances.fillna(0).groupby(by=bg_importances.index).agg('mean')

        return avg_importances, avg_bg_importances

    def _calculate_max_value(self, importance_values, bg_importance):
        if self.has_bg_data:
            all_importances = np.vstack([bg_importance, importance_values])
            std_dev = all_importances.std()
            # Define the absmax from what it's seen, and the newly predicted values
            absmax = _get_absmax(all_importances)

            # Add a tiny visual buffer if we have uncertain absmax
            if self.max_ref_samples < len(self.bg_data):
                absmax = absmax + std_dev
        else:
            absmax = _get_absmax(importance_values)

        return absmax

    def _calculate_col_gradient_bar_pd(self, series):
        """ Parameters:
                series: The series to get the styles for
            Returns: styles for a pandas dataframe as a bar chart """
        # Get the index of the series in our supplied dataframe
        # This is pandas specific, but we also know we're in panda land.
        col_idx = list(self.data.columns).index(series.name)
        importance_series = self.importance_values[:self.max_rows, col_idx]
        percentages = [_get_percent_color(v, self.max_value) for v in importance_series]
        return [_get_gradient_string(pct) for pct in percentages]

    def _calculate_col_gradient_bar(self):
        """ Returns: styles as an np.array for a table as a bar chart """

        keys = list(self.data.keys())
        styles = np.empty(shape=(len(self.data[keys[0]]), len(keys)), dtype=object)
        for idx, col in enumerate(self.data.keys()):
            importance_series = self.importance_values[:, idx]
            percentages = [_get_percent_color(v, self.max_value) for v in importance_series]
            styles[:, idx] = [_get_gradient_string(pct) for pct in percentages]

        return styles[:self.max_rows, :]


def _get_absmax(x):
    return max(x.max(), np.abs(x.min()))


def _get_percent_color(value, absmax):
    """ Related to a bar chart, returns the percent coloring in either
        direction assuming 50% is the middle
    """
    return 50 + value/absmax*50


def _get_gradient_string(value):
    primary = Theme.color('primary')
    accent = Theme.color('accent')
    if value > 50:
        # Try to make sure you can always see the sliver of contribution, even if it's small.
        value = max(53, value)
        return f"background: linear-gradient(90deg, transparent 50.0%, {primary} 50.0%, {primary} {value}%, transparent {value}%)"
    elif value < 50:
        value = min(47, value)
        return f"background: linear-gradient(90deg, transparent {value}%, {accent} {value}%, {accent} 50.0%, transparent 50.0%)"
    else:
        return 'background-color: default'


def _short_sample(data, no_samples):
    """ Sample function that does not oversample nor sample with replacement.

    Arguments:
        data {[np_dict]} -- a dictionary of numpy arrays
        no_samples {[type]} -- number of samples to take up till len(data)
    """
    length = len(data[list(data.keys())[0]])
    permutation = np.random.permutation(length)

    return {col: data[col][permutation][:no_samples] for col in data}


def _sanitize_dataframe(maybe_df):
        if type(maybe_df).__name__ == "DataFrame":
            data = {col: maybe_df[col].values for col in maybe_df.columns}
        else:
            data = maybe_df

        return data
