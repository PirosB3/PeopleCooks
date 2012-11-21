import libs
import simplejson
import urllib
import logging
logging.basicConfig()

from libs.parser import MarkdownParser

MANIFEST_FILE = 'https://dl.dropbox.com/u/2771940/PeopleCooks/mainfest.json'
logger = logging.getLogger(__file__)

def read_url(url):
    return urllib.urlopen(url).read()

def main():
    recipes = []
    manifest_list = simplejson.loads(read_url(MANIFEST_FILE))
    for recipe_url in manifest_list:
        try:
            recipe_md = read_url(recipe_url)
            recipe_obj = MarkdownParser(recipe_md)
            recipes.append(recipe_obj)
            logger.warning("Correctly imported '%s'" % recipe_obj['title'])
        except Exception, err:
            logger.error(str(err))

    # Get and import all ingredients
    libs.persistence.reset_all()
    for recipe in recipes:
        ingredients = []
        for ingredient, amount in recipe['ingredients'].iteritems():
            #print "ADD INGREDIENT: " + ingredient
            slug = libs.persistence.slugify(ingredient)
            libs.persistence.add_new_ingredient({ 'name' : ingredient, 'slug' : slug})
            #print "appending %s with %s: " % (libs.persistence.slugify(ingredient), amount)
            ingredients.append({
                'slug' : slug,
                'amount' : amount
            })
        #print recipe['steps'],
        #print ingredients
        libs.persistence.add_new_recipe({
            'title': recipe['title'],
            'slug': libs.persistence.slugify(recipe['title']),
            'description': recipe['description'],
            'steps': recipe['steps'],
            'ingredients': ingredients
        })


if __name__ == '__main__':
    main()
