"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

#post data
app.add_url_rule('/post', 'post', view_func=views.post)

# Say hello
app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

