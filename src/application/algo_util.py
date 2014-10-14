import string
import math
from random import shuffle,sample,randint
from operator import itemgetter
from scipy import linalg, mat, dot
import numpy
#import yummly_util
####### CHANGE

import yummly_backup1010 as yummly_util

def get_users():
    # yummly_util.update_local_ingredients() # run to update local data
    ingredients_list = yummly_util.get_ingredients_locally()
    num_ingredients = len(ingredients_list)

    freqency_vector = numpy.zeros(num_ingredients)

    range_of_ids = 20 # Without database setup, working with fake accounts for now.
    rjson = yummly_util.get_n_recipes(n=100)
    recipes = []
    for m in rjson['matches']:
        recipes.append((m['id'],m["ingredients"]))

    users = {}
    
    for user_id in range(range_of_ids):

        user_vector = numpy.zeros(num_ingredients)
        likes = []
        dislikes = []
        mehs = []

        u_recipes = sample(recipes,randint(4,20))
        u_pref = map(lambda (fid,fings):(fid,fings,randint(-1,1)),u_recipes)

        for (fid,fings,score) in u_pref:
            if score == 1:
                likes.append(fid)
            elif score == -1:
                dislikes.append(fid)
            else:
                mehs.append(fid)
            
            for ingredient in fings:
                i = ingredients_list.index(ingredient)
                user_vector[i] = user_vector[i] + score
                freqency_vector[i] = freqency_vector[i] + 1

        users[user_id] = {'likes':set(likes),'dislikes':set(dislikes),'mehs':set(mehs),'vector':user_vector}

    # normalize vectors
    numpy.seterr(all='ignore')
    for user_id,attributes in users.iteritems():
        users[user_id]['vector'] = numpy.divide(users[user_id]['vector'],freqency_vector)
        where_are_NaNs = numpy.isnan(users[user_id]['vector'])
        users[user_id]['vector'][where_are_NaNs] = 0

    return users

def print_current_users():
    users = get_users()
    for user_id,attributes in users.iteritems():
        print "User:" + str(user_id)
        for attribute,info in attributes.iteritems():
            print  "\t>>>" + attribute + ":" + str(info)

def cos_sim(a,b):
    return dot(a,b.T)/linalg.norm(a)/linalg.norm(b)

def get_recommendations(user_id):
    users = get_users() 

    def get_closeness(user_id1,user_id2):
        return cos_sim(users[user_id1]['vector'],users[user_id2]['vector'])

    def get_unique_recipe_ids(user_id1,user_id2):
        return list(users[user_id2]['likes'] - users[user_id1]['likes'] - users[user_id1]['dislikes'] - users[user_id1]['mehs'])

    if not users.has_key(user_id):
        return None
    
    other_users = users.keys()
    other_users.remove(user_id)

    def get_closeness_to_cur(other_user_id):
        return (other_user_id,get_closeness(user_id,other_user_id))

    id_score_pairs = map(get_closeness_to_cur,other_users)
    ranked_id_score_pairs = sorted(id_score_pairs,key=itemgetter(1),reverse=False)

    num_recommendations = 3
    recommendations = []
    sim_user_id_index = 0
    while len(recommendations) < num_recommendations: 
        unique_recipe_ids = get_unique_recipe_ids(user_id,ranked_id_score_pairs[sim_user_id_index][0])
        recipe_urls = yummly_util.get_recipe_urls(unique_recipe_ids)
        recommendations.extend( shuffle( recipe_urls ) )
        sim_user_id_index = sim_user_id_index + 1
    
    return recommendations[:num_recommendations]
    
get_recommendations(2)
