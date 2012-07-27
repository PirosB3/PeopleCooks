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
    return map(lambda x: {'name': x['name'], 'slug': x['_slug'] }, db.ingredients.find(fields=['name', '_slug']))

@db_name_or_default
def get_recipe_names(db):
    return map(lambda x: {'title': x['title'], 'slug': x['_slug'] }, db.recipes.find(fields=['title', '_slug']))

@db_name_or_default
def get_recipe_by_slug(slug, db):
    return db.recipes.find_one({'_slug': slug})

@db_name_or_default
def get_ingredient_by_slug(slug, db):
    try:
        ingredient = db.ingredients.find({'_slug': slug})[0]
    except IndexError:
        return False
    ingredient['recipes'] = [recipe['_slug'] for recipe in db.recipes.find({'ingredients.slug': ingredient['_slug']}, {'_slug': 1})]
    return ingredient


@db_name_or_default
def add_new_recipe(recipe, db):
    if '_slug' not in recipe:
        recipe['_slug'] = slugify(recipe['title'])
    for ingredient in recipe['ingredients']:
        if db.ingredients.find({'_slug': ingredient['slug']}).count() != 1:
            return False
    return bool(db.recipes.insert(recipe))
