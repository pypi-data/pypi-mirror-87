import logging
from typing import Optional

from aporia.consts import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


class AporiaError(Exception):
    """Base class for Aporia SDK exceptions."""

    pass


def handle_error(
    message: str,
    add_trace: bool,
    raise_exception: bool,
    log_level: int = logging.ERROR,
    original_exception: Optional[Exception] = None,
):
    """Handles an error with either a log or an exception.

    Args:
        message (str): Error message
        add_trace (bool): True if stack trace should be added to the log or exception
        raise_exception (bool): True if exceptions should be raised
        log_level (int): Log level for log messages. Defaults to logging.ERROR.
        original_exception (Exception, optional): Original exception for stack trace. Defaults to None.
    """
    if raise_exception:
        if add_trace:
            raise AporiaError(message) from original_exception
        else:
            raise AporiaError(message) from None
    else:
        logger.log(level=log_level, msg=message, exc_info=add_trace)
