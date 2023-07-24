"""Const values for all db unit tests."""
from psycopg import errors
import inspect

PSYCOPG_BASE_ERRORS = [
    errors.Error,
    errors.InterfaceError,
    errors.DatabaseError,
    errors.DataError,
    errors.OperationalError,
    errors.IntegrityError,
    errors.InternalError,
    errors.ProgrammingError,
    errors.NotSupportedError,
    errors.ConnectionTimeout,
    errors.PipelineAborted,
]

PSYCOPG_ALL_ERRORS = [cls for name, cls in inspect.getmembers(errors)
                      if inspect.isclass(cls) and issubclass(cls, errors.Error)]

