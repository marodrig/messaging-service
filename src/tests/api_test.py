"""
api_test.py
Unit test for REST-API.

"""
import unittest
from src import app as flaskapp
from flask import jsonify
import json


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

    def test_get_request_only_accept_json(self):
        """
        """
        response = self.app.get('/v1/messages',
                                headers={
                                    'Accept': 'text/html'})
        self.assertEqual(406, response.status_code)

    def test_get_request_slice_result(self):
        """
        """
        response = self.app.get('/v1/messages',
                                query_string={
                                    'start-idx': '0',
                                    'stop-idx': '6'})
        self.assertEqual(200, response.status_code)

    def test_post_error_code_when_not_json(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data='not json')
        self.assertEqual(response.status_code, 400)

    def test_post_error_message_on_wrong_content(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data='not json')
        self.assertIn('error', response.json)

    def test_post_has_location_header(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data=json.dumps({
                                     'message': 'this message',
                                     'recipient-id': '123'}),
                                 headers={
                                     'content-type': 'application/json'})
        self.assertIn('Location', response.headers)

    def test_post_returns_201(self):
        """
        """
        response = self.app.post('/v1/messages',
                                 data=json.dumps({
                                     'message': 'testing',
                                     'recipient-id': '562'}),
                                 headers={
                                     'content-type': 'application/json'})
        self.assertEqual(201, response.status_code)

    def test_delete_success(self):
        """
        """
        response = self.app.delete('/v1/messages',
                                   query_string={
                                    'messages-id': '1'})
        self.assertEqual(204, response.status_code)

    def test_put_success(self):
        """
        """
        response = self.app.put('/v1/messages',
                                 json={
                                     'message': 'message'
                                 })
        self.assertEqual(200, response.status_code)
        
    def tearDown(self):
        """
        """
        self.app = None


if __name__ == '__main__':
    unittest.main()
