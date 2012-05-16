import unittest
from flask import Flask

class PeopleCooksTestCase(unittest.TestCase):
    def test_local_settings(self):
        """ Assert that the local settings are read """
        app = Flask(__name__)
        app.config.from_object('settings')
        self.assertFalse(app.config['DEBUG'])

if __name__ == '__main__':
    unittest.main()
