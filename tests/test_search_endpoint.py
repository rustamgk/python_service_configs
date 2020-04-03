import typing
import unittest
from unittest import mock
from http import HTTPStatus

import flask
from flask import url_for
import flask.wrappers
import flask.testing

from .common import BaseTestCase


class TestConfigRegistrySearchEndpoint(BaseTestCase):
    """
    TestConfigRegistrySearchEndpoint
    """

    def test_search_endpoint(self):
        assert url_for('search') == '/search', 'Expected search endpoint URL: /search'
        rv = self.client.get(url_for('search'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'Expected HTTP status 404 Not Found; Repository empty => no results'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 0, 'Should be exact 0 results ATM'

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
            assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status: 200 OK'

        ## No criteria
        rv = self.client.get(url_for('search'))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status 200 Not Found; Search without criteria => any entry match'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 3, 'Should be exact 3 result ATM'

        ## Criteria: no match
        rv = self.client.get(url_for('search', **{'metadata.qwerty': 'foobar'}))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.NOT_FOUND, 'Expected HTTP status 404 Not Found; No entry match that criteria'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 0, 'Should be exact 0 result ATM'

        ## Criteria: 1 match
        rv = self.client.get(url_for('search', **{'metadata.foobar': 'deadbeef'}))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status 200 OK; There is exact 1 entry'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 1, 'Should be exact 1 result ATM'
        assert rv.json[0].get('metadata').get('foobar') == 'deadbeef'

        ## Criteria: 2 match
        rv = self.client.get(url_for('search', **{'metadata.type': 'cpu'}))  # type: flask.wrappers.Response
        assert rv.status_code == HTTPStatus.OK, 'Expected HTTP status 200 OK; There is exact 2 entries'
        assert isinstance(rv.json, list), 'This endpoint should return list'
        assert len(rv.json) == 2, 'Should be exact 1 result ATM'
        assert rv.json[0].get('metadata').get('type') == 'cpu'


if __name__ == '__main__':
    unittest.main()
