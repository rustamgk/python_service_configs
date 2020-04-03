import typing
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing

from .common import BaseTestCase


class TestConfigRegistry(BaseTestCase):
    """
    TestConfigRegistry
    """

    def test_configs_get(self):
        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, list), 'This endpoint should return list'

    def test_configs_post_empty_body(self):
        payload = b''
        headers = {'Content-Type': 'application/json'}

        rv = self.client.post(url_for('configs'), data=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_wrong_content_type(self):
        payload = {
            'foobar': 'deadbeef',
        }

        headers = {'Content-Type': 'text/plain'}

        rv = self.client.post(url_for('configs'), json=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_incorrect_schema(self):
        payload = {
            'foobar': 'deadbeef',
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_wrong_metadata_type(self):
        payload = {
            'name': 'test-config-1',
            'metadata': 'string',
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST, 'Expected HTTP status: 400 Bad Request'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'bad request', 'Fail expected'

    def test_configs_post_correct_request(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'

    def test_configs_endpoint(self):
        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 0, 'Should be exact 0 results ATM'

    def test_configs_endpoint_return_results(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'

        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 1, 'Should be exact 0 results ATM'

        assert rv.json[0].get('name') == 'test-config-1', 'Should match pasted result'


if __name__ == '__main__':
    unittest.main()
