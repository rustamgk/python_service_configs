import typing  # pylint: disable=unused-import
import logging
from flask.logging import default_handler

__all__ = (
    'logger',
)

logger = logging.getLogger()  # pylint: disable=invalid-name
# logger.addHandler(default_handler)
