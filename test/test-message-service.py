"""
Tests for messagin service

"""
import os
from src import message-service as flaskapp
import unittest
import tempfile


class FlaskTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.db_fd, flaskapp.app.config['DATABASE'] = tempfile.mkstemp()
        src.app.testing = True
        self.app = flaskapp.app.test_client()
        with flaskapp.app.app_context():
            flaskapp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(src.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
