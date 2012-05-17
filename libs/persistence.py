# Import config file
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from settings import *
from pymongo import Connection

def get_ingredient_names(db= Connection()[DATABASE_NAME]):
    names = set()
    for c in db.recipes.find(fields=['ingredients.name']):
        for i in c['ingredients']:
            names.add(i['name'])
    return names

def get_recipe_names(db= Connection()[DATABASE_NAME]):
    return map(lambda x: x['title'], db.recipes.find(fields=['title']))

def get_recipe_by_title(title, db= Connection()[DATABASE_NAME]):
    return db.recipes.find_one({'title': title})

def get_recipe_names_by_ingredient(name, db= Connection()[DATABASE_NAME]):
    return map(lambda x: x['title'], db.recipes.find({'ingredients.name': name}, fields=['title']))


