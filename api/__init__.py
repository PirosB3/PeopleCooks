import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../libs/'))
import libs
from functools import wraps
from flask import Blueprint, Response, request
from simplejson import dumps

api_blueprint = Blueprint('api', __name__)

def apify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        status, name, result = f(*args, **kwargs)
        return Response(
            dumps({
                'name': name,
                'result': result
            }), status, mimetype='application/json')
    return wrapper

@api_blueprint.route('/getRecipeNames')
@apify
def getRecipeNames():
    return 200, 'getRecipeNames', libs.get_recipe_names()

@api_blueprint.route('/getIngredientNames')
@apify
def getIngredientNames():
    return 200, 'getIngredientNames', libs.get_ingredient_names()

@api_blueprint.route('/getRecipeBySlug')
@apify
def getRecipeBySlug():
    if 'slug' in request.values:
        recipe = libs.get_recipe_by_slug(request.values['slug'])
        if recipe:
            return 200, 'getRecipeBySlug', recipe
    return 404, 'getRecipeBySlug', {'error': 'recipe not found'}


