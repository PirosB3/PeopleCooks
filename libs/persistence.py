# Import config file
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from settings import *
from pymongo import Connection

class Persistence(object):
    db = None

    def _get_db(self):
        if not self.db:
            db = Connection()[DATABASE_NAME]
        return self.db

    @classmethod
    def get_ingredient_names(db = None):
        db = db or self._get_db()
        return db.recipes.find({}, {'ingredients.name': 1})
