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

    def test_configs_endpoint_delete_non_exists(self):
        rv = self.client.delete(url_for('configs', name='qwerty'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, dict), 'This endpoint should return dict'

    def test_configs_endpoint_delete_success(self):
        config_name = 'qwerty'
        payload = {
            'name': config_name,
            'metadata': {'foobar': 'deadbeef', },
        }

        rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.CREATED

        rv = self.client.get(url_for('configs', name=config_name))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert rv.json.get('name') == config_name

        rv = self.client.delete(url_for('configs', name=config_name))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK
        assert isinstance(rv.json, dict), 'This endpoint should return dict'

        rv = self.client.get(url_for('configs', name=config_name))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    unittest.main()
