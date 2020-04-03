import typing
import unittest
from unittest import mock

from webapp.utils import is_entry_match


class TestEntryMatch(unittest.TestCase):
    """
    Test is_entry_match function actually works
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_entry_match_helper(self):
        entry = {
            'name': 'entry',
            'metadata': {
                'cpu': {
                    'cores': '8',
                    'arch': 'x86',
                },
                'memory': {
                    'size': '2048'
                }
            }
        }

        assert is_entry_match(entry, {'metadata.cpu.cores': '8', }) is True
        assert is_entry_match(entry, {'metadata.cpu.cores': '7', }) is False
        assert is_entry_match(entry, {'wololo': '7', }) is False
        assert is_entry_match(entry, {
            'metadata.cpu.arch': 'x86',
            'metadata.memory.size': '2048',
        }) is True
        assert is_entry_match(entry, {'metadata.cpu': '12'}) is False

    def test_examples1_pass(self):
        examples = [
            {
                "name": "datacenter-1",
                "metadata": {
                    "monitoring": {
                        "enabled": "true"
                    },
                    "limits": {
                        "cpu": {
                            "enabled": "false",
                            "value": "300m"
                        }
                    }
                }
            },
            {
                "name": "datacenter-2",
                "metadata": {
                    "monitoring": {
                        "enabled": "true"
                    },
                    "limits": {
                        "cpu": {
                            "enabled": "true",
                            "value": "250m"
                        }
                    }
                }
            }
        ]

        for entry in examples:
            assert is_entry_match(entry, {'metadata.monitoring.enabled': 'true'}) is True

    def test_examples2_pass(self):
        examples = [
            {
                "name": "burger-nutrition",
                "metadata": {
                    "calories": "230",
                    "fats": {
                        "saturated-fat": "0g",
                        "trans-fat": "1g"
                    },
                    "carbohydrates": {
                        "dietary-fiber": "4g",
                        "sugars": "1g"
                    },
                    "allergens": {
                        "nuts": "false",
                        "seafood": "false",
                        "eggs": "true"
                    }
                }
            }
        ]

        for entry in examples:
            assert is_entry_match(entry, {'metadata.allergens.eggs': 'true'}) is True


if __name__ == '__main__':
    unittest.main()
