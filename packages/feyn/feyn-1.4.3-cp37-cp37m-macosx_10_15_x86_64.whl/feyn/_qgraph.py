from typing import Callable, Dict, Iterator, Iterable, List, Optional, Set, Union

import numpy as np

import _feyn
import feyn.filters
import feyn.losses
from feyn import Graph, SGDTrainer
from feyn.metrics import get_pearson_correlations

FittingShowType = Union[str, Callable[[Graph, float], None]]

def _dist1_mod(a,b,modulo):
        d = abs(b-a)%modulo
        return min(d,modulo-d)

def _add_strengths(graphs:Union[Graph, List[Graph]], data):

    # Always work with a list of graphs
    if isinstance(graphs, Graph):
        graphs = [graphs]

    for graph in graphs:
        signals = get_pearson_correlations(graph, data)
        for node, signal in enumerate(signals):
            graph[node]._strength = np.abs(signal)

    return graphs

class QGraph:
    """
    A QGraph is extracted from the QLattice with the `QLattice.get_regressor()` or the `QLattice.get_classifier` method. It represents infinite list of graphs linking a set of input registers to an output register.

    One way to think about a QGraph is as a partially ordered list of all possible graphs complying with some constraints. The head of the list contains the best graphs found for solving a problem at any given time.

    A QGraph can be gradually sorted by fitting it to one or more datasets. Fitting is done using one of two methods, the `fit` method which searches further and further into the infinite list for better graphs, and the `sort` method which merely re-sorts the head of the list with new conditions.

    Since the list is infinite, the sorting can never actually finish, but using the QLattice simulator, the QGraph can be extremely smart about how and where in the infinite list to search for better graphs.

    It is possible to limit or constrain which graphs belong in the infinite list in several ways, most importantly using the `filter` method.

    The constructor is for internal use. QGraphs should always be generated with the `QLattice.get_graph` method.

    Arguments:
        graph_dict -- A dictionary containing the QGraph descriptor.
    """
    def __init__(self, qlattice, registers: Dict[str, str]):
        """Construct a new `QGraph` object."""
        self.qlattice = qlattice
        self.registers = registers

        self.graph_count = 0
        self.fit_count = 0

        self._filters = {}

        self._graphs = []

        self.trainer = SGDTrainer()

    def _refresh(self):

        depthfilter = self._filters.get("depth")
        if depthfilter:
            max_depth = depthfilter.depth
        else:
            max_depth = 5

        specfilter = self._filters.get("spec_filter")
        if specfilter:
            specs = specfilter.specs
        else:
            specs = _feyn.get_specs()

        qgraph_json = self.qlattice._generate(specs, self.registers, max_depth)

        new_graphs = self._from_graph_dict(qgraph_json)

        for _, qfilter in self._filters.items():
            new_graphs = list(qfilter(new_graphs))

        self._graphs = sorted(set(self._graphs), key=lambda g: g.loss_value, reverse=False)
        self._graphs += new_graphs

        self.graph_count += len(new_graphs)



    def head(self, n=5):
        """
        Show the first `n` Graphs in the QGraph.

        This only works in an interactive environment like Jupyter Notebook

        Keyword Arguments:
            n {int} -- Number of graphs to show. (default: {5})
        """
        if n>len(self._graphs):
            n = len(self._graphs)
            if n == 0:
                print("<Empty QGraph>")
                return

        import IPython
        for i in range(n):
            IPython.display.display(self._graphs[i])

    def _template(self):
        res = QGraph(self.qlattice, self.registers)
        res._filters = self._filters.copy()

        return res

    def filter(self, qfilter:feyn.filters.QGraphFilter) -> "QGraph":
        """Create a new filtered QGraph which represents all graphs matching the specified filter.

        A QGraph is an infinite list of graphs complying with some constraints. These constraints are specified as filters on the QGraph itself. Notice that when filtering an infinite list, the result is still infinite!

        The search for graphs can be guided or limited by filtering a QGraph on for example depth, the number of edges, or required input features.

        Arguments:
            qfilter {feyn.filters.QGraphFilter} -- The filter to apply.

        Raises:
            ValueError: Raised when the qfilter could not be understood.

        Returns:
            QGraph -- The filtered QGraph
        """
        if not isinstance(qfilter, feyn.filters.QGraphFilter):
            raise ValueError("qfilter must be subtype of feyn.filters.QGraphFilter")

        key = qfilter.key()

        res = self._template()
        res._filters[key] = qfilter
        res._graphs = list(qfilter(self._graphs))
        return res

    def copy(self) -> "QGraph":
        """
        Make a shallow copy of the QGraph.

        Returns:
            QGraph -- The copied QGraph.
        """
        res = self._template()
        res._graphs = self._graphs.copy()
        return res

    def _algo_x(self):
        lim = 2000
        tot = 0

        keep = []
        locs = {}
        hashes = set()
        for g in self._graphs:
            h = hash(g)
            if h in hashes:
                continue

            loc = g[-1]._latticeloc[0]
            cnt = locs.get(loc, 0)

            density = 200
            if cnt >= density:
                continue

            if g.age > 200*np.exp(-cnt/(density/(20*0.693))) + 1:
                # Too old
                continue

            locs[loc]=cnt+1
            keep.append(g)
            hashes.add(h)

            tot+=1
            if tot==lim:
                break

        self._graphs = keep


    def fit(self, data, n_samples:Optional[int]=None, loss_function=_feyn.DEFAULT_LOSS, show:Optional[FittingShowType]="graph", threads:int=1, sample_weights=None) -> "QGraph":
        """
        Fit and sort the `QGraph` with the given data set. After the fitting, the head of the QGraph will be sorted by increasing loss.

        Each call will further explore the infinite list of graphs, and may find better graphs that are then brought forward to their correct sorting order. Sometimes this leads to a new best graph making it to the first position in the list.

        A call to fit() is comparable to an epoch in other frameworks. Every call will potentially lead to a new best graph being found. Since the list is infinite, there is always the possibility that a new superior graph is found, but in practice between 5 and 100 calls are usually sufficient.

        The n_samples parameter controls how much each graph in the QGraph is trained during the process. The default behavior is to train each graph once with each sample in the dataset, unless the set is smaller than 10000, in which case the dataset will be upsampled to 10000 samples before fitting.

        The samples are shuffled randomly before fitting to avoid issues with the Stochastic Gradient Descent algorithm.

        The recommended workflow for fitting a QGraph involves several steps in a loop:
        > for epoch in range(10):
        >     qgraph.fit(train)       # fit the data to the training set
        >     best = qgraph.best()    # get a list of the best performing graphs
        >     qlattice.update(best)   # update the qlattice with the best graphs

        Arguments:
            data -- Training data including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            n_samples -- Number of samples to fit on. The samples will be taken from `data`, possibly over- or undersampling the data. Passing `None` means use every sample in the dataset or 10000 samples, whichever is larger.
            loss_function -- Name of the loss function or the function itself. This is the loss function to use for fitting. Can either be a string or one of the functions provided in `feyn.losses`.
            show -- Controls status display. If specified, it should be either "graph", "text", or a user-defined callback function which receives the best graph found so far, along with it's loss.
            threads -- Number of concurrent threads to use for fitting. Choose this number to match the number of CPU cores on your machine.
            sample_weights -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, i.e. one weight for each sample

        Returns:
            QGraph -- The QGraph itself.
        """
        self._refresh()
        self.fit_count += 1
        self.trainer.fit(self, data, n_samples, loss_function, show, threads, sample_weights)

        for g in self._graphs:
            g.age += 1

        self._algo_x()

        return self

    def sort(self, data, loss_function=_feyn.DEFAULT_LOSS, threads:int=1, sample_weights=None):
        """
        Sort the head of the QGraph by loss of each graph against the provided data set. The difference between QGraph.fit and QGraph.sort is that while the fit function will bring completely new graphs to the head of the QGraph, the sort function will only sort the graphs that are already in the head.

        # Fit and sort a graph from a qgraph
        >>> qgraph.fit(training_data, loss_function=feyn.losses.squared_error)
        >>> qgraph.sort(some_other_data, loss_function=feyn.losses.absolute_error)

        # After this, the first graph in the QGraph will be the best performing graph on "some_other_data"
        >>> best = qgraph[0]

        Arguments:
            data -- The data set to sort by. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            loss_function -- The loss function to use when sorting graphs. Can either be a string or one of the functions provided in `feyn.losses`.
            threads -- Number of concurrent threads to use for sorting. Choose this number to match the number of CPU cores on your machine.
            sample_weights -- An optional numpy array of weights for each sample. If present, the array must have the same size as the data set, i.e. one weight for each sample

        Returns:
            QGraph -- The QGraph itself
        """
        return self.trainer.sort(self, data, loss_function, threads, sample_weights)

    def best(self, n=5, data:Optional[Iterable]=None) -> List[Graph]:
        res = []

        locs = []

        for g in self._graphs:
            x = g[-1]._latticeloc[0]

            too_close = [_dist1_mod(x,other,self.qlattice.width)<4 for other in locs]
            if True in too_close:
                # This graph has an endpoint within 4 x-units from another, better graph
                continue

            locs.append(x)
            res.append(g)
            if len(res)>=n:
                break

        if data is not None:
            return _add_strengths(res, data)
        return res

    def __getitem__(self, key) -> Union["QGraph", Graph]:
        if isinstance(key, slice):
            res = self._template()
            res._graphs = self._graphs[key]
            return res
        else:
            return self._graphs.__getitem__(key)

    def __iter__(self) -> Iterator[Graph]:
        for g in self._graphs:
            yield g

    def __len__(self):
        return self._graphs.__len__()

    def __add__(self, other) -> "QGraph":
        res = self._template()
        res._graphs = self._graphs + other._graphs
        return res

    def __repr__(self):
        if self._filters:
            filterstring = " and ".join("("+repr(f)+")" for f in self._filters.values())
        else:
            filterstring = "<unfiltered>"

        return f"QGraph {filterstring} <head: {self.__len__()}>"

    def _from_graph_dict(self, graph_dict: dict) -> Set[Graph]:
        nodemap = {node["id"]: node for node in graph_dict["nodes"]}

        ## Add the links to the nodes themselves.
        # TODO: Change wire format to avoud this conversion
        for node in nodemap.values():
            node["links"] = [None, None]

        for link in graph_dict["links"]:
            source_id = link["source"]
            target_node = nodemap[link["target"]]
            ord = int(link["ord"])
            target_node["links"][ord] = source_id

        new_graphs = set()

        out_ids = [n["id"] for n in nodemap.values() if n["spec"].startswith("out:")]
        for out_id in out_ids:
            # The following algorithm builds a 1D array of nodes
            # that preserverves execution order
            nodelist = []
            current = [out_id]
            while len(current) > 0:
                node_id = current.pop(0)
                if node_id in nodelist:
                    nodelist.remove(node_id)
                nodelist.insert(0, node_id)

                for pred_id in nodemap[node_id]["links"]:
                    if pred_id is not None:
                        current.append(pred_id)

            # Convert the list of ids to a list of nodes
            nodelist = [nodemap[nodeid] for nodeid in nodelist]
            new_graphs.add(self._build_graph(nodelist))

        return new_graphs

    def _build_graph(self, nodelist: List[Dict]):
        sz = len(nodelist)
        graph = Graph(sz)

        for i, node_json in enumerate(nodelist):

            interaction = Graph._get_interaction(node_json)
            graph[i] = interaction

            if node_json["spec"].startswith("in:"):
                interaction._set_source(0, -1)
                continue

            for ord, src_id in enumerate(node_json["links"]):
                if src_id == None:
                    continue
                source_index = next(ix for ix, n in enumerate(nodelist) if n["id"]==src_id)
                interaction._set_source(ord, source_index)

        graph.strength = graph[-1]._strength
        return graph
