
from requests import Response


def check_status_code(req: Response):
    """
    Check status code of requests response to raise the correct exception

    :param req: The requests Response of your requests call
    """

    if req.status_code == 400:
        raise QueryError(url=req.url, message="Endpoint is invalid or was built incorrectly")
    elif req.status_code == 401:
        raise JWTError(message="JWT Access token is missing or invalid credentials were provided")
    elif req.status_code == 403:
        raise PermissionsError(message="User doesn't have the correct permissions to access this data")
    elif req.status_code == 404:
        raise QueryError(url=req.url, message="Endpoint is invalid or was built incorrectly")


class PyBehrtechException(Exception):
    """Base exception used by this module."""
    pass


class JWTError(PyBehrtechException):
    """A request for the JWT failed"""

    def __init__(self, message):
        PyBehrtechException.__init__(self, message)


class PermissionsError(PyBehrtechException):
    """User of request doesn't have permissions"""

    def __init__(self, message):
        PyBehrtechException.__init__(self, message)


class QueryError(PyBehrtechException):
    """Request to endpoint is invalid or was built incorrectly"""

    def __init__(self, url, message):
        self.url = url
        PyBehrtechException.__init__(self, url, message)
