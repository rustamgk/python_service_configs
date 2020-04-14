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


class TestConfigsPutPatch(BaseTestCase):
    """
    TestConfigsPutPatch

    patch/put - share same handler
    """

    def test_configs_endpoint_put_correct_request_while_entry_not_exists(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }

        url = url_for('configs', name='test-config-1')
        rv = self.client.put(url, json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'error', 'Status==error expected'

    def test_configs_endpoint_put_correct_request(self):
        payload = {
            'name': 'test-config-1',
            'metadata': {
                'foobar': 'deadbeef',
            },
        }
        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED

        rv = self.client.get(url_for('configs', name='test-config-1'))  # type: flask.wrappers.Response
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

        url = url_for('configs', name='test-config-1')
        rv = self.client.put(url, json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, dict), 'This endpoint should return dict'
        assert rv.json.get('status') == 'ok', 'Status==ok expected'

        rv = self.client.get(url_for('configs', name='test-config-1'))
        assert rv.status_code == HTTPStatus.OK
        assert rv.json.get('metadata').get('foobar') is None
        assert rv.json.get('metadata').get('cpu').get('arch') == 'arm'
        assert rv.json == payload


if __name__ == '__main__':
    unittest.main()
