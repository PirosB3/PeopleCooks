import os
import unittest
import pymongo
import libs
from flask import Flask
from simplejson import loads

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures.json')
TEST_DATABASE = 'test'


class PeopleCooksTestCase(unittest.TestCase):
    db_required = False
    c = None

    def setUp(self):
        if not self.c and self.db_required:
            self.c = pymongo.Connection()
            self.db = self.c[TEST_DATABASE]
            self._load_fixtures()

    def tearDown(self):
        if self.c:
            self._drop_fixtures()

    def _drop_fixtures(self):
        self.c.drop_database(TEST_DATABASE)

    def _load_fixtures(self):
        f = loads(open(FIXTURES).read())
        for key, value in f.iteritems():
            self.db[key].insert(value)

class PeopleCooksTestCase(PeopleCooksTestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object('settings')

    @unittest.skip("Can be tweaked in local settings")
    def test_local_settings(self):
        """ Assert that the local settings are read """
        self.assertFalse(self.app.config['DEBUG'])

class PersistentStoreTestCase(PeopleCooksTestCase):
    db_required = True

#    def test_get_all_recipe_names(self):
#        recipe_names = libs.Persistence.get_recipe_names()
#        self.assertEqual(3, len(recipe_names))

    def test_get_all_ingredient_names(self):
        ingredient_names = libs.Persistence.get_ingredient_names(self.db)
        self.assertEqual(7, len(ingredient_names))


if __name__ == '__main__':
    unittest.main()
