import typing
import os
import tempfile
import shutil
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing
import webapp


class TestConfigRegistry(unittest.TestCase):
    """
    TestConfigRegistry
    """

    def setUp(self):
        self._storage_path = tempfile.mkdtemp()
        self.m = mock.patch.dict(os.environ, {'STORAGE_PATH': self._storage_path, })
        self.m.start()
        self.app = webapp.create_app()  # type: flask.Flask
        self.app_context = self.app.test_request_context()  # type: flask.ctx.RequestContext
        self.app_context.push()
        self.client = self.app.test_client()  # type: flask.testing.FlaskClient

    def tearDown(self):
        try:
            shutil.rmtree(self._storage_path)
        finally:
            self.m.stop()

    def test_favicon_return_no_content(self):
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
        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, list), 'This endpoint should return list'

    def test_configs_post_empty_body(self):
        payload = b''
        headers = {'Content-Type': 'application/json'}

        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.post(url_for('configs'), data=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_wrong_content_type(self):
        payload = {
            'foobar': 'deadbeef',
        }

        headers = {'Content-Type': 'text/plain'}

        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.post(url_for('configs'), json=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_incorrect_schema(self):
        payload = {
            'foobar': 'deadbeef',
        }

        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_wrong_metadata_type(self):
        payload = {
            'name': 'test-config-1',
            'metadata': 'string',
        }

        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    # @mock.patch.dict(os.environ, {'STORAGE_PATH': tempfile.mkdtemp()})
    def test_configs_post_correct_request(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        assert url_for('configs') == '/configs', 'Expected configs endpoint URL: /configs'
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'


if __name__ == '__main__':
    unittest.main()
