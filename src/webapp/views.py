import os
import typing

from http import HTTPStatus
from flask.logging import create_logger
from flask.views import MethodView, View
from flask import Response, make_response, jsonify, current_app, request

from .validator import validate_schema

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

    @validate_schema('schemas/registry-entry-config.schema.json')
    def post(self):
        # type: () -> Response
        # config = request.json
        return make_response(jsonify({
            'status': 'ok',
        }), 200)


class SearchAPI(MethodView):
    def get(self):
        return jsonify([])
