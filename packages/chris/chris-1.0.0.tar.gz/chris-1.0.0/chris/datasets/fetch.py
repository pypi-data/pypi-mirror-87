"""Dataset fetching convenience functions."""
import json

import pandas as pd

from pathlib import Path

from chris.datasets.datasets import Datasets
from chris.datasets.dataset_formats import DatasetFormats
from chris.datasets.dataset_info import DatasetInfo
from chris.datasets.type_aliases import DatasetType


DATA_DIR = Path(__file__).parent.absolute() / 'data'


def fetch_dataset(dataset_info: DatasetInfo) -> DatasetType:
    """
    Fetch a dataset.

    :param dataset_info: DatasetInfo dataset metadata object.
    """
    dataset_path = DATA_DIR / dataset_info.data_path
    if dataset_info.data_format == DatasetFormats.JSON:
        with open(dataset_path, 'r') as f:
            data = json.load(f)
    elif dataset_info.data_format == DatasetFormats.CSV:
        data = pd.read_csv(dataset_path)
    return data


def fetch_projects() -> DatasetType:
    """Fetch the projects dataset."""
    return fetch_dataset(Datasets.PROJECTS)
