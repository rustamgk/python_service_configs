import typing
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing
import webapp


class TestWebapp(unittest.TestCase):
    """
    TestWebapp
    """

    def setUp(self):
        self.app = webapp.create_app()  # type: flask.Flask
        self.app_context = self.app.test_request_context()  # type: flask.ctx.RequestContext
        self.app_context.push()
        self.client = self.app.test_client()  # type: flask.testing.FlaskClient

    def tearDown(self):
        pass

    def test_favicon_get_no_content(self):
        assert url_for('favicon') == '/favicon.ico', 'Expected favicon URL: /favicon.ico'
        rv = self.client.get(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NO_CONTENT, 'Expected HTTP status: 204 No Content'
        assert rv.data == b'', 'Expected empty response'

    def test_favicon_post_not_allowed(self):
        assert url_for('favicon') == '/favicon.ico', 'Expected favicon URL: /favicon.ico'
        rv = self.client.post(url_for('favicon'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.METHOD_NOT_ALLOWED, 'Expected HTTP status: 405 Method Not Allowed'

    def test_unsupported_endpoints(self):
        rv = self.client.get('/any-other-endpoint')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'Expected HTTP status: 404 Not Found'
        # assert rv.status_code == HTTPStatus.FORBIDDEN, 'Expected HTTP status: 403 Forbidden'

    def test_configs_get(self):
        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.get('/configs')  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, list), 'This endpoint should return list'


if __name__ == '__main__':
    unittest.main()
