"""
models.py

App Engine datastore models

"""

from google.appengine.ext import db

# Food entity contains a name and picture url stores as a text
# Food can be liked by multiple people and one person can like many foods
class Food(db.Model):
	food_name = db.StringProperty(required=True)
	food_picture = db.StringProperty(required=True)

class User(db.Model):
    # this id is facebook id
    id = db.IntegerProperty(required = True)
    username = db.StringProperty(required = True)
    foods = db.ListProperty(db.Key)