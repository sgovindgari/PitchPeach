"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from models import User, Food
import facebook


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['POST'])
def login(uid, username):
    user_form = UserForm()
    if user_form.validate_on_submit():
        user = User(user_form.username)
        user.put()

@app.route('/survey')
def survey():
    return render_template('survey.html')

def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

#############################################

# FOOD RECOMMENDATION SYSTEM CODE GOES HERE

#############################################

# Given user id gets the list of foods this user likes
def get_foods(user_id):
    user = User.get_by_id(user_id)
    return user.food_list

################################################

