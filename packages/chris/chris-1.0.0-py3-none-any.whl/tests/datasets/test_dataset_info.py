from chris.datasets.dataset_info import DatasetInfo
from chris.datasets.dataset_formats import DatasetFormats


class TestDatasetInfo:

    def test_get_dataset_info_attributes(self):
        name = 'Dataset Name'
        data_path = 'folder/dataset-path.csv'
        data_format = DatasetFormats.CSV
        description = "Test dataset."

        info = DatasetInfo(name, data_path, data_format, description)

        assert info.name == name
        assert info.data_path == data_path
        assert info.data_format == data_format
        assert info.description == description
