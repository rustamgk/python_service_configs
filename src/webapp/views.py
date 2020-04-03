import os
import typing

from http import HTTPStatus
from flask.logging import create_logger
from flask.views import MethodView, View
from flask import Response, make_response, jsonify, current_app, request

from .validator import validate_schema
from .storage import ConfigRegistry

__all__ = (
    'FaviconView',
    'ConfigsAPI',
    'SearchAPI',
)


class FaviconView(View):
    def dispatch_request(self):
        # type: () -> Response
        return make_response('', HTTPStatus.NO_CONTENT)


REGISTRY_ENTRY_SCHEMA = 'schemas/registry-entry-config.schema.json'


class BaseAPIView(MethodView):
    def _storage(self):
        return ConfigRegistry.get()


class ConfigsAPI(BaseAPIView):

    def get(self, name):
        # type: (typing.Optional[str]) -> Response
        if name is None:
            return jsonify(self._storage().list())

        config = self._storage().load(name)
        if config is None:
            return make_response({
                'status': 'not found'
            }, HTTPStatus.NOT_FOUND)
        return make_response(jsonify(config), HTTPStatus.OK)

    @validate_schema(REGISTRY_ENTRY_SCHEMA)
    def post(self):
        # type: () -> Response
        is_stored = self._storage().store(request.json)
        if is_stored:
            return make_response(jsonify({
                'status': 'ok',
            }), HTTPStatus.OK)
        else:
            return make_response(jsonify({
                'status': 'fail',
            }), HTTPStatus.INTERNAL_SERVER_ERROR)

    def delete(self, name):
        # type: (str) -> Response
        is_deleted = self._storage().delete(name)
        if is_deleted:
            return make_response(b'', HTTPStatus.NO_CONTENT)
        return make_response(jsonify({
            'status': 'fail',
            'message': 'Unable to delete confif'
        }), HTTPStatus.INTERNAL_SERVER_ERROR)

    @validate_schema(REGISTRY_ENTRY_SCHEMA)
    def put(self, name):
        # type: (str) -> Response
        is_present = self._storage().is_exists(name)
        if not is_present:
            return make_response({
                'status': 'fail',
                'message': 'Config not exists',
            }, HTTPStatus.NOT_FOUND)

        is_stored = self._storage().store(request.json)
        if is_stored:
            return jsonify({'status': 'ok'})

        return make_response(jsonify({
            'status': 'fail',
            'message': 'Unable to modify config',
        }), HTTPStatus.INTERNAL_SERVER_ERROR)

    patch = put


class SearchAPI(BaseAPIView):
    def get(self):
        results = self._storage().search(request.args)
        if len(results):
            return jsonify(results)
        return make_response(jsonify(results), HTTPStatus.NOT_FOUND)
