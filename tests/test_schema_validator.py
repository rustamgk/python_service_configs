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

    def test_valid_entries_pass(self):
        entries = [
            {
                'name': 'test-config-1',
                'metadata': {
                    'foobar': 'deadbeef',
                },
            },
        ]
        try:
            for entry in entries:
                self.schema_validator(entry)
        except fastjsonschema.exceptions.JsonSchemaException:
            self.fail('This should pass')

    def test_fail_on_non_string_values(self):
        entries = [
            '',
            {},
            None,
            12,
            {
                'name': 'foobar'
            },
            {
                'metadata': {
                    'cpu': 'true'
                }
            },
            {
                'name': 'fail',
                'metadata': {
                    'cpu': {
                        'value': 3.14159
                    }
                }
            }
        ]

        for entry in entries:
            with self.assertRaises(fastjsonschema.exceptions.JsonSchemaException):
                self.schema_validator(entry)


if __name__ == '__main__':
    unittest.main()
