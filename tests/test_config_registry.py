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
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, list), 'This endpoint should return list'

    def test_configs_post_empty_body(self):
        payload = b''
        headers = {'Content-Type': 'application/json'}

        rv = self.client.post(url_for('configs'), data=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_post_wrong_content_type(self):
        payload = {
            'foobar': 'deadbeef',
        }

        headers = {'Content-Type': 'text/plain'}

        rv = self.client.post(url_for('configs'), json=payload, headers=headers)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_post_incorrect_schema(self):
        payload = {
            'foobar': 'deadbeef',
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_post_wrong_metadata_type(self):
        payload = {
            'name': 'test-config-1',
            'metadata': 'string',
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Fail expected'

    def test_configs_post_correct_request(self):
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

    def test_configs_post_same_correct_request_multiple_times(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        ## First request - Created
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'
        assert rv.headers.get('Location') is None, 'Location header not set'

        for _ in range(3):
            rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
            assert rv.status_code == HTTPStatus.CONFLICT
            assert isinstance(rv.json, dict), 'This endpoint should return dict'
            assert rv.json.get('status') == 'error', 'Status==error expected'
            assert rv.headers.get('Location') is not None, 'Location header expected'

        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert len(rv.json) == 1, 'Should be 1 entry'

    def test_configs_put_correct_request_while_entry_not_exists(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        rv = self.client.put(url_for('configs', name='test-config-1'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Status==error expected'

    def test_configs_put_correct_request(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED
        
        rv = self.client.get(url_for('configs', name='test-config-1'))
        assert rv.status_code == HTTPStatus.OK
        assert rv.json.get('metadata').get('foobar') == 'deadbeef'
        assert rv.json == payload

        payload = {
            'name': 'test-config-1',
            'metadata': {
                'cpu': {
                    'arch': 'arm',
                }
            },
        }

        rv = self.client.put(url_for('configs', name='test-config-1'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'

        rv = self.client.get(url_for('configs', name='test-config-1'))
        assert rv.status_code == HTTPStatus.OK
        assert rv.json.get('metadata').get('foobar') is None
        assert rv.json.get('metadata').get('cpu').get('arch') == 'arm'
        assert rv.json == payload

    def test_configs_endpoint(self):
        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
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
        assert rv.status_code == HTTPStatus.CREATED

        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 1, 'Should be exact 0 results ATM'

        assert rv.json[0].get('name') == 'test-config-1', 'Should match pasted result'


if __name__ == '__main__':
    unittest.main()
