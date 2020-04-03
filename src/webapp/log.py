import typing
import logging
from flask.logging import default_handler

__all__ = (
    'logger',
)

logger = logging.getLogger()
logger.addHandler(default_handler)
