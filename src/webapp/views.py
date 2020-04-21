import typing
from flask.views import MethodView, View
from flask import Response, make_response, jsonify
from http import HTTPStatus

__all__ = (
    'FaviconView',
    'ConfigsAPI',
)


class FaviconView(View):
    '''
    Favicon not present.
    Return 204 No Content
    '''

    def dispatch_request(self):
        # type: () -> (str, int)
        return ('', HTTPStatus.NO_CONTENT)


class ConfigsAPI(MethodView):
    def get(self):
        return jsonify([])
