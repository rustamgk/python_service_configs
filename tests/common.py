# pylint: disable=unused-import,no-self-use
import typing
import os
import tempfile
import shutil
import unittest
from unittest import mock

import flask
import flask.wrappers
import flask.testing
import webapp

__all__ = (
    'BaseTestCase',
)


class BaseTestCase(unittest.TestCase):
    """
    BaseTestCase
    """

    def setUp(self):
        # type: () -> None
        self._storage_path = tempfile.mkdtemp()
        self.mock_env = mock.patch.dict(os.environ, {'STORAGE_PATH': self._storage_path, })
        self.mock_env.start()
        self.app = webapp.create_app()  # type: flask.Flask
        self.app_context = self.app.test_request_context()  # type: flask.ctx.RequestContext
        self.app_context.push()
        self.client = self.app.test_client()  # type: flask.testing.FlaskClient

    def tearDown(self):
        # type: () -> None
        try:
            shutil.rmtree(self._storage_path)
        finally:
            self.mock_env.stop()
