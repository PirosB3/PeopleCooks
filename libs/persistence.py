# Import config file
import sys, os, re
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from functools import wraps
from settings import *
from pymongo import Connection
from bson.objectid import ObjectId
from unicodedata import normalize

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

def slugify(value):
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)

def db_name_or_default(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'db' not in kwargs:
            kwargs['db'] = Connection(MONGO_ADDRESS, MONGO_PORT)[DATABASE_NAME]
        return f(*args, **kwargs)
    return wrapper

@db_name_or_default
def get_ingredient_names(db):
    names = set()
    for c in db.recipes.find(fields=['ingredients.name']):
        for i in c['ingredients']:
            names.add(i['name'])
    return list(names)

@db_name_or_default
def get_recipe_names(db):
    return map(lambda x: {'title': x['title'], 'slug': x['_slug'] }, db.recipes.find(fields=['title', '_slug']))

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
    if '_slug' not in recipe:
        recipe['_slug'] = slugify(recipe['title'])
    return bool(db.recipes.insert(recipe))
