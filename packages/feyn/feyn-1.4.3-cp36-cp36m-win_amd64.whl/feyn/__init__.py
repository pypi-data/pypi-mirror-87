"""Feyn is the main Python module to build and execute models that utilizes a QLattice.

A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction. The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communcate with, extract models from, and update the QLattice.

The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

The workflow is typically:

# Connect to the QLattice
>>> ql = feyn.QLattice()

# Extract a Regression QGraph
>>> qgraph = gl.get_regressor(data.columns, output="out")

# Fit the QGraph to a local dataset
>>> qgraph.fit(data)

# Pick the best Graph from the QGraph
>>> graph = qgraph[0]

# Possibly update the QLattice with the graph to make the QLattice better at this kind of model in the future
>>> ql.update(graph)

# Or use the graph to make predictions
>>> predicted_y = graph.predict(new_data)
"""
import pkg_resources  # part of setuptools
from _feyn import Interaction
from ._svgrenderer import SVGRenderer
from ._graph import Graph
from ._sgdtrainer import SGDTrainer
from ._qgraph import QGraph

from ._snapshots import SnapshotCollection, Snapshot
from ._qlattice import QLattice
from ._register import Register

from . import tools
from . import losses
from . import filters
from . import metrics
from . import plots
from . import reference

_current_renderer = SVGRenderer

__all__ = ['QLattice', 'QGraph', 'Graph', 'Interaction', 'SnapshotCollection', 'Snapshot']

__version__ = pkg_resources.require("feyn")[0].version
