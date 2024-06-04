import unittest
from unittest.mock import MagicMock
from pycurl import PyCurl


class TestPyCurl(unittest.TestCase):

    def setUp(self):
        self.curl = PyCurl()

    def test_get_request(self):
        expected_response = {'status_code': 200, 'headers': {'Content-Type': 'text/html; charset=UTF-8'}}
        self.curl.exec = MagicMock(return_value=None)
        self.curl.get_response = MagicMock(return_value=expected_response)
        response = self.curl.get('https://vimm.net')
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
