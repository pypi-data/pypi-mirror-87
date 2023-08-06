import re
import unittest

import requests
import httpretty
import numpy as np
import pytest

import feyn.filters
import feyn.losses
from feyn import QLattice


class TestSDK(unittest.TestCase):
    def setUp(self):
        self.lt = QLattice()
        self.lt.reset()

    def test_init_arguments_validation(self):
        url = "http://example.com"

        with self.subTest("raises if section is combined with url or token"):
            with self.assertRaises(ValueError):
                QLattice(config="section", url=url, api_token="token")

            with self.assertRaises(ValueError):
                QLattice(config="section", url=url)

            with self.assertRaises(ValueError):
                QLattice(config="section", api_token="token")

        with self.subTest("raises if only url or token is specified"):
            with self.assertRaises(ValueError):
                QLattice(api_token="token")


    def test_can_add_new_registers(self):
        self.assertEqual(len(self.lt.registers), 0)

        # Get a qgraph which has the side effect of creating the registers
        self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        with self.subTest("Registers are available in the qlattice after addition"):
            self.assertEqual(len(self.lt.registers), 3)


    def test_delete_registers(self):
        self.assertEqual(len(self.lt.registers), 0)

        # Get a qgraph which has the side effect of creating the registers
        self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        with self.subTest("Registers can be deleted with del"):
            del(self.lt.registers["age"])
            self.assertEqual(len(self.lt.registers), 2)

        with self.subTest("Registers can be deleted with delete"):
            self.lt.registers.delete("smoker")
            self.assertEqual(len(self.lt.registers), 1)

        with self.assertRaises(ValueError) as ex:
            self.lt.registers.delete("non_existing")

        self.assertIn("non_existing", str(ex.exception))


    def test_qlattice_can_get_classifier(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        self.assertGreater(len(qgraph), 0)

    def test_qlattice_can_get_regressor(self):
        qgraph = self.lt.get_regressor(["age", "smoker", "insurable"], "lifexpectancy")

        self.assertGreater(len(qgraph), 0)


    def test_fit_qgraph(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        with self.subTest("Can fit with default arguments"):
            qgraph.fit(data, n_samples=100, show=None)

        with self.subTest("Can fit with named loss function"):
            qgraph.fit(data, n_samples=100, loss_function="absolute_error", show=None)

        with self.subTest("Can fit with loss function"):
            qgraph.fit(data, n_samples=100, loss_function=feyn.losses.absolute_error, show=None)


    def test_can_refresh_qgraph_after_updates(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")
        self.lt.update(qgraph[0])

        qgraph._refresh()
        self.assertGreater(len(qgraph._graphs), 0)

    def test_update_qgraph_with_older_graph(self):
        qg1 = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")
        graph = qg1[0]

        self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")
        self.lt.update(graph)

    def test_can_get_qgraph_with_any_column_as_output(self):
        columns = ["age", "smoker", "insurable"]
        for target in columns:
            qgraph = self.lt.get_regressor(columns, target)
            self.assertGreater(len(qgraph), 0)

    def test_qgraph_sort(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        qgraph.fit(data, n_samples=100, show=None)

        testdata = {
            "age": np.array([8, 16, 25, 50]),
            "smoker": np.array([0, 0, 1, 1]),
            "insurable": np.array([1, 0, 1, 0])
        }

        with self.subTest("Can sort with data"):
            qg = qgraph.sort(testdata)
            # TODO: Test that it was sorted by loss on the data
            self.assertIsNotNone(qg)

        with self.subTest("Can provide a loss function"):
            qg = qgraph.sort(testdata, loss_function=feyn.losses.absolute_error)
            # TODO: Test that they actually got sorted by that loss function
            self.assertIsNotNone(qg)

        with self.subTest("Can provide the name of a loss function"):
            qg = qgraph.sort(testdata, loss_function="absolute_error")
            # TODO: Test that they actually got sorted by that loss function
            self.assertIsNotNone(qg)

    def test_qgraph_filter(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        qgraph.fit(data, n_samples=100, show=None)

        with self.subTest("Can filter with depth"):
            qg = qgraph.filter(feyn.filters.Depth(1))
            for g in qg:
                self.assertEqual(g.depth, 1)

        with self.subTest("Can filter with edges"):
            qg = qgraph.filter(feyn.filters.Edges(3))
            for g in qg:
                self.assertEqual(g.edges, 3)

        with self.subTest("Can filter with contains"):
            qg = qgraph.filter(feyn.filters.Contains("smoker"))
            for g in qg:
                self.assertTrue("smoker" in g)

    def test_retries_failed_updates(self):
        qgraph = self.lt.get_classifier(["age", "smoker", "insurable"], "insurable")

        with httpretty.enabled():
            # Ideally we would have liked to just mock out the update http call.
            # But it is not possible in httpretty. And at same time, we are
            # creating the socket through request.session and init time of the
            # qlattice. So this socket cannot be highjacked by httpretty.
            # See this: https://github.com/gabrielfalcao/HTTPretty/issues/381
            self.lt._http_client = feyn._httpclient.HttpClient("http://example.org/api")
            self.lt._http_client.get_adapter("http://").max_retries.backoff_factor = 0.1  # Instant retries

            httpretty.register_uri(
                httpretty.POST,
                re.compile(r'http://.*'),
                status=502
            )

            with self.assertRaisesRegex(requests.exceptions.HTTPError, "502"):
                self.lt.update(qgraph[0])

            self.assertEqual(len(httpretty.latest_requests()), 3, "Did not retry the failed requests")
