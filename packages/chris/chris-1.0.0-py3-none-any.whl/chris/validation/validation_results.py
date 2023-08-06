"""Results of validation."""
from tabulate import tabulate
from chris.validation.color_printing import print_rgb, Color


class ValidationResults:
    """Results of validation."""

    def __init__(self, n_items: int, item_type: str):
        """
        Construct a ValidationResults.

        :param n_items: Number of items being validated.
        :param item_type: The type of item being validated.
        """
        self._n_items = n_items
        self._item_type = item_type
        self._errors = []
        self._completed = {}

    def add_error(self, message: str) -> None:
        """
        Add an error message to the validation results.

        :param message: Message to add.
        """
        self._errors.append(message)

    def add_completed(self, field: str, count: int = 1) -> None:
        """
        Register that a field has been completed for one (or more) item(s).

        :param field: Name of the field to mark as completed.
        :param count: Number of fields to mark completed.
        """
        if field not in self._completed:
            self._completed[field] = 0
        self._completed[field] += count

    def print(self):
        """Print the validation results to stdout."""
        print(f"Validated items of type: {self._item_type}")
        n_errors = len(self._errors)
        if n_errors == 0:
            print_rgb(f"Successfully validated {self._n_items} items", Color.GREEN)
            completed_counts = self._completed.values()
            completed_percents = [v / self._n_items for v in completed_counts]
            completed_table = {
                'Field': self._completed.keys(),
                'Percent Completed': completed_percents,
                'Number Completed': completed_counts,
            }
            print()
            print(tabulate(completed_table, headers='keys', tablefmt='github'))
        else:
            print_rgb(f"Found {n_errors} errors while validating:", Color.RED)
            for error in self._errors:
                print(f"- {error}")
        print()

    def has_errors(self):
        """Get whether the results have any errors."""
        return len(self.errors) > 0

    def get_errors(self):
        """Get the list of error messages found during validation."""
        return self.errors
