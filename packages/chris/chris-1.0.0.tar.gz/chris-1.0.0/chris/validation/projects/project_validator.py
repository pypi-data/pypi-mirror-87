"""Validator for projects."""
import re

from chris.validation.projects.project_properties import ProjectProperties
from chris.validation.validation_results import ValidationResults
from chris.validation.validator import Validator


class ProjectValidator(Validator):
    """Validator for projects."""

    DATA_FILENAME = 'projects/projects.json'

    MIN_DESCRIPTION_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 1200
    MIN_LINK_LENGTH = 5

    @classmethod
    def validate(cls):
        """Validate projects."""
        items = cls.load_items(cls.DATA_FILENAME)
        n_items = len(items)
        results = ValidationResults(n_items, 'project')

        seen_names = set()
        seen_project_types = set()
        # seen_source_links = set()
        # seen_download_links = set()

        for item in items:
            for field in ProjectProperties.FIELDS:
                if not hasattr(item, field):
                    results.add_error(f"Project \"{item.name}\" is missing field \"{field}\"")

            if not re.fullmatch(r'[a-z0-9-]{36}', item.project_id):
                results.add_error(f"Invalid project_id format \"{item.project_id}\"")

            if item.name in seen_names:
                results.add_error(f"Duplicate name \"{item.name}\"")
            seen_names.add(item.name)

            # if item.source_link is not None and item.source_link in seen_source_links:
            #     results.add_error(f"Duplicate source_link \"{item.source_link}\"")
            # seen_source_links.add(item.source_link)

            # if item.download_link is not None and item.download_link in seen_download_links:
            #     results.add_error(f"Duplicate download_link \"{item.download_link}\"")
            # seen_download_links.add(item.download_link)

            if item.project_type is not None:
                if item.project_type not in ProjectProperties.PROJECT_TYPES:
                    results.add_error(f"Unknown project_type \"{item.project_type}\" for \"{item.name}\"")
                seen_project_types.add(item.project_type)

            if item.date is None:
                results.add_error(f"Project \"{item.name}\" is missing the required \"date\" field")
            else:
                if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', item.date):
                    results.add_error(f"Invalid date format \"{item.date}\"")

            if item.source_link is not None:
                if not len(item.source_link) > cls.MIN_LINK_LENGTH:
                    results.add_error(f"Invalid source_link length \"{item.source_link}\" for \"{item.name}\"")

            if item.download_link is not None:
                if not len(item.download_link) > cls.MIN_LINK_LENGTH:
                    results.add_error(f"Invalid download_link length \"{item.download_link}\" for \"{item.name}\"")

            if item.description is not None:
                description_length = len(item.description)
                if description_length < cls.MIN_DESCRIPTION_LENGTH:
                    results.add_error(f"Description length ({description_length}) for \"{item.name}\" "
                                      f"is less than {cls.MIN_DESCRIPTION_LENGTH}")

                if description_length > cls.MAX_DESCRIPTION_LENGTH:
                    results.add_error(f"Description length ({description_length}) for \"{item.name}\" "
                                      f"is more than {cls.MAX_DESCRIPTION_LENGTH}")

                results.add_completed('description')

        # Validate unused

        seen_known_map = [
            ('project_type', seen_project_types, ProjectProperties.PROJECT_TYPES),
        ]

        for field, seen_set, known_set in seen_known_map:
            for value in known_set:
                if value not in seen_set:
                    results.add_error(f"Unused {field} \"{value}\"")

        # Validate constants

        for project_type in ProjectProperties.PROJECT_TYPES:
            if not re.fullmatch(r'[a-z]+', project_type):
                results.add_error(f"Invalid project_type format \"{project_type}\"")

        for field, _, known_set in seen_known_map:
            last_value = None
            for value in known_set:
                if last_value is not None and value.lower() <= last_value.lower():
                    results.add_error(f"Unordered constants for {field}: \"{last_value}\" vs \"{value}\"")
                last_value = value

        return results


def validate():
    """Run validation for projects."""
    validator = ProjectValidator()
    results = validator.validate()
    results.print()


if __name__ == '__main__':
    validate()
