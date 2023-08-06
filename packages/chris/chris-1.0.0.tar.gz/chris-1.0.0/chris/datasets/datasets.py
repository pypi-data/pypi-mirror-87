"""Information for all package datasets."""
from chris.datasets.dataset_formats import DatasetFormats
from chris.datasets.dataset_info import DatasetInfo


class Datasets:
    """Information for all package datasets."""

    # region blog

    PODCAST_EPISODES = DatasetInfo(
        'Podcast Episodes',
        'blog/podcast-episodes.json',
        DatasetFormats.JSON,
        "Podcast episodes.")
    POSTS = DatasetInfo(
        'Posts',
        'blog/posts.json',
        DatasetFormats.JSON,
        "Blog posts.")

    # endregion blog

    # region cooking

    RECIPES = DatasetInfo(
        'Recipes',
        'cooking/recipes.json',
        DatasetFormats.JSON,
        "Cooking recipes.")

    # endregion cooking

    # region media

    MOVIES = DatasetInfo(
        'Movies',
        'media/movies.csv',
        DatasetFormats.CSV,
        "Movies.")
    PODCASTS = DatasetInfo(
        'Podcasts',
        'media/podcasts.csv',
        DatasetFormats.CSV,
        "Podcasts.")
    TV_SHOWS = DatasetInfo(
        'TV Shows',
        'media/tv-shows.csv',
        DatasetFormats.CSV,
        "TV shows.")
    YOUTUBE_CHANNELS = DatasetInfo(
        'YouTube Channels',
        'media/youtube-channels.csv',
        DatasetFormats.CSV,
        "YouTube channels.")

    # endregion media

    # region outdoor

    CYCLING_ROUTES = DatasetInfo(
        'Cycling Routes',
        'outdoor/cycling-routes.json',
        DatasetFormats.JSON,
        "Cycling routes.")
    HIKING_ROUTES = DatasetInfo(
        'Hiking Routes',
        'outdoor/hiking-routes.json',
        DatasetFormats.JSON,
        "Hiking routes.")
    RUNNING_ROUTES = DatasetInfo(
        'Running Routes',
        'outdoor/running-routes.json',
        DatasetFormats.JSON,
        "Running routes.")

    # endregion outdoor

    # region professional

    COURSES = DatasetInfo(
        'College Courses',
        'professional/courses.json',
        DatasetFormats.JSON,
        "College courses.")
    JOBS = DatasetInfo(
        'Jobs',
        'professional/jobs.json',
        DatasetFormats.JSON,
        "Jobs.")

    # endregion professional

    # region projects

    PROJECTS = DatasetInfo(
        'Projects',
        'projects/projects.json',
        DatasetFormats.JSON,
        "Software projects.")

    # endregion projects

    # region surveys

    SURVEYS = DatasetInfo(
        'Surveys',
        'surveys/surveys.json',
        DatasetFormats.JSON,
        "Surveys.")

    # endregion surveys
