import os
import unittest
import pymongo
import libs
from flask import Flask
from simplejson import loads

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures.json')
TEST_DATABASE = 'test'

class PersistentStoreTestCase(unittest.TestCase):
    def setUp(self):
        self.c = pymongo.Connection()
        self.db = self.c[TEST_DATABASE]
        self._load_fixtures()

    def tearDown(self):
        self.c.drop_database(TEST_DATABASE)

    def _load_fixtures(self):
        f = loads(open(FIXTURES).read())
        for key, value in f.iteritems():
            self.db[key].insert(value)

    def test_get_all_ingredient_names(self):
        ingredient_names = libs.get_ingredient_names(self.db)
        self.assertEqual(6, len(ingredient_names))

    def test_get_all_recipe_names(self):
        recipe_names = libs.get_recipe_names(self.db)
        self.assertEqual(3, len(recipe_names))

    def test_get_recipe_by_title(self):
        recipe = libs.get_recipe_by_title('Linguine al pesto', db= self.db)
        self.assertTrue(type(recipe) == dict)

        recipe = libs.get_recipe_by_title('abra cadabra', db= self.db)
        self.assertIsNone(recipe)


if __name__ == '__main__':
    unittest.main()
