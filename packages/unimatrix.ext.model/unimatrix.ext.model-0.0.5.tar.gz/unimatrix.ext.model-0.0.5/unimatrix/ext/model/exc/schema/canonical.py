"""Declares :class:`CanonicalExceptionSchema`."""
import marshmallow
import marshmallow.fields


class CanonicalExceptionSchema(marshmallow.Schema):
    """The schema for exceptions that are not otherwise specified."""

    id = marshmallow.fields.UUID(
        required=True
    )

    code = marshmallow.fields.String(
        required=True
    )

    message = marshmallow.fields.String(
        required=True
    )

    detail = marshmallow.fields.String(
        required=True
    )

    hint = marshmallow.fields.String(
        required=True
    )
