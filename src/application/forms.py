"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.db import model_form
from .models import User, Food

class UserForm(wtf.Form):
	id = wtf.TextField('Id', validators=[validators.Required()])
	username = wtf.TextField('Username', validators=[validators.Required()])
	foods = wtf.TextAreaField('Foods', validators=[validators.Required()])

class FoodForm(wtf.Form):
	name = wtf.TextField('Name', validators=[validators.Required()])
	food_picture = wtf.TextAreaField('Picture', validators=[validators.Required()])