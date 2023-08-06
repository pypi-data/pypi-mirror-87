"""Properties of posts."""


class PostProperties:
    """Properties of posts."""

    # region field-names

    FIELDS = [
        'post_id',
        'title',
        'content_type',
        'length',
        'source',
        'areas',
        'series',
        'speaker',
        'episode_number',
        'date_created',
        'date_posted',
        'link',
        'tags',
        'summary',
        'archived',
    ]

    # endregion field-names

    # region field-values

    AREAS = [
        'art',
        'biology',
        'business',
        'comedy',
        'complexity',
        'computers',
        'engineering',
        'justice',
        'law',
        'logic',
        'mathematics',
        'medicine',
        'music',
        'neuroscience',
        'philosophy',
        'physics',
        'politics',
        'psychology',
        'technology',
    ]

    CONTENT_TYPES = [
        'article',
        'audio',
        'paper',
        'video',
    ]

    SERIES = [
        '3Blue1Brown',
        'Adam Neely',
        'Aeon Essays',
        'Andrew Huang',
        'Big Think',
        'CGP Grey',
        'Charles Cornell',
        'CollegeHumor',
        'Domain of Science',
        'Future Thinkers',
        'Jack Conte',
        'Joe Rogan Experience',
        'Jordan Greenhall',
        'Lex Fridman Podcast',
        'Making Sense',
        'minutephysics',
        'New Economic Thinking',
        'Numberphile',
        'Oz Talk',
        'Paradigms',
        'Paul Collider',
        'Sixty Symbols',
        'Smarter Every Day',
        'Steve Mould',
        'TED',
        'TED Ed',
        'The Portal',
        'The Royal Institution',
        'This American Life',
        'Veritasium',
        'VICE',
        'WIRED',
    ]

    SOURCES = [
        'Aeon',
        'BuzzFeed News',
        'Daily Motion',
        'Frontiers in Human Neuroscience',
        'Microsoft',
        'Sam Harris',
        'Technology Review',
        'TED',
        'This American Life',
        'Vimeo',
        'Vox',
        'WIRED',
        'YouTube',
    ]

    # endregion field-values
