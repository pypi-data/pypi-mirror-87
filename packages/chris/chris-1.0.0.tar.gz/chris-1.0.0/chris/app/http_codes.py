"""HTTP response codes."""


class HTTPCodes:
    """HTTP response codes."""

    # region success

    SUCCESS_GENERAL = 200
    SUCCESS_CREATED = 201

    # endregion success

    # region error

    ERROR_GENERAL = 400
    ERROR_INVALID_PARAM = 403
    ERROR_NOT_FOUND = 404
    ERROR_INTERNAL_SERVER = 500

    # endregion error
