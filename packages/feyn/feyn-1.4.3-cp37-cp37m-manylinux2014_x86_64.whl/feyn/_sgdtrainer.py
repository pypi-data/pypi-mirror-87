import numpy as np
import itertools
import threading
from typing import Callable, Union, Optional

import _feyn
import feyn

FittingShowType = Union[str, Callable[[feyn.Graph, float], None]]


class SGDTrainer:
    def __init__(self):
        pass

    def _update_display(self, qgraph, current_ix, best_ix, show):
        if best_ix is None:
            print(f"No graphs successfully fitted yet that satisfies criteria (have you tried relaxing your filters?), Graphs tried: {len(qgraph)}")
            return

        pct = (current_ix+1)*100//len(qgraph)
        status = "Fitting %i: %i%% completed. Best loss so far: %.6f" % (qgraph.fit_count, pct, qgraph[best_ix].loss_value)

        if show == "graph":
            import IPython
            svgdata = feyn._current_renderer.rendergraph(qgraph[best_ix], status)
            IPython.display.clear_output(wait=True)
            IPython.display.display(IPython.display.HTML(svgdata))

        elif show == "text":
            print(status)
        elif callable(show):
            show(qgraph[best_ix], qgraph[best_ix].loss_value)
        elif show is None:
            pass
        else:
            raise Exception("show must be either None, 'graph' or 'text', or a callback function")

    def fit(self, qgraph, data, n_samples:Optional[int]=10000, loss_function=_feyn.DEFAULT_LOSS,
                show:Optional[FittingShowType]="graph", threads:int=1, sample_weights=None) -> "QGraph":
        """
        Fit the `QGraph` with given data set.

        Arguments:
            qgraph -- The qgraph to fit
            data -- Training data including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            n_samples -- Number of samples to fit on. The samples will be taken from `data`, possibly over or undersampling the data. None means every sample in the dataset or 10000 samples, whichever is larger.
            loss_function -- Name of the loss function or the function itself. This is the loss function to use for fitting. Can either be a string or one of the functions provided in `feyn.losses`.
            show -- Controls status display. If specified, it should be either "graph", "text", or a user-defined callback function which recieves the best graph found so far, along with it's loss.
            threads -- Number of concurrent threads to use for fitting. Choose this number to match the number of CPU cores on your machine.
            sample_weights -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, ie. one weight for each sample

        Returns:
            QGraph -- The fitted QGraph.
        """

        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        length = len(next(iter(data.values())))

        if n_samples is None:
            n_samples = max(10000, length)

        # Create a sequence of indices from the permutated data of length n_samples
        permutation = np.resize(np.random.permutation(length), (n_samples,))

        data = {key: values[permutation] for key, values in data.items()}

        if sample_weights is not None:
            s_size = len(sample_weights)
            if not s_size == length:
                raise ValueError(f"The sizes of data ({length}) and the sample weights ({s_size}) do not match.")

            # Also permutate the sample_weights
            sample_weights = sample_weights[permutation]

        loss_function = feyn.losses._get_loss_function(loss_function)
        if not hasattr(loss_function, "c_derivative"):
            raise ValueError("Loss function cannot be used for fitting, since it doesn't have a corresponding c derivative")

        _best_ix = None
        _current_ix = 0
        _counter = itertools.count()
        _terminate = False
        _exception: BaseException = None

        def fitting_thread():
            nonlocal _terminate, _best_ix, _current_ix, _counter, _exception, self
            try:
                while not _terminate:
                    ix = next(_counter)
                    if ix >= len(qgraph):
                        return
                    _current_ix = ix
                    g = qgraph[ix]
                    g._fit(data, loss_function=loss_function, sample_weights=sample_weights)

                    if not np.isfinite(g.loss_value):
                        # Graph not defined in its entire domain. Ignore it
                        continue

                    if _best_ix == None or g.loss_value < qgraph[_best_ix].loss_value:
                        _best_ix = ix
            except BaseException as e:
                _exception = e

        threadlist = [threading.Thread(target=fitting_thread) for _ in range(threads)]

        try:
            [t.start() for t in threadlist]
            while True in [t.is_alive() for t in threadlist]:
                [t.join(0.5/threads) for t in threadlist]
                if _exception:
                    raise _exception
                self._update_display(qgraph, _current_ix, _best_ix, show)
        finally:
            _terminate=True
            [t.join() for t in threadlist]
        if _exception:
            raise _exception

        # Remove any graphs that dont work fo the input domain
        qgraph._graphs = list(filter(lambda g: np.isfinite(g.loss_value), qgraph._graphs))

        qgraph._graphs.sort(key=lambda g: g.loss_value, reverse=False)
        return qgraph


    def sort(self, qgraph, data, loss_function=_feyn.DEFAULT_LOSS, threads:int=1, sample_weights=None) -> "QGraph":
        """
        Sort the `QGraph` with given data set.

        Arguments:
            qgraph -- The qgraph to sort
            data -- Training data including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            loss_function -- Name of the loss function or the function itself. This is the loss function to use for sorting. Can either be a string or one of the functions provided in `feyn.losses`.
            threads -- Number of concurrent threads to use for fitting. Choose this number to match the number of CPU cores on your machine.
            sample_weights -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, ie. one weight for each sample
        """
        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        loss_function = feyn.losses._get_loss_function(loss_function)

        _counter = itertools.count()
        _terminate = False
        _exception: BaseException = None

        def sort_thread():
            nonlocal _terminate, _counter, _exception, self
            try:
                while not _terminate:
                    ix = next(_counter)
                    if ix >= len(qgraph):
                        return

                    g = qgraph[ix]
                    out_reg = g[-1]
                    losses = loss_function(data[out_reg.name], g.predict(data))
                    if sample_weights is not None:
                        losses *= sample_weights
                    g.loss_value = np.mean(losses)
            except BaseException as e:
                _exception = e

        threadlist = [threading.Thread(target=sort_thread) for _ in range(threads)]

        try:
            [t.start() for t in threadlist]
            while True in [t.is_alive() for t in threadlist]:
                [t.join(1/threads) for t in threadlist]
                if _exception:
                    raise _exception
        finally:
            _terminate=True
            [t.join() for t in threadlist]
        if _exception:
            raise _exception

        qgraph._graphs.sort(key=lambda g: g.loss_value, reverse=False)
        return qgraph
