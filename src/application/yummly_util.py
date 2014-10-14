import requests
import json
from random import randint
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

def get_recipe_json(id_num):
    r = requests.get("http://api.yummly.com/v1/api/recipe/"+id_num, params=credentials.items())
    return json.loads(r.text)

def get_recipe_urls(recipe_ids):
    recipe_jsons = map(get_recipe_json,recipe_ids)

    id_url_pairs = []
    for rj in recipe_jsons:
        #print "ID:" +str(rj_id)
        for image in rj['images']:
            #print "IMAGE"
            imageSizes = sorted(image['imageUrlsBySize'])
            if len(imageSizes) >= 1:
                #print "SIZE:" + str(imageSizes[0]) + "LARGEST URL:" + str(image['imageUrlsBySize'][imageSizes[0]])
                
                rj_id = rj['id']
                rj_url = image['imageUrlsBySize'][imageSizes[0]]
                rj_name = rj['name']
                id_url_pairs.append((rj_id,rj_url,rj_name))            

    return id_url_pairs

def get_n_recipes(n=4):
    maxResult = max(10,n)
    start=randint(0,100000)
    extra_criteria = {'requirePictures':'true','maxResult':str(maxResult),'start':str(start)}
    r = requests.get("http://api.yummly.com/v1/api/recipes", params=dict(credentials.items() + extra_criteria.items()))
    rjson = json.loads(r.text)
    return rjson

def get_random_recipes(num = 4):
    rjson = get_n_recipes(num)
    
    recipe_ids = []
    for m in rjson['matches']:
        recipe_ids.append(m['id'])

    return get_recipe_urls(recipe_ids[:num])


# print get_random_recipes()
