import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import unittest
import pymongo
import libs
from flask import Flask
from simplejson import loads
from settings import *
from libs.persistence import get_database
from libs.parser import MarkdownParser

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_FIXTURES = os.path.join(TEST_ROOT, 'fixtures.json')
MD_FIXTURES = os.path.join(TEST_ROOT, 'fixture.md')

class PersistentStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.c = pymongo.Connection(MONGO_URL_TESTING)
        self.db = self.c[get_database(MONGO_URL_TESTING)]
        f = loads(open(DB_FIXTURES).read())
        for key, value in f.iteritems():
            self.db[key].insert(value)

    def test_get_all_ingredient_names(self):
        ingredient_names = libs.get_ingredient_names(db= self.db)
        self.assertEqual(6, len(ingredient_names))

    def test_get_all_recipe_names(self):
        recipe_names = libs.get_recipe_names(db= self.db)
        self.assertEqual(3, len(recipe_names))

    def test_reset_all(self):
        libs.reset_all(db = self.db)
        self.assertEqual(0, len(libs.get_ingredient_names(db= self.db)))
        self.assertEqual(0, len(libs.get_recipe_names(db= self.db)))

    def test_ingredient_not_added_twice(self):
        ingredients = len(libs.get_ingredient_names(db= self.db))
        libs.add_new_ingredient({ "name" : "Pepper"}, db= self.db)
        self.assertEqual(ingredients, len(libs.get_ingredient_names(db= self.db)))

    def test_get_recipe_by_slug(self):
        recipe = libs.get_recipe_by_slug('linguine-al-pesto', db= self.db)
        self.assertTrue(type(recipe) == dict)

        recipe = libs.get_recipe_by_slug('abra cadabra', db= self.db)
        self.assertIsNone(recipe)

    def test_get_recipe_names_by_ingredient(self):
        recipes = libs.get_recipe_names_by_ingredient('pepper', db= self.db)
        self.assertEqual(2, len(recipes))

    def test_add_recipe(self):
        new_recipe =  {
         "title":"My new Recipe!",
         "_slug": "my-new-re\cipe",
         "description":"Devo chiedere?",
         "steps":[
            "take the seafood and wash it well",
            "start toasking the seafood with a bit of oil"
         ],
         "ingredients":[
            {
               "slug":"clambs",
               "amount":"20kg"
            }
           ]
         }
        self.assertTrue(libs.add_new_recipe(new_recipe, db= self.db))
        self.assertTrue(libs.get_recipe_by_slug(new_recipe['_slug'], db= self.db))

    def test_get_recipe_names_by_ingredient(self):
        ingredient = libs.get_ingredient_by_slug('pepper', db= self.db)
        self.assertTrue(ingredient)
        self.assertEqual('Pepper' ,ingredient['name'])
        self.assertEqual(2, len(ingredient['recipes']))

    def test_add_ingredient(self):
        new_ingredient = {
            "name" : "Gnocchi"
        }
        self.assertTrue(libs.add_new_ingredient(new_ingredient, db= self.db))
        self.assertTrue(libs.get_ingredient_by_slug('gnocchi', db= self.db))

    def tearDown(self):
        self.db.recipes.remove()
        self.db.ingredients.remove()

class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = open(MD_FIXTURES, 'r')

    def test_it_should_read_directives(self):
        mdp = MarkdownParser(self.test_file.read())
        self.assertEqual(mdp['title'], "Spaghetti alla carbonara")
        self.assertEqual(mdp['lorem'], "Ipsum")
        self.assertEqual(mdp['description'], "This page lets you create HTML by entering text in a simple format that's easy to read and write.")

    def test_it_should_read_lists(self):
        mdp = MarkdownParser(self.test_file.read())
        self.assertEqual(len(mdp['ingredients']), 3)
        self.assertEqual(mdp['ingredients'][0], 'Spaghetti')

    def test_it_should_read_dicts(self):
        mdp = MarkdownParser(self.test_file.read())
        self.assertEqual(len(mdp['dictionary'].keys()), 3)
        self.assertEqual(mdp['dictionary']['Hello'], 'World')
        self.assertEqual(mdp['dictionary']['First'], 'Second')

    def test_return_none_if_not_found(self):
        mdp = MarkdownParser(self.test_file.read())
        self.assertEqual(None, mdp['unknown'])

if __name__ == '__main__':
    unittest.main()
