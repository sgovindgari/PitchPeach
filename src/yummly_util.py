import string
import math
from random import shuffle,sample,randint
from operator import itemgetter
import requests
import json
from scipy import linalg, mat, dot
import numpy

# yummly credentials
# appid: 3e049aba
# key: ab364d21141b81e05e3ecf0b87f221ba
credentials = {'_app_id': '3e049aba', '_app_key': 'ab364d21141b81e05e3ecf0b87f221ba'}

def json_text_to_ingredients(text):
    ingredients_json = json.loads(text)
    ingredients = []
    for entry in ingredients_json:
        ingredients.append( entry['term'] )

    return sorted(ingredients)

def get_remote_ingredients_json_text():
    ingredients_jsonp = requests.get("http://api.yummly.com/v1/api/metadata/ingredient", params=credentials)
    ingredients_jsonp_text = ingredients_jsonp.text
    ingredients_json_text = ingredients_jsonp_text[ ingredients_jsonp_text.index(",") + 1 : ingredients_jsonp_text.rindex(")") ]
    return ingredients_json_text

def update_local_ingredients():
    f = open('ingredients.json', 'w')
    f.write(get_remote_ingredients_json_text().encode('utf8'))
    f.close()

def get_ingredients_remotally():
    return json_text_to_ingredients(get_remote_ingredients_json_text())

def get_ingredients_locally():
    f = file('ingredients.json', 'r')
    return json_text_to_ingredients(f.read().decode('utf8'))

def get_recipes():
    r = requests.get("http://api.yummly.com/v1/api/recipes", params=payload)
    rjson = json.loads(r.text)
    for ka,va in rjson.iteritems():
            print "k" + str(ka)
            print "v" + str(va)

    for m in rjson['matches']:
        print m['ingredients']

