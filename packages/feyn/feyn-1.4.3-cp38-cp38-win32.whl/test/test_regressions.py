"""
This file contains regression errors observed in production. Some of these tests may
be a bit gnarly formulated, they may be a bit more fragile, and they probably do not
smell like a requirement specification for the feyn.

The idea is, that these can be deleted whenever they become too annoying.
"""

import unittest

import numpy as np

import feyn
from feyn import QLattice

class TestMiscRegressions(unittest.TestCase):

    def test_graph_handles_nans(self):
        in_reg = feyn.Interaction("in:linear(f)->i", (0,-1,-1), name="in_reg")
        tanh = feyn.Interaction("cell:tanh(i)->i", (0,0,0))
        out_reg = feyn.Interaction("out:linear(i)->f", (1,-1,-1), name="out_reg")

        g = feyn.Graph(3)
        g[0] = in_reg
        g[1] = tanh
        g[2] = out_reg

        in_reg._set_source(0, -1)
        tanh._set_source(0, 0)
        out_reg._set_source(0, 1)

        with self.subTest("ValueError when Nan in input"):
            with self.assertRaises(ValueError) as ctx:
                data = { "in_reg": [np.nan] }
                g.predict(data)

            self.assertIn("nan", str(ctx.exception))

        with self.subTest("ValueError when inf in input"):
            with self.assertRaises(ValueError) as ctx:
                data = { "in_reg": [np.inf] }
                g.predict(data)

            self.assertIn("inf", str(ctx.exception))

        with self.subTest("ValueError when Nan in output"):
            with self.assertRaises(ValueError) as ctx:
                data = {
                    "in_reg": np.array([1.0]),
                    "out_reg": np.array([np.nan])
                }
                g._fit(data, loss_function=feyn.losses.squared_error)

            self.assertIn("nan", str(ctx.exception))


    def test_qgraph_filter_works_with_numpy_int(self):
        lt = QLattice()
        lt.reset()

        data = {
            "reg1": np.array([10, 20, 30]),
            "reg2": np.array([10, 20, 30]),
            "reg3": np.array([10, 20, 30])
        }

        qgraph = lt.get_regressor(["reg1", "reg2", "reg3"], "reg3")
        qgraph = qgraph.filter(feyn.filters.MaxDepth(np.int64(2)))
        qgraph = qgraph.fit(data, n_samples=10, show=None)

        self.assertIsNotNone(qgraph)
