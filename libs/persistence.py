# Import config file
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from settings import *
from pymongo import Connection

def _get_db():
    return Connection()[DATABASE_NAME]

def get_ingredient_names(db= None):
    db = db or _get_db()
    names = set()
    for c in db.recipes.find(fields=['ingredients.name']):
        for i in c['ingredients']:
            names.add(i['name'])
    return names

def get_recipe_names(db= None):
    db = db or _get_db()
    return map(lambda x: x['title'], db.recipes.find(fields=['title']))

def get_recipe_by_title(title, db= None):
    db = db or _get_db()
    return db.recipes.find_one({'title': title})

