from typing import Union, Iterable, Optional

import numpy as np

import _feyn
import feyn


class GraphMetricsMixin:
    def squared_error(self, data:Iterable):
        """
        Compute the graph's squared error loss on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.squared_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.squared_error(data[self.target], pred)

    def absolute_error(self, data:Iterable):
        """
        Compute the graph's absolute error on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.absolute_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.absolute_error(data[self.target], pred)

    def binary_cross_entropy(self, data:Iterable):
        """
        Compute the graph's binary cross entropy on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = graph.predict(data)
        > se = feyn.losses.binary_cross_entropy(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.binary_cross_entropy(data[self.target], pred)

    def accuracy_score(self, data: Iterable):
        """
        Compute the graph's accuracy score on a data set

        The accuracy score is useful to evaluate classification graphs. It is the fraction of the preditions that are correct. Formally it is defned as

        (number of correct predictions) / (total number of preditions)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            accuracy score for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.accuracy_score(data[self.target], pred)

    def accuracy_threshold(self, data: Iterable):
        """
        Compute the accuracy score of predictions with optimal threshold

        The accuracy score is useful to evaluate classification graphs. It is the fraction of the preditions that are correct. Accuracy is normally calculated under the assumption that the threshold that separates true from false is 0.5. Hovever, this is not the case when a model was trained with another population composition than on the one which is used.

        This function first computes the threshold limining true from false classes that optimises the accuracy. It then returns this threshold along with the accuracy that is obtained using it.

        Arguments:
            true -- Expected values
            pred -- Predicted values

        Returns a tuple with:
            threshold that maximizes accuracy
            accuracy score obtained with this threshold

        """
        pred = self.predict(data)
        return feyn.metrics.accuracy_threshold(data[self.target], pred)


    def r2_score(self, data: Iterable):
        """
        Compute the graph's r2 score on a data set

        The r2 score for a regression model is defined as 
        1 - rss/tss

        Where rss is the residual sum of squares for the predictions, and tss is the total sum of squares.
        Intutively, the tss is the resuduals of a so-called "worst" model that always predicts the mean. Therefore, the r2 score expresses how much better the predictions are than such a model.

        A result of 0 means that the model is no better than a model that always predicts the mean value
        A result of 1 means that the model perfectly predicts the true value

        It is possible to get r2 scores below 0 if the predictions are even worse than the mean model.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            r2 score for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.r2_score(data[self.target], pred)

    def mae(self, data):
        """
        Compute the graph's mean absolute error on a data set

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            MAE for the predictions
        """ 
        pred = self.predict(data)
        return feyn.metrics.mae(data[self.target], pred)


    def mse(self, data):
        """
        Compute the graph's mean squared error on a data set

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            MSE for the predictions
        """ 
        pred = self.predict(data)
        return feyn.metrics.mse(data[self.target], pred)


    def rmse(self, data):
        """
        Compute the graph's root mean squared error on a data set

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            RMSE for the predictions
        """ 
        pred = self.predict(data)
        return feyn.metrics.rmse(data[self.target], pred)


    def plot_confusion_matrix(self,
                            data: Iterable,
                            labels: Iterable=None,
                            title:str='Confusion matrix',
                            color_map="abzu-partial",
                            ax=None) -> None:

        """
        Compute and plot a Confusion Matrix.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            labels -- List of labels to index the matrix
            title -- Title of the plot.
            color_map -- Color map from matplotlib to use for the matrix
            ax -- matplotlib axes object to draw to, default None
        Returns:
            [plot] -- matplotlib confusion matrix
        """
        pred = self.predict(data).round()
        feyn.plots.plot_confusion_matrix(data[self.target], pred, labels, title, color_map, ax)


    def plot_regression_metrics(self, data: Iterable, title:str="Regression metrics", ax=None ) -> None:
        """
        Plot the graph's metrics for a regression.

        This is a shorthand for calling feyn.plots.plot_regression_metrics.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to, default None

        """
        pred = self.predict(data)
        feyn.plots.plot_regression_metrics(data[self.target], pred, title, ax)


    def plot_segmented_loss(self, data:Iterable, by:Optional[str] = None, loss_function="squared_error", title="Segmented Loss", ax=None) -> None:
        """
        Plot the loss by segment of a dataset.

        This plot is useful to evaluate how a model performs on different subsets of the data.

        Example:
        > qg = qlattice.get_regressor(["age","smoker","heartrate"], output="heartrate")
        > qg.fit(data)
        > best = qg[0]
        > feyn.plots.plot_segmented_loss(best, data, by="smoker")

        This will plot a histogram of the model loss for smokers and non-smokers separately, which can help evaluate wheter the model has better performance for euther of the smoker sub-populations.

        You can use any column in the dataset as the `by` parameter. If you use a numerical column, the data will be binned automatically.

        Arguments:
            data -- The dataset to measure the loss on.
            by -- The column in the dataset to segment by.
            loss_function -- The loss function to compute for each segmnent,
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to
        """

        feyn.plots.plot_segmented_loss(self, data, by=by, loss_function=loss_function, title=title, ax=ax)

    def plot_roc_curve(self, data: Iterable, title:str="ROC curve", ax=None, **kwargs) -> None:
        """
        Plot the graph's ROC curve.

        This is a shorthand for calling feyn.plots.plot_roc_curve.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to, default None
            **kwargs -- additional options to pass on to matplotlib    
        """
        pred = self.predict(data)
        feyn.plots.plot_roc_curve(data[self.target], pred, title, ax, **kwargs)


