import pytest

from .. import utilities

from chris.app.http_codes import HTTPCodes


class TestHTTPCodes:

    @pytest.mark.parametrize('http_code', utilities.get_public_class_members(HTTPCodes))
    def test_http_code_formats(self, http_code):
        message = f"Invalid HTTP code format \"{http_code}\""
        assert isinstance(http_code, int), message
        assert http_code >= 0, message
