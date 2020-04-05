# pylint: disable=unused-import,no-self-use
import typing
import unittest
import fastjsonschema
from webapp.validator import get_schema_validator, REGISTRY_ENTRY_SCHEMA


class TestJSONSchemaValidator(unittest.TestCase):
    """
    TestJSONSchemaValidator
    """

    def setUp(self):
        self.schema_validator = get_schema_validator(REGISTRY_ENTRY_SCHEMA)

    def tearDown(self):
        pass

    def test_valid_entries_pass(self):
        valid_entries = [
            {
                'name': 'test-config-1',
                'metadata': {
                    'foobar': 'deadbeef',
                },
            },
            {
                'name': 'datacenter-1',
                'metadata': {
                    'monitoring': {
                        'enabled': 'true'
                    },
                    'limits': {
                        'cpu': {
                            'enabled': 'false',
                            'value': '300m'
                        }
                    },
                    'note': 'upgrade required'
                }
            }
        ]
        try:
            for entry in valid_entries:
                self.schema_validator(entry)
        except fastjsonschema.exceptions.JsonSchemaException as exc:
            self.fail('This should pass; %s' % exc)

    def test_fail_on_non_string_values(self):
        invalid_entries = [
            '',
            {},
            None,
            12,
            {'foobar': 1},
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

        for entry in invalid_entries:
            with self.assertRaises(fastjsonschema.JsonSchemaException):
                self.schema_validator(entry)


if __name__ == '__main__':
    unittest.main()
