"""Package web application."""
import flask
import json
import pkg_resources

from flask_cors import CORS
from typing import List

from chris.app import logging_utilities
from chris.app import settings
from chris.app.app_utilities import create_response
from chris.app.http_codes import HTTPCodes
from chris.datasets.fetch import fetch_dataset
from chris.datasets.datasets import Datasets


logging_utilities.initialize_logger()
logger = logging_utilities.logger


class App:
    """Package web application."""

    def __init__(self):
        """Construct an App."""
        self._app = flask.Flask(__name__)
        self._register_api_endpoints()
        CORS(self._app)

    def _register_api_endpoints(self):
        self._app.route('/', methods=['GET'])(self.get_info)

        self._app.route('/v1/media', methods=['GET'])(self.get_media_v1)
        self._app.route('/v1/media/movies', methods=['GET'])(self.get_media_movies_v1)
        self._app.route('/v1/media/tv', methods=['GET'])(self.get_media_tv_v1)
        self._app.route('/v1/media/podcasts', methods=['GET'])(self.get_media_podcasts_v1)
        self._app.route('/v1/media/youtube', methods=['GET'])(self.get_media_youtube_v1)

        self._app.route('/v1/outdoor', methods=['GET'])(self.get_outdoor_v1)
        self._app.route('/v1/outdoor/cycling', methods=['GET'])(self.get_outdoor_cycling_v1)
        self._app.route('/v1/outdoor/hiking', methods=['GET'])(self.get_outdoor_hiking_v1)
        self._app.route('/v1/outdoor/running', methods=['GET'])(self.get_outdoor_running_v1)

        self._app.route('/v1/posts', methods=['GET'])(self.get_posts_v1)

        self._app.route('/v1/projects', methods=['GET'])(self.get_projects_v1)
        self._app.route('/v1/projects/download/<project_id>', methods=['POST'])(self.post_projects_download_v1)

        self._app.route('/v1/professional', methods=['GET'])(self.get_professional_v1)
        self._app.route('/v1/professional/courses', methods=['GET'])(self.get_professional_courses_v1)
        self._app.route('/v1/professional/jobs', methods=['GET'])(self.get_professional_jobs_v1)

        self._app.route('/v1/recipes', methods=['GET'])(self.get_recipes_v1)
        self._app.route('/v1/surveys', methods=['GET'])(self.get_surveys_v1)
        self._app.route('/v1/surveys/<survey_id>', methods=['POST'])(self.post_survey_results)

    # region logging

    def _get_request_info(self):
        user_agent = flask.request.user_agent
        user_agent_properties = {
            'browser': user_agent.browser,
            'language': user_agent.language,
            'platform': user_agent.platform,
            'string': user_agent.string,
            'version': user_agent.version,
        }
        return {
            'request_body': json.dumps(flask.request.json),
            'user_agent_properties': json.dumps(user_agent_properties),
            'ip_address': flask.request.remote_addr
        }

    def _log(self, message, *args, extras=None, **kwargs):
        request_info = self._get_request_info()
        log_extras = {'custom_dimensions': request_info}
        extras = log_extras if extras is None else {**log_extras, **extras}
        from pprint import pprint
        pprint(extras)
        logger.info(message, *args, extra=extras, **kwargs)

    # endregion logging
    # region info

    def _list_endpoints(self,
                        with_arguments: bool = True) -> List[str]:
        """
        List all endpoints supported by the application.

        :param with_arguments: Whether to include routes with arguments.
        :return: List of endpoints support by the application.
        """
        links = set()
        for rule in self._app.url_map.iter_rules():
            arguments = {argument: f":{argument}" for argument in rule.arguments}
            link = flask.url_for(rule.endpoint, **arguments)
            links.add(link)
        return list(links)

    @logging_utilities.log_context('get_info', tag='api')
    def get_info(self):
        """
        Get application information.

        This includes information about the available API routes.
        """
        return flask.jsonify({
            'docs': 'http://docs.chrisgregory.me/',
            'package': 'https://pypi.org/project/chris',
            'routes': sorted(self._list_endpoints()),
            'source': 'https://github.com/gregorybchris/personal-website',
            'version': pkg_resources.get_distribution('chris').version,
        })

    # endregion info
    # region media

    @logging_utilities.log_context('get_media', tag='api')
    def get_media_v1(self):
        """Get media data."""
        movies_df = fetch_dataset(Datasets.MOVIES)
        podcasts_df = fetch_dataset(Datasets.PODCASTS)
        tv_shows_df = fetch_dataset(Datasets.TV_SHOWS)
        youtube_channels_df = fetch_dataset(Datasets.YOUTUBE_CHANNELS)
        return flask.jsonify({
            'movies': list(movies_df.T.to_dict().values()),
            'podcasts': list(podcasts_df.T.to_dict().values()),
            'tv': list(tv_shows_df.T.to_dict().values()),
            'youtube': list(youtube_channels_df.T.to_dict().values()),
        })

    @logging_utilities.log_context('get_media_movies', tag='api')
    def get_media_movies_v1(self):
        """Get movie data."""
        movies_df = fetch_dataset(Datasets.MOVIES)
        return flask.jsonify(list(movies_df.T.to_dict().values()))

    @logging_utilities.log_context('get_media_podcasts', tag='api')
    def get_media_podcasts_v1(self):
        """Get podcast data."""
        podcasts_df = fetch_dataset(Datasets.PODCASTS)
        return flask.jsonify(list(podcasts_df.T.to_dict().values()))

    @logging_utilities.log_context('get_media_tv', tag='api')
    def get_media_tv_v1(self):
        """Get TV data."""
        tv_df = fetch_dataset(Datasets.TV_SHOWS)
        return flask.jsonify(list(tv_df.T.to_dict().values()))

    @logging_utilities.log_context('get_media_youtube', tag='api')
    def get_media_youtube_v1(self):
        """Get YouTube data."""
        youtube_df = fetch_dataset(Datasets.YOUTUBE_CHANNELS)
        return flask.jsonify(list(youtube_df.T.to_dict().values()))

    # endregion media
    # region outdoor

    @logging_utilities.log_context('get_outdoor', tag='api')
    def get_outdoor_v1(self):
        """Get outdoor data."""
        return flask.jsonify({
            'cycling': fetch_dataset(Datasets.CYCLING_ROUTES),
            'hiking': fetch_dataset(Datasets.HIKING_ROUTES),
            'running': fetch_dataset(Datasets.RUNNING_ROUTES),
        })

    @logging_utilities.log_context('get_outdoor_cycling', tag='api')
    def get_outdoor_cycling_v1(self):
        """Get cycling data."""
        return flask.jsonify(fetch_dataset(Datasets.CYCLING_ROUTES))

    @logging_utilities.log_context('get_outdoor_hiking', tag='api')
    def get_outdoor_hiking_v1(self):
        """Get hiking data."""
        return flask.jsonify(fetch_dataset(Datasets.HIKING_ROUTES))

    @logging_utilities.log_context('get_outdoor_running', tag='api')
    def get_outdoor_running_v1(self):
        """Get running data."""
        return flask.jsonify(fetch_dataset(Datasets.RUNNING_ROUTES))

    # endregion outdoor
    # region posts

    @logging_utilities.log_context('get_posts', tag='api')
    def get_posts_v1(self):
        """Get blog post data."""
        return flask.jsonify({
            'posts': fetch_dataset(Datasets.POSTS)
        })

    # endregion posts
    # region projects

    @logging_utilities.log_context('get_projects', tag='api')
    def get_projects_v1(self):
        """Get project data."""
        return flask.jsonify(fetch_dataset(Datasets.PROJECTS))

    @logging_utilities.log_context('post_projects_download', tag='api')
    def post_projects_download_v1(self, project_id):
        """Post a project download action."""
        projects = fetch_dataset(Datasets.PROJECTS)
        for project in projects:
            if project['project_id'] == project_id:
                project_name = project['name']
                self._log(f"Project \"{project_name}\" ({project_id}) downloaded")

                success_message = f"Successfully downloaded project {project_name}"
                return create_response(success_message, HTTPCodes.SUCCESS_GENERAL)
        error_message = f"Project with ID {project_id} not found"
        return create_response(error_message, HTTPCodes.ERROR_NOT_FOUND)

    # endregion projects
    # region professional

    @logging_utilities.log_context('get_professional', tag='api')
    def get_professional_v1(self):
        """Get professional data."""
        return flask.jsonify({
            'courses': fetch_dataset(Datasets.COURSES),
            'jobs': fetch_dataset(Datasets.JOBS),
        })

    @logging_utilities.log_context('get_professional_courses', tag='api')
    def get_professional_courses_v1(self):
        """Get college course data."""
        return flask.jsonify(fetch_dataset(Datasets.COURSES))

    @logging_utilities.log_context('get_professional_jobs', tag='api')
    def get_professional_jobs_v1(self):
        """Get job data."""
        return flask.jsonify(fetch_dataset(Datasets.JOBS))

    # endregion professional
    # region recipes

    @logging_utilities.log_context('get_recipes', tag='api')
    def get_recipes_v1(self):
        """Get recipe data."""
        return flask.jsonify(fetch_dataset(Datasets.RECIPES))

    # endregion recipes
    # region surveys

    @logging_utilities.log_context('get_surveys', tag='api')
    def get_surveys_v1(self):
        """Get survey data."""
        return flask.jsonify(fetch_dataset(Datasets.SURVEYS))

    @logging_utilities.log_context('post_survey_results', tag='api')
    def post_survey_results(self, survey_id):
        """Post a survey result."""
        surveys = fetch_dataset(Datasets.SURVEYS)
        for survey in surveys:
            if survey['survey_id'] == survey_id:
                survey_name = survey['name']
                self._log(f"Survey \"{survey_name}\" ({survey_id}) submitted")

                success_message = f"Successfully submitted survey \"{survey_name}\""
                return create_response(success_message, HTTPCodes.SUCCESS_GENERAL)
        error_message = f"Survey with ID {survey_id} not found"
        return create_response(error_message, HTTPCodes.ERROR_NOT_FOUND)

    # endregion surveys

    def run(self):
        """Run the web application."""
        debug_mode = 1 if bool(settings.FLASK_DEBUG) else 0
        self._app.run(host=settings.FLASK_HOST,
                      port=settings.FLASK_RUN_PORT,
                      debug=debug_mode)
