import pytest
import re

from .. import utilities

from chris.datasets.dataset_formats import DatasetFormats


class TestDatasetFormats:

    @pytest.mark.parametrize('dataset_format', utilities.get_public_class_members(DatasetFormats))
    def test_dataset_format_formats(self, dataset_format):
        message = f"Invalid dataset format \"{dataset_format}\""
        assert re.match(r'[a-z]{1,10}', dataset_format), message
