# pylint: skip-file
from .base import CanonicalException

try:
    from . import pydantic
except ImportError:
    pass


class DoesNotExist(CanonicalException):
    """Raised to indicate that a resource lookup was requested but no
    entity matched the given predicate.
    """
    code = 'RESOURCE_DOES_NOT_EXIST'
    message = "The requested resource does not exist."
    detail = "No resources were found that matched the given search query."
    http_status_code = 404


class Duplicate(CanonicalException):
    """Raised to indicate that the creation of a resource was requested,
    but there was a conflicting identifier.
    """
    code = 'RESOURCE_EXISTS'
    message = "A resource with the provided identifying attributes exists."
    http_status_code = 409


class MultipleObjectsReturned(CanonicalException):
    """Raised when a single resource was requested but the search predicate
    yielded multiple results.
    """
    http_status_code = 404
    code = 'RESOURCE_DOES_NOT_EXIST'
    message = "The requested resource does not exist."
    detail = "Multiple resources were found that matched the given search query."
    hint = "Limit the search query, if possible."
