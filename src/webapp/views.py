import os
import typing

from http import HTTPStatus
from flask.logging import create_logger
from flask.views import MethodView, View
from flask import Response, make_response, jsonify, current_app, request, url_for

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
        '''
        200 - OK
        404 - Not Found
        '''
        if name is None:
            return jsonify(self._storage().list())

        config = self._storage().load(name)
        if config is None:
            return make_response(jsonify({
                'message': 'not found',
            }), HTTPStatus.NOT_FOUND)

        return jsonify(config)

    @validate_schema(REGISTRY_ENTRY_SCHEMA)
    def post(self):
        # type: () -> Response
        '''
        https://tools.ietf.org/html/rfc7231#section-4.3.3
        201 - Created
        409 - Conflict
        500 - Internal Server Error
        '''
        is_exists = self._storage().is_exists(request.json.get('name'))
        if is_exists:
            resp = make_response(jsonify({
                'status': 'error',
                'message': 'entry exists'
            }), HTTPStatus.CONFLICT)
            resp.headers['Location'] = url_for('configs', name=request.json.get('name'), _external=True, _method='GET')
            return resp

        is_stored = self._storage().store(request.json)
        if is_stored:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'created'
            }), HTTPStatus.CREATED)  # type: Response

        else:
            return make_response(jsonify({
                'status': 'error',
                'message': 'unable to create entry'
            }), HTTPStatus.INTERNAL_SERVER_ERROR)

    def delete(self, name):
        # type: (str) -> Response
        '''
        https://tools.ietf.org/html/rfc7231#section-4.3.5
        200 - Ok
        500 - Internal Server Error
        '''
        is_deleted = self._storage().delete(name)
        if is_deleted:
            return make_response(jsonify({
                'status': 'ok',
                'message': 'deleted'
            }), HTTPStatus.OK)
        return make_response(jsonify({
            'status': 'error',
            'message': 'unable to delete entry'
        }), HTTPStatus.INTERNAL_SERVER_ERROR)

    @validate_schema(REGISTRY_ENTRY_SCHEMA)
    def put(self, name):
        # type: (str) -> Response
        '''
        https://tools.ietf.org/html/rfc7231#section-4.3.4
        200 - Ok
        404 - Not Found
        500 - Internal Server Error
        '''
        is_present = self._storage().is_exists(name)
        if not is_present:
            return make_response({
                'status': 'error',
                'message': 'entry not exists',
            }, HTTPStatus.NOT_FOUND)

        is_stored = self._storage().store(request.json)
        if is_stored:
            return jsonify({'status': 'ok'})

        return make_response(jsonify({
            'status': 'fail',
            'message': 'unable to modify config',
        }), HTTPStatus.INTERNAL_SERVER_ERROR)

    ## Same as PUT
    patch = put


class SearchAPI(BaseAPIView):
    def get(self):
        '''
        200 - Ok
        404 - Not Found
        '''
        results = self._storage().search(request.args)
        if len(results):
            return jsonify(results)
        return make_response(jsonify(results), HTTPStatus.NOT_FOUND)
