from enum import Enum
from http import HTTPStatus


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class HTTPMessage(Enum):
    REQUEST = "request"
    RESPONSE = "response"


__all__ = ["HTTPMethod", "HTTPStatus"]
