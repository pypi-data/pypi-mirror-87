"""Validator base class."""
import json
import pathlib

from typing import Any, Dict, List

from chris.validation.item import Item


class Validator:
    """Validator base class."""

    DATA_DIR_PATH = pathlib.Path(__file__).parent.absolute() / '..' / 'datasets' / 'data'

    @classmethod
    def load_items(cls,
                   data_filename: str) -> List[Dict[str, Any]]:
        """
        Load items to validate from a file.

        :data_filename: Filename of data.
        """
        data_filepath = cls.DATA_DIR_PATH / data_filename
        with open(data_filepath, 'r') as f:
            item_records = json.load(f)
        return [Item.from_record(record) for record in item_records]
