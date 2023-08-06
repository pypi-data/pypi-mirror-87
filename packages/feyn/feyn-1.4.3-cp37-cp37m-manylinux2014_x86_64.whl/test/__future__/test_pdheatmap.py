import unittest
import pytest

from feyn.__future__.contrib.inspection import plot_importance_dataframe
import feyn
import pandas as pd

from os.path import dirname
filepath = dirname(__file__)


class TestPdHeatmap(unittest.TestCase):

    @pytest.mark.future
    def test_that_it_runs(self):
        df = pd.read_csv(f'{filepath}/simple_data.csv')
        graph = feyn.Graph.load(f'{filepath}/simple.graph')

        heatmap = plot_importance_dataframe(graph, df)
        assert heatmap is not None, "Heatmap should be computed"
