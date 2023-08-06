# pylint: skip-file
from .base import CanonicalException
from .schema import CollectionValidationErrorSchema
from .schema import ValidationErrorSchema

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


class ValidationError(CanonicalException):
    """Raised when input data did not satisfy the specifed format
    requirements.
    """
    schema_class = ValidationErrorSchema
    http_status_code = 422
    code = 'DATA_CONSTRAINT_VIOLATION'
    message = "The input data did not satisfy the specification."
    hint = "Inspect .spec to see field-specific errors."

    def __init__(self, *args, **kwargs):
        self.spec = kwargs.pop('spec')
        self.index = kwargs.pop('index', None)
        super().__init__(*args, **kwargs)



class CollectionValidationError(CanonicalException):
    """Raised when collection input data did not satisfy the specifed format
    requirements.
    """
    schema_class = CollectionValidationErrorSchema
    http_status_code = 422
    code = 'DATA_CONSTRAINT_VIOLATION'
    message = "The input data did not satisfy the specification."
    hint = "Inspect .items to see the errors for each item."

    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop('items')
        super().__init__(*args, **kwargs)
