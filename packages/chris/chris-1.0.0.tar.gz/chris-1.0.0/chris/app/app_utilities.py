"""Application utilities."""
import flask

from typing import Tuple


def create_response(message: str,
                    code: int) -> Tuple[flask.wrappers.Response, int]:
    """
    Create an HTTP response.

    :param message: Response message.
    :param code: Response code.
    :return: Flask HTTP response.
    """
    return (flask.jsonify(message=message), code)
