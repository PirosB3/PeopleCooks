import os
import unittest
import pymongo
import libs
from flask import Flask
from simplejson import loads
from settings import *

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures.json')
TEST_DATABASE = 'test'

class PersistentStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.c = pymongo.Connection(MONGO_ADDRESS, MONGO_PORT)
        self.db = self.c[TEST_DATABASE]
        f = loads(open(FIXTURES).read())
        for key, value in f.iteritems():
            self.db[key].insert(value)

    def test_get_all_ingredient_names(self):
        ingredient_names = libs.get_ingredient_names(db= self.db)
        self.assertEqual(6, len(ingredient_names))

    def test_get_all_recipe_names(self):
        recipe_names = libs.get_recipe_names(db= self.db)
        self.assertEqual(3, len(recipe_names))

    def test_get_recipe_by_title(self):
        recipe = libs.get_recipe_by_title('Linguine al pesto', db= self.db)
        self.assertTrue(type(recipe) == dict)

        recipe = libs.get_recipe_by_title('abra cadabra', db= self.db)
        self.assertIsNone(recipe)

    def test_get_recipe_names_by_ingredient(self):
        recipes = libs.get_recipe_names_by_ingredient('Pepper', db= self.db)
        self.assertEqual(2, len(recipes))

    def test_add_recipe(self):
        new_recipe =  {
         "title":"My new Recipe!",
         "_slug": "my-new-recipe",
         "description":"Devo chiedere?",
         "steps":[
            "take the seafood and wash it well",
            "start toasking the seafood with a bit of oil"
         ],
         "ingredients":[
            {
               "name":"Clambs",
               "amount":"20kg"
            }
           ]
         }
        self.assertTrue(libs.add_new_recipe(new_recipe, db= self.db))
        self.assertTrue(libs.get_recipe_by_title(new_recipe['title']))

    def tearDown(self):
        self.db.recipes.remove()

if __name__ == '__main__':
    unittest.main()
