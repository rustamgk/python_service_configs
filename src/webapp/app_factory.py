import typing

import flask

from .views import FaviconView, ConfigsAPI, SearchAPI

__all__ = (
    'create_app',
)

FLASK_APP = __name__.split('.')[0]


def create_app():
    # type: () -> flask.Flask
    app = flask.Flask(FLASK_APP)

    # Dummy endpoint for favicon.ico
    # avoid 404 Not Found error
    app.add_url_rule('/favicon.ico', view_func=FaviconView.as_view('favicon'))

    # Config API Endpoint
    configs_view = ConfigsAPI.as_view('configs')
    app.add_url_rule('/configs', strict_slashes=False,
                     defaults={'name': None}, view_func=configs_view, methods=['GET'])
    app.add_url_rule('/configs', strict_slashes=False,
                     view_func=configs_view, methods=['POST'])
    app.add_url_rule('/configs/<name>', view_func=configs_view,
                     methods=['GET', 'PUT', 'PATCH', 'DELETE'])

    # Search API Endpoint
    app.add_url_rule('/search', view_func=SearchAPI.as_view('search'))

    return app
