import unittest

from pyvimond.utils import create_api_metadata


class UtilsTest(unittest.TestCase):

    def test_create_api_metadata(self):
        metadata = {
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }

        self.assertEqual({
            'entries': {
                'foo': [{'value': True, 'lang': '*'}],
                'bar': [{'value': 'very bar', 'lang': '*'}],
                'baz': [{'value': 42, 'lang': '*'}],
            },
            'empty': True
        }, create_api_metadata(metadata))


if __name__ == '__main__':
    unittest.main()
