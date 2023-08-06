import pytest

import pandas as pd

from .. import utilities

from chris.datasets import fetch_projects
from chris.datasets.datasets import Datasets
from chris.datasets.dataset_formats import DatasetFormats
from chris.datasets.fetch import fetch_dataset


class TestFetch:
    @pytest.mark.parametrize('dataset_info', utilities.get_public_class_members(Datasets))
    def test_fetch_all(self, dataset_info):
        dataset = fetch_dataset(dataset_info)
        self.validate_data(dataset, dataset_info)

    def validate_data(self, dataset, dataset_info):
        if dataset_info is None:
            assert dataset is not None
        else:
            if dataset_info.data_format == DatasetFormats.JSON:
                assert isinstance(dataset, list)
            elif dataset_info.data_format == DatasetFormats.CSV:
                assert isinstance(dataset, pd.DataFrame)

    def test_fetch_projects(self):
        data = fetch_projects()
        self.validate_data(data, None)
