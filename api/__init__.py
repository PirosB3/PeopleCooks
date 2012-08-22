import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../libs/'))
import libs
from functools import wraps
from flask import Blueprint, Response, request
from simplejson import dumps, JSONEncoder
from bson.objectid import ObjectId

api_blueprint = Blueprint('api', __name__)

class ObjectIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return repr(obj)
        return super(ObjectIDEncoder, self).default(obj)

def apify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        status, result = f(*args, **kwargs)
        return Response(
            dumps(result, cls= ObjectIDEncoder), status, mimetype='application/json'
        )
    return wrapper

@api_blueprint.route('/recipes')
@apify
def getRecipeNames():
    return 200, libs.get_recipe_names()

@api_blueprint.route('/ingredients')
@apify
def getIngredientNames():
    return 200, libs.get_ingredient_names()

@api_blueprint.route('/recipes/<slug>')
@apify
def getRecipeBySlug(slug):
    if slug:
        recipe = libs.get_recipe_by_slug(slug)
        if recipe:
            return 200, recipe
    return 404, {'error': 'recipe not found'}

@api_blueprint.route('/ingredients/<slug>')
@apify
def getIngredientbySlug(slug):
    if slug:
        ingredient= libs.get_ingredient_by_slug(slug)
        if ingredient:
            return 200, ingredient
    return 404, {'error': 'ingredient not found'}
