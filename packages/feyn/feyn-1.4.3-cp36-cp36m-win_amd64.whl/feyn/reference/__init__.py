"""
This model contains reference models that can be used for comparison with feyn Graphs.
"""
import numpy as np
import typing
import feyn

from .._graphmixin import GraphMetricsMixin

class ConstantModel(GraphMetricsMixin):
    def __init__(self, graph, const):
        self.const = const
        self.target = graph[-1].name

    def predict(self, data: typing.Iterable):
        return np.full(len(data), self.const)

class LogisticRegressionModel(GraphMetricsMixin):
    def __init__(self, graph, data):
        import sklearn.linear_model

        self.target = graph[-1].name
        self.features = graph.features

        self._lr = sklearn.linear_model.LogisticRegression(penalty="none")
        self._lr.fit(X=data[self.features],y=data[self.target])

    def predict(self, data: typing.Iterable):
        pred = self._lr.predict_proba(data[self.features])[:,1]
        return pred

class LinearRegressionModel(GraphMetricsMixin):
    def __init__(self, graph, data):
        import sklearn.linear_model

        self.target = graph[-1].name
        self.features = graph.features

        self._linreg = sklearn.linear_model.LinearRegression()
        self._linreg.fit(X=data[self.features],y=data[self.target])

    def predict(self, data: typing.Iterable):
        pred = self._linreg.predict(data[self.features])
        return pred
