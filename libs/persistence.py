# Import config file
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from functools import wraps
from settings import *
from pymongo import Connection

def db_name_or_default(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'db' not in kwargs:
            kwargs['db'] = Connection()[DATABASE_NAME]
        return f(*args, **kwargs)
    return wrapper

@db_name_or_default
def get_ingredient_names(db):
    names = set()
    for c in db.recipes.find(fields=['ingredients.name']):
        for i in c['ingredients']:
            names.add(i['name'])
    return names

@db_name_or_default
def get_recipe_names(db):
    return map(lambda x: x['title'], db.recipes.find(fields=['title']))

@db_name_or_default
def get_recipe_by_title(title, db):
    result = db.recipes.find_one({'title': title})
    if result:
        del result['_id']
    return result

@db_name_or_default
def get_recipe_names_by_ingredient(name, db):
    return map(lambda x: x['title'], db.recipes.find({'ingredients.name': name}, fields=['title']))

@db_name_or_default
def add_new_recipe(recipe, db):
    return bool(db.recipes.insert(recipe))
