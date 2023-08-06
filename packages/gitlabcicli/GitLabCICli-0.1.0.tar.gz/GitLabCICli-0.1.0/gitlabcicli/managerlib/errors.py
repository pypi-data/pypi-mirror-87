"""The errors that are raised by the lib."""


class OperationalError(Exception):
    """A server side operation could not be executed."""


class ValidationError(ValueError):
    """Raised, when a value could not be validated."""


class QueryError(Exception):
    """A error was caused by a specific query."""


class DoesNotExist(QueryError):
    """A ressource matching the query does not exist."""


class APIError(Exception):
    """The API returned an error."""
