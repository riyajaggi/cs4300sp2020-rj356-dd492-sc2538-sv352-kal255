import json
import numpy as np


def des(shows):

    stuff = []
    descript = json.load(open("datasets/p2/tv_shows_reviews_description.json"))

    for x in shows:
        if x in descript:
            d = descript[x]['description']
            stuff.append(d)
    return stuff

# 
# print(des(["Game of Thrones", "Friends"]))
