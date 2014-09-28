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
from application import yummly_util

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

# gets more foods when More is clicked on the profile page
@app.route('/getMoreQuiz', methods=['GET', 'POST'])
def getMoreQuiz():
    userid = request.json['uid']
    # get the user and save the preferences of this user
    q = db.GqlQuery("SELECT * "
                        "FROM User "
                        "WHERE id = :1", userid)
    user = q[0]
    preferences = request.json['pref']
    old_lst = cache.get("old_lst")
    food_lst = []
    if preferences and old_lst:
        for i in range(4):
            food = Food(food_id = old_lst[i][0], food_pref = preferences[i])
            food_lst.append(food)
    user.foods = food_lst
    user.put()

    # get more recipes
    lst = yummly_util.get_random_recipes()
    pic_url = []
    for recipe_id,recipe_url in lst:
        pic_url.append(recipe_url)
    return render_template('survey.html', lst = pic_url)

#TODO - Fix this
@app.route('/getMoreOne')
@app.route('/pitch')
@app.route('/pitch/<lst>')
def getMoreOne(lst=[]):
    lst = yummly_util.get_random_recipes()
    return render_template('pitch.html', lst = lst)

@app.route('/survey')
@app.route('/survey/<lst>')
def survey(lst=[]):
    lst = yummly_util.get_random_recipes()
    cache.set("old_lst", lst)
    pic_url = []
    for recipe_id,recipe_url in lst:
        pic_url.append(recipe_url)
    return render_template('survey.html', lst = pic_url)

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
