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


class TestSearchEndpoint(BaseTestCase):
    """
    TestSearchEndpoint
    """

    def test_search_endpoint(self):
        rv = self.client.get(url_for('search'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'Repository empty => no results'
        assert isinstance(rv.json, list)
        assert len(rv.json) == 0

    def test_search_endpoint_misc_requests(self):
        payloads = [
            {
                'name': 'test-config-1',
                'metadata': {
                    'foobar': 'deadbeef',
                },
            },
            {
                'name': 'another config',
                'metadata': {
                    'type': 'cpu',
                    'cpu': {
                        'arch': 'x86'
                    },
                },
            },
            {
                'name': 'some other config',
                'metadata': {
                    'type': 'cpu',
                    'cpu': {
                        'arch': 'x86-64'
                    },
                },
            }
        ]
        for payload in payloads:
            rv = self.client.post(url_for('configs'), json=payload)  # type: flask.wrappers.Response
            assert rv.status_code == HTTPStatus.CREATED

        # No criteria
        rv = self.client.get(url_for('search'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Search without criteria => any entry match'
        assert isinstance(rv.json, list)
        assert len(rv.json) == 3

        # Criteria: no match
        url = url_for('search', **{'metadata.qwerty': 'foobar'})
        rv = self.client.get(url)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'No entry match that criteria'
        assert isinstance(rv.json, list)
        assert len(rv.json) == 0

        # Criteria: 1 match
        url = url_for('search', **{'metadata.foobar': 'deadbeef'})
        rv = self.client.get(url)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'There is exact 1 entry'
        assert isinstance(rv.json, list)
        assert len(rv.json) == 1
        assert rv.json[0].get('metadata').get('foobar') == 'deadbeef'

        # Criteria: 2 match
        url = url_for('search', **{'metadata.type': 'cpu'})
        rv = self.client.get(url)  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'There is exact 2 entries'
        assert isinstance(rv.json, list)
        assert len(rv.json) == 2
        assert rv.json[0].get('metadata').get('type') == 'cpu'


if __name__ == '__main__':
    unittest.main()
