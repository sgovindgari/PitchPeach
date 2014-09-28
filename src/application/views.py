"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, jsonify, render_template, flash, url_for, redirect

from flask_cache import Cache
from google.appengine.ext import db
import json
from application import app
from decorators import login_required, admin_required
from models import User, Food
import facebook

from forms import UserForm, FoodForm

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/post', methods=['POST'])
def post():
    user_id = request.json['uid']
    username = request.json['username']
    food_list = []
    if user_id and username:
        form = UserForm()
        q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE username = :1", username)
        if q.count() > 0:
            flash("User already exists")
            return request.json['uid']
        new_user = User(id = int(user_id), username = username, foods = food_list)
        new_user.put()
    return request.json['uid']

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
