"""Item to be validated."""


class Item:
    """Item to be validated."""

    @classmethod
    def from_record(cls, record):
        """
        Create a new Item from a dictionary of attributes.

        :param record: Dictionary to marshall into an Item.
        """
        p = Item()
        for key, value in record.items():
            setattr(p, key, value)
        return p
