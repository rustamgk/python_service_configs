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


class TestConfigsGet(BaseTestCase):
    """
    TestConfigsGet
    """

    def test_configs_endpoint_get_empty(self):
        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 0, 'Should be exact 0 results ATM'

    def test_configs_endpoint_get_return_stored(self):
        amount = 3
        for config_id in range(amount):
            payload = {'name': 'config-%s' % config_id, 'metadata': {}}
            rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
            assert rv.status_code == HTTPStatus.CREATED

        rv = self.client.get(url_for('configs'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == amount, 'Should be exact 0 results ATM'

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
