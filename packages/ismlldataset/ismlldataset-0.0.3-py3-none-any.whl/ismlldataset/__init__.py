"""
The OpenML module implements a python interface to
`OpenML <https://www.openml.org>`_, a collaborative platform for machine
learning. OpenML can be used to

* store, download and analyze datasets
* make experiments and their results (e.g. models, predictions)
  accesible and reproducible for everybody
* analyze experiments (uploaded by you and other collaborators) and conduct
  meta studies

In particular, this module implements a python interface for the
`OpenML REST API <https://www.openml.org/guide#!rest_services>`_
(`REST on wikipedia
<http://en.wikipedia.org/wiki/Representational_state_transfer>`_).
"""

from . import config
from .datasets import ISMLLDataset
from . import datasets
from . import tasks
from . import utils


from .__version__ import __version__


def populate_cache(task_ids=None, dataset_ids=None, flow_ids=None,
                   run_ids=None):
    """
    Populate a cache for offline and parallel usage of the OpenML connector.

    Parameters
    ----------
    task_ids : iterable

    dataset_ids : iterable

    flow_ids : iterable

    run_ids : iterable

    Returns
    -------
    None
    """
    if dataset_ids is not None:
        for dataset_id in dataset_ids:
            datasets.functions.get_dataset(dataset_id)


__all__ = [
    'OpenMLDataset',
    'utils',
    '__version__',
]

# Load the scikit-learn extension by default
import sklearn  # noqa: F401
