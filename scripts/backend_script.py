import re
import os
import numpy as np
import json
import pickle

def jaccardRanking(show, N=3):
    """
    given an input string show name, return a ranked list of the N most similar shows using the jaccSimMat (using N = 3 for demo)
    """
    jaccSimMat = np.load("MainModel.npy")

    with open("shows_lst.txt", "r") as json_file:
        shows = json.load(json_file)

    showInd = shows.index(show)
    scores = jaccSimMat[showInd]

    result = sorted(range(len(scores)), key=lambda substr: scores[substr])[
        (-N-1): -1]
    result.reverse()

    ranking = []
    for x in result:
        name = shows[x]
        ranking.append(name)

    # print(ranking)
    return ranking

# jaccardRanking ("Friends", 3)
# print(jaccardRanking("Criminal Minds"))

def descriptionRanking(show, N = 3):
    """
    Returns a ranked list of shows and their cosine similarity scores

    Parameters: 
    show - name of tv show to search for (string)
    N - number of shows returned (int)
    """

    description_dict = pickle.load( open( "datasets/p2/description_similarity.p", "rb" ) )
    description_dict = {k.lower():v for k, v in description_dict.items()}

    result = description_dict[show.lower()][:N]

    return result
