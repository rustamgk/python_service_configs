import typing
import unittest
import fastjsonschema
from webapp.validator import get_schema_validator


class TestSchemaValidator(unittest.TestCase):
    """
    TestSchemaValidator
    """

    def setUp(self):
        self.schema_validator = get_schema_validator('schemas/registry-entry-config.schema.json')

    def tearDown(self):
        pass

    def test_fail(self):
        with self.assertRaises(fastjsonschema.exceptions.JsonSchemaException):
            self.schema_validator({'foobar': 1})

    def test_pass(self):
        payload = {
            'name': 'test-config',
            'metadata': {
                'foobar': 'deadbeef',
            }
        }
        try:
            self.schema_validator(payload)
        except fastjsonschema.exceptions.JsonSchemaException:
            self.fail('This should pass')


if __name__ == '__main__':
    unittest.main()
