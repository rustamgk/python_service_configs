# pylint: disable=unused-import,no-self-use
import typing
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing

from .common import BaseTestCase


class TestConfigsPost(BaseTestCase):
    """
    TestConfigsPost
    """

    def test_configs_endpoint_post_empty_body(self):
        headers = {'Content-Type': 'application/json'}
        payload = b''

        rv = self.client.post(url_for('configs'), data=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_endpoint_post_wrong_content_type(self):
        headers = {'Content-Type': 'text/plain'}
        payload = {'foobar': 'deadbeef'}

        rv = self.client.post(url_for('configs'), json=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_endpoint_post_incorrect_schema(self):
        payload = {'foobar': 'deadbeef'}

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_endpoint_post_wrong_metadata_type(self):
        payload = {'name': 'test-config-1', 'metadata': 'string'}

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_endpoint_post_correct_request(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'

    def test_configs_endpoint_post_same_correct_request_multiple_times(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        # First request - Created
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'
        assert rv.headers.get('Location') is None, 'Location header not set'

        # In case config with such name exists -> return 409 Conflict
        for _ in range(3):
            rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
            assert rv.status_code == HTTPStatus.CONFLICT
            assert isinstance(rv.json, dict), 'This endpoint should return dict'
            assert rv.json.get('status') == 'error', 'Status==error expected'
            assert rv.headers.get('Location') is not None, 'Location header expected'

        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert len(rv.json) == 1, 'Should be 1 entry'


if __name__ == '__main__':
    unittest.main()
