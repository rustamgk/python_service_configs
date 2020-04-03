import typing
import sys
import logging

import flask
from flask import redirect, url_for
from flask.logging import create_logger

from .views import FaviconView, ConfigsAPI, SearchAPI

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

    @app.before_first_request
    def setup_logging():
        if not app.debug:
            # In production mode, add log handler to sys.stderr.
            app.logger.addHandler(logging.StreamHandler())
            app.logger.setLevel(logging.INFO)

    ## Dummy endpoint for favicon.ico
    app.add_url_rule('/favicon.ico', view_func=FaviconView.as_view('favicon'))

    ## Config API Endpoint
    configs_view = ConfigsAPI.as_view('configs')
    app.add_url_rule('/configs', strict_slashes=False, defaults={'name': None}, view_func=configs_view,
                     methods=['GET'])
    app.add_url_rule('/configs', strict_slashes=False, view_func=configs_view, methods=['POST'])
    app.add_url_rule('/configs/<name>', view_func=configs_view, methods=['GET', 'PUT', 'PATCH', 'DELETE'])

    ## Search API Endpoint
    app.add_url_rule('/search', view_func=SearchAPI.as_view('search'))

    return app
