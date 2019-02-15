"""
api_test.py
Unit test for REST-API.

"""
import unittest
from src import app as flaskapp
from flask import jsonify


class PyTest(unittest.TestCase):
    """
    Test class for api

    """

    def setUp(self):
        self.app = flaskapp.app.test_client()

    def test_get_request_ok(self):
        """
        """
        response = self.app.get('/v1/messages')
        self.assertEqual(response.status_code, 200)

    def test_post_not_json(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data='not json')
        self.assertEqual(response.status_code, 400)

    def test_post_has_location_header(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data=jsonify({'message': 'this message',
                                                'recipient-id': 123}))
        self.assertIn('Location', response.headers)

    def tearDown(self):
        """
        """
        self.app = None


if __name__ == '__main__':
    unittest.main()
