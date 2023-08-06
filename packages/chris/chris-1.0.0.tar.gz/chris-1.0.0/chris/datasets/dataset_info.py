"""Dataset metadata."""


class DatasetInfo:
    """Dataset metadata."""

    def __init__(self,
                 name: str,
                 data_path: str,
                 data_format: str,
                 description: str) -> None:
        """
        Construct a DatasetInfo.

        :param name: Name of the dataset.
        :param data_path: Relative path to the dataset.
        :param data_format: Format of the dataset.
        :param description: Description of the dataset.
        """
        self.name = name
        self.data_path = data_path
        self.data_format = data_format
        self.description = description

    def __str__(self) -> str:
        """Get the string representation of the dataset DatasetInfo."""
        return f"Dataset(name=\"{self.name}\")"
