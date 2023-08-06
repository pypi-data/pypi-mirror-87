import unittest
from unittest import signals
import pytest

from feyn.__future__.contrib.reference._signal_search import get_model, repeated_kfold_regression_analysis, plot_kfold_traintest_score_results

import feyn
import _feyn
from feyn._graphmixin import GraphMetricsMixin
import sklearn
import numpy as np
import pandas as pd
import matplotlib

from os.path import dirname
filepath = dirname(__file__)

@pytest.mark.future
class TestSignalSearch(unittest.TestCase):

    def setUp(self):
        self.data = pd.read_csv(f'{filepath}/simple_data.csv')
        self.target = 'y'

    def test_get_model_returns_qlattice(self):
        # Setup
        qlattice = feyn.QLattice()

        # Execute
        model = get_model(qlattice)

        # Assert
        assert type(model) == feyn.QLattice

    def test_get_model_returns_tree(self):
        # Setup
        model_type = 'tree'

        # Execute
        model = get_model(model_type)

        # Assert
        assert type(model) == sklearn.tree._classes.DecisionTreeRegressor

    def test_get_model_returns_linear(self):
        # Setup
        model_type = 'linear'

        # Execute
        model = get_model(model_type)

        # Assert
        assert type(model) == sklearn.linear_model._base.LinearRegression

    def test_get_model_unknown_type(self):
        # Setup
        model_type = 'banana'

        # Execute & Assert
        self.assertRaises(ValueError, get_model, model_type)

    def test_repeated_kfold_regression_analysis_runs_for_tree(self):
        # Setup
        model_type = 'tree'

        # Execute
        result = repeated_kfold_regression_analysis(self.data, self.target, model_type, n_repeats=1)

        # Assert
        assert type(result) == np.ndarray
        assert result.shape == (1, 3, 2)

    def test_repeated_kfold_regression_analysis_runs_for_linear(self):
        # Setup
        model_type = 'linear'

        # Execute
        result = repeated_kfold_regression_analysis(self.data, self.target, model_type, n_repeats=1)

        # Assert
        assert type(result) == np.ndarray
        assert result.shape == (1, 3, 2)

    def test_repeated_kfold_regression_analysis_runs_for_qlattice(self):
        # Setup
        model_type = FakeQLattice()

        # Execute
        result = repeated_kfold_regression_analysis(self.data, self.target, model_type, qlattice_updates=1, n_splits=2, n_repeats=1)

        # Assert
        assert type(result) == np.ndarray
        assert result.shape == (1, 2, 2)
        assert (result == np.array([[[42, 42], [42, 42]]])).all()


class FakeQLattice(feyn.QLattice):

    def __init__(self):
        pass

    def reset(self):
        pass

    def get_regressor(self, registers, output, stypes, max_depth):
        return FakeQGraph(self, {'banana': 'face'})

    def update(self, graphs):
        pass


class FakeQGraph(feyn.QGraph):

    def __init__(self, qlattice, registers):
        self._graphs = [FakeGraph(2)]

    def fit(self, data, n_samples=None, loss_function=_feyn.DEFAULT_LOSS, show="graph", threads=1, sample_weights=None):
        pass

    def best(self, n=3):
        return self._graphs


class FakeGraph(feyn.Graph, GraphMetricsMixin):
    def r2_score(self, data):
        return 42
