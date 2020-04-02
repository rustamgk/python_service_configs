import typing
import sys

import flask
from flask import redirect, url_for
from flask.logging import create_logger

from .views import FaviconView, ConfigsAPI

__all__ = (
    'create_app',
)

FLASK_APP = __name__.split('.')[0]


def create_app():
    # type: () -> flask.Flask
    app = flask.Flask(FLASK_APP)
    logger = create_logger(app)

    logger.info('Runtime: app=%s; flask=%s; debug=%s', FLASK_APP, flask.__version__, app.debug)
    logger.info('Runtime: python=%s;', sys.version)

    app.add_url_rule('/favicon.ico', view_func=FaviconView.as_view('favicon'))
    app.add_url_rule('/configs', view_func=ConfigsAPI.as_view('configs'))

    return app
