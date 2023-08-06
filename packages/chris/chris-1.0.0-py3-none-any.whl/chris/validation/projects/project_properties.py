"""Properties of projects."""


class ProjectProperties:
    """Properties of projects."""

    # Field Names

    FIELDS = [
        'project_id',
        'name',
        'date',
        'project_type',
        'description',
        'source_link',
        'download_link',
        'image_links',
        'primary_language',
        'archived',
    ]

    # Field values

    PROJECT_TYPES = [
        'jar',
        'program',
        'web',
    ]
