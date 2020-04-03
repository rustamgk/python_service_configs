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
    'BaseTestCase'
)

class BaseTestCase(unittest.TestCase):
    """

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
