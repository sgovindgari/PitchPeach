"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb

# TODO - Remove this
class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

# Food entity contains a name and picture url stores as a text
# Food can be liked by multiple people and one person can like many foods
class Food(ndb.Model):
	food_name = ndb.StringProperty(required=True)
	food_picture = ndb.TextProperty(required=True)
	users = ndb.StructuredProperty(User, repeated=True)

class User(ndb.Model):
    # this id is facebook id
    id = ndb.IntegerProperty(required = True)
    username = ndb.StringProperty(required = True)
    email = ndb.EmailProperty()
    passwd = ndb.StringProperty()
    foods = ndb.StructuredProperty(Food, repeated=True)