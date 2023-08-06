import flask

from chris.app import app_utilities
from chris.app.http_codes import HTTPCodes


class TestAppUtilities:

    def test_create_response(self):
        test_app = flask.Flask(__name__)
        test_message = 'my_message'
        test_code = HTTPCodes.SUCCESS_GENERAL
        with test_app.app_context():
            response, status = app_utilities.create_response(test_message, test_code)
            assert status == test_code
            assert response.json['message'] == test_message
