import typing

from http import HTTPStatus
from flask.logging import create_logger
from flask.views import MethodView, View
from flask import Response, make_response, jsonify, current_app

__all__ = (
    'FaviconView',
    'ConfigsAPI',
    'SearchAPI',
)


class FaviconView(View):
    def dispatch_request(self):
        # type: () -> Response
        return make_response('', HTTPStatus.NO_CONTENT)


class ConfigsAPI(MethodView):
    def get(self, name):
        # type: (typing.Optional[str]) -> Response
        current_app.logger.info('Name is: %s', name)
        return jsonify([])


class SearchAPI(MethodView):
    def get(self):
        return jsonify([])
