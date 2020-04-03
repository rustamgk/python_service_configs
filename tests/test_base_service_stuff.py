import typing
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing

from .common import BaseTestCase


class TestBaseServiceStuff(BaseTestCase):
    """
    TestBaseServiceStuff
    """

    def test_favicon_return_no_content(self):
        assert url_for('favicon') == '/favicon.ico', 'Expected favicon URL: /favicon.ico'
        rv = self.client.get(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NO_CONTENT, 'Expected HTTP status: 204 No Content'
        assert rv.data == b'', 'Expected empty response'

    def test_favicon_post_not_allowed(self):
        assert url_for('favicon') == '/favicon.ico', 'Expected favicon URL: /favicon.ico'
        rv = self.client.post(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED, 'Expected HTTP status: 405 Method Not Allowed'

    def test_endpoint_urls(self):
        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        assert url_for('configs', name='test') == '/configs/test', 'Expected URL: /configs/test'
        assert url_for('search') == '/search', 'Expected configs endpoint URL: /search'

    def test_unsupported_endpoints(self):
        rv = self.client.get('/any-other-endpoint')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'Expected HTTP status: 404 Not Found'
        # assert rv.status_code == HTTPStatus.FORBIDDEN, 'Expected HTTP status: 403 Forbidden'


if __name__ == '__main__':
    unittest.main()
