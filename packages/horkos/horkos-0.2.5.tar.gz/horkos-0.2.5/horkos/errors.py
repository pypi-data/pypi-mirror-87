class Error(Exception):
    """Base error."""


class SchemaValidationError(Error):
    """The given data schema failed to validate."""


class RecordValidationError(Error):
    """A record failed to validate against the schema."""


class CastingError(Error):
    """Could not cast value."""
