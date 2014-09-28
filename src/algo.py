import string
import math
from random import shuffle,sample,randint
from operator import itemgetter

# yummly credentials
# appid: 3e049aba
# key: ab364d21141b81e05e3ecf0b87f221ba
import requests

def read(fileName):
    text_file = open(fileName, "r")
    lines = text_file.readlines()

    data = []
    for line in lines:
        data.append( line[8:].strip() )
    text_file.close()

    return data

foodList = read("list_of_list_of_foods.txt")


users = {}
for user_id in range(200):
    shuffle(foodList)

    num_entries = randint(20,50)
    likes_i = randint(0,num_entries)
    dislikes_i = randint(likes_i,num_entries)

    likes = foodList[:likes_i]
    dislikes = foodList[likes_i:dislikes_i]
    mehs = foodList[dislikes_i:num_entries]
    
    users[user_id] = {'likes':set(likes),'dislikes':set(dislikes),'mehs':set(mehs)}

for user_id,attributes in users.iteritems():
    print "User:" + str(user_id)
    for attribute,info in attributes.iteritems():
        print  "\t>>>" + attribute + ":" + str(info)

def get_closeness(user_id1,user_id2):
    like_score = len(users[user_id1]['likes'].intersection(users[user_id2]['likes']))
    dislike_score = len(users[user_id1]['dislikes'].intersection(users[user_id2]['dislikes']))
    mehs_score = len(users[user_id1]['mehs'].intersection(users[user_id2]['mehs']))
    return like_score + dislike_score + mehs_score

def get_recommendations(user_id):
    if not users.has_key(user_id):
        return None
    
    other_users = users.keys()
    other_users.remove(user_id)

    def get_closeness_to_cur(other_user_id):
        return (other_user_id,get_closeness(user_id,other_user_id))

    id_score_pairs = map(get_closeness_to_cur,other_users)
    ranked_id_score_pairs = sorted(id_score_pairs,key=itemgetter(1),reverse=True)

    print ranked_id_score_pairs
    #num_recommendations = 4
    #recommendations = []
    #while len(recommendations) < num_recommendations:

get_recommendations(2)

