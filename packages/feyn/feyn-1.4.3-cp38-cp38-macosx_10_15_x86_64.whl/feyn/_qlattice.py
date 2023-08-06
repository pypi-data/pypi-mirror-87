import typing
import warnings
from typing import Dict, List
from urllib.parse import urlparse

import _feyn
import feyn
from feyn import Graph, QGraph, SnapshotCollection

from ._config import Config, resolve_config, resolve_config_failed_message
from ._httpclient import HttpClient
from ._register import RegisterCollection


class QLattice:
    """
    A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction.

    The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

    The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communicate with, extract models from, and update the QLattice.

    Most interactions with the QLattice takes place through the QGraph object which represents an infinite list of graphs (or models) for a specific problem.

    So, while a QLattice is able to generate any graph linking any input to any output, a QGraph merely contains the graphs that relate a specified set of inputs to a specified output.

    The workflow is typically:
    1) extract a QGraph from the QLattice using `QLattice.get_regressor` or `QLattice.get_classifier`.
    2) fit the QGraph to a local dataset using `QGraph.fit`.
    3) choose one or more models from the QGraph using `QGraph[index]`.
    4) potentially update the QLattice with new knowledge using `QLattice.update`.

    Arguments:
        url -- URL of your QLattice. (Should not to be used in combination with the config parameter).
        api_token -- Authentication token for the communicating with this QLattice. (Should not to be used in combination with the config parameter).
        config -- The configuration setting in your feyn.ini or .feynrc file to load the url and api_token from. These files should be located in your home folder.
    """
    def __init__(self, url: str=None, api_token: str=None, config: str=None):
        """Construct a new 'QLattice' object."""

        if config:
            if url or api_token:
                raise ValueError("Must specify either a config or url and token.")
        else:
            if not url and api_token:
                raise ValueError("Must specify either a config or url and token.")

        if url:
            if not _is_url(url):
                raise ValueError(f"Value [{url}] for param `url` is not a valid url. Did you mean to specify `config` instead?")

            cfg = Config(url, api_token)
        else:
            cfg = resolve_config(config)

            if cfg is None:
                raise ValueError(resolve_config_failed_message)

        self.url = cfg.url + "/api/v1/qlattice"

        headers = {
            'Authorization': f'Bearer {cfg.api_token or "none"}',
            'User-Agent': f"feyn/{feyn.__version__}"
        }

        self._http_client = HttpClient(self.url, headers)

        self._load_qlattice()

        self._snapshots = SnapshotCollection(self)
        self._registers = RegisterCollection(self)

    def get_qgraph(self, registers: List[str], output: str, stypes: Dict[str,str]={}, max_depth: int = 5) -> "QGraph":
        """
        Deprecated function to extract a QGraph. Use one of the following instead:
        * qlattice.get_classifier
        * qlattice.get_regressor
        """
        warnings.warn("The function get_qgraph is deprecated. Use either get_regressor or get_classifier", DeprecationWarning, stacklevel=2)

        return self._get_qgraph(registers, output, stypes, max_depth)


    def get_classifier(self, registers: List[str], output: str, stypes: Dict[str,str]={}, max_depth: int = 4, specs=None) -> "QGraph":
        """
        Extract QGraph classifier from inputs registers to an output register.

        Use this function to extract a QGraph for binary classification. Once the QGraph has been extracted from the QLattice, you'll typically use the `QGraph.fit()` function to fit the QGraph to an actual dataset.

        Arguments:
            registers -- List of register names to use in the QGraph.
            output -- The output register name.
            stypes -- An optional map from register names to semantic types.
            max_depth -- The maximum depth of the graphs.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """

        stypes[output]="b"
        return self._get_qgraph(registers, output, stypes, max_depth)

    def get_regressor(self, registers: List[str], output: str, stypes: Dict[str,str]={}, max_depth: int = 5) -> "QGraph":
        """
        Extract QGraph regressor from inputs registers to an output register.

        Use this function to extract a QGraph for regression (continuous output values). Once the QGraph has been extracted from the QLattice, you'll typically use the `QGraph.fit()` function to fit the QGraph to an actual dataset.

        Arguments:
            registers -- List of register names to use in the QGraph.
            output -- The output register name.
            stypes -- An optional map from register names to semantic types.
            max_depth -- The maximum depth of the graphs.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """
        stypes[output]="f"
        return self._get_qgraph(registers, output, stypes, max_depth)


    def _get_qgraph(self, registers: List[str], output: str, stypes: Dict[str,str]={}, max_depth: int = 5) -> "QGraph":
        """
        Extract QGraph from inputs registers to an output register.

        The standard workflow for QLattices is to extract a QGraph using this function. You specify a list of input registers corresponding to the input values you want to use for predictions, and a single output register corresponding to the output variable you want to predict.

        Once the QGraph has been extracted from the QLattice, you'll typically use the `QGraph.fit()` function to fit the QGraph to an actual dataset.

        Arguments:
            registers -- List of register names to use in the QGraph.
            output -- The output register name.
            stypes -- An optional map from register names to semantic types.
            max_depth -- The maximum depth of the graphs.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """

        if output not in registers:
            registers = registers.copy()
            registers.append(output)

        if len(registers)<2:
            raise Exception("A QGraph must have at least one input register")

        regmap = {}
        for reg in registers:
            stype = stypes.get(reg, "f")

            if stype in ("cat", "categorical"):
                stype = "c"
            if stype in ("float", "numerical"):
                stype = "f"

            if reg == output:
                pattern = f"out:*(*)->{stype}"
            else:
                pattern = f"in:*({stype})->*"

            regmap[reg] = pattern

        res = QGraph(self, regmap)
        res = res.filter(feyn.filters.MaxDepth(max_depth))

        res._refresh()

        return res

    def _generate(self, specs: List[str], registers: Dict[str, str], max_depth) -> Dict:
        req = self._http_client.post("/generate",
                                    json={
                                        'specs': specs,
                                        'registers': registers,
                                        'max_depth': max_depth
                                    })

        if req.status_code == 422:
            raise ValueError(req.text)

        req.raise_for_status()

        return req.json()

    def update(self, graphs: typing.Union[Graph, typing.Iterable[Graph]]) -> None:
        """
        Update QLattice with learnings from a `Graph`.

        When updated, the QLattice learns to produce better QGraphs. This is how a QLattice evolves and narrows in on producing QGraphs with better and better models.

        Without updating, the QLattice will not learn about good models and the QGraphs produced from the QLattice will not contain better models.

        # Pick the best Graph from the QGraph and update the QLattice with it's learnings
        >>> graph = qgraph[0]
        >>> ql.update(graph)

        Arguments:
            graphs -- Graph or list of Graphs with learnings worth storing.
        """
        if isinstance(graphs, QGraph):
            raise ValueError("Hi there friend! I am expecting a single `Graph` with learnings that you deem worth teaching me.\
                              You seem to have passed in an entire QGraph. I have no way to figure out which parts I should learn from in it.")

        if isinstance(graphs, Graph):
            graphs = [graphs]

        for graph in graphs:
            req = self._http_client.post("/update", json=graph._to_dict())
            req.raise_for_status()

    @property
    def snapshots(self):
        """
        Collection of snapshots for this QLattice

        Use this collection to capture, list and restore the complete state of a QLattice.
        """
        return self._snapshots

    @property
    def registers(self):
        """
        The RegisterCollection of the QLattice

        The RegisterCollection is used to find, create and remove registers from the QLattice.
        """
        return self._registers

    def reset(self) -> None:
        """
        Clear all learnings in this QLattice.

        This is a potentially dangerous action. Think twice before calling this method.
        """
        req = self._http_client.post("/reset")
        req.raise_for_status()

        self._load_qlattice()

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (self.width, self.height, self.url)

    def _load_qlattice(self):
        req = self._http_client.get("/")

        # The purpose of this special handling is to create a channel for messaging the user about issues that we have somehow
        # failed to consider beforehand.
        if req.status_code == 400:
            raise ConnectionError(req.text)

        req.raise_for_status()

        qlattice = req.json()

        self.width = qlattice['width']
        self.height = qlattice['height']


def _is_url(maybe_url):
    try:
        result = urlparse(maybe_url)
        return all([result.scheme, result.netloc])
    except:
        return False
