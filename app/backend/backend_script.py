import re
import os
import numpy as np
import json
import app.backend.adhoc_similarity as adhoc_similarity
import pickle
# import scripts.edit_distance as ed

with open('./datasets/p2/tv_shows_to_index_final.json') as a_file:
  tv_shows_to_index = json.load(a_file)

def capitalize_show_name(show):
    """
    Returns the name of the given show capitalized

    Parameter show: a show title
    Precondition: a non-empty string
    """
    for capitalized_show, _ in tv_shows_to_index.items():
        if capitalized_show.lower() == show.lower():
           return capitalized_show

def jaccardRanking(show, N=3):
    """
    given an input string show name, return a ranked list of the N most similar shows using the jaccSimMat (using N = 3 for demo)
    """
    jaccSimMat = np.load("MainModel.npy")

    with open("shows_lst.txt", "r") as json_file:
        shows = json.load(json_file)
    
    if not show in shows:
        return [] 

    showInd = shows.index(show)
    scores = jaccSimMat[showInd]

    result = sorted(range(len(scores)), key=lambda substr: scores[substr])[(-N-1): -1]
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

    if show.lower() not in list(description_dict.keys()):
        return []

    result = description_dict[show.lower()][:N]

    return result


def reviewRanking(show, N = 3):
    """
    Returns a ranked list of shows and their cosine similarity scores

    Parameters: 
    show - name of tv show to search for (string)
    N - number of shows returned (int)
    """

    review_dict = pickle.load( open( "datasets/p2/review_similarity.p", "rb" ) )
    review_dict = {k:v for k, v in review_dict.items()}
    review_show = capitalize_show_name(show)

    if review_show not in list(review_dict.keys()):
        return [] 
    result = review_dict[review_show][:N]

    return result

# print(reviewRanking("friends"))
    
def final_search(query_show, n, free_search=None, genre=None):
    """
    Returns: A ranked list of similar shows based on reviews, descriptions, 
    transcripts,and other optional arguments.

    Parameter query_show: the given show
    Precondition: a non-empty string

    Parameter n: the number of similar shows to output
    Precondition: an integer

    (Optional) Parameter free_search: a query with extra information to include 
    in the search 
    Precondition: (Default is None) None or non-empty string

    (Optional) Parameter genre: a query genre 
    Precondition: (Default is None) None or non-empty string representation of 
    a valid genres
    """

    weights = {
        'transcripts' : .10 ,
        'reviews' : .45,
        'descriptions' : .45,
        'genre' : 0,
        'free search' : 0,
    }
    # query_show = ed.edit_search(query_show)[0][1] # rn it does edit distance on everything, we want only on the shows that are not in the index json

    results = []
    tv_sim_score_sum = {}
    transcripts_ranking = jaccardRanking(query_show, n) # list of tv shows
    reviews_ranking = reviewRanking(query_show, 10) # list of tv shows and sim scores
    if reviews_ranking is None:
        reviews_ranking = []
    desc_ranking = descriptionRanking(query_show, 10)
    # print("Description")
    # print(desc_ranking)
    free_search_ranking = []
    if free_search is not None:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(free_search, n*2) # list of tv shows and sim scores
        weights['transcripts'] = weights['transcripts'] - .05
        weights['reviews'] =  weights['reviews'] - .05
        weights['descriptions'] = weights['descriptions'] - .2
        weights['free search'] = .30
        for show, score in free_search_ranking:
            if show in tv_sim_score_sum:
                tv_sim_score_sum[show] += weights['free search'] * score * 100
            else:
                tv_sim_score_sum[show] = weights['free search'] * score * 100
    # genre_search_ranking = []
    # if genre is not None:
    #   genre_ranking =   
        # weights['transcripts'] = weights['transcripts'] - .05
        # weights['reviews'] =  weights['reviews'] - .05
        # weights['descriptions'] = weights['descriptions'] - .05
        # weights['free search'] = weights['free search'] - .05
        # weights['genre'] = .2
        # for show, score in genre_ranking:
        #     if show in tv_sim_score_sum:
        #         tv_sim_score_sum[show] += weights['genre'] * score * 100
        #     else:
        #         tv_sim_score_sum[show] = weights['genre'] * score * 100
    
    for i in range(len(transcripts_ranking)):
        show = transcripts_ranking[i]
        score = (.5 - ((i+1)/100))
        if show in tv_sim_score_sum:
            tv_sim_score_sum[show] += weights['transcripts'] * score * 100
        else:
            tv_sim_score_sum[show] = weights['transcripts'] * score * 100
    for show, score in reviews_ranking:
        if show in tv_sim_score_sum:
            tv_sim_score_sum[show] += weights['reviews'] * score * 100
        else:
            tv_sim_score_sum[show] = weights['reviews'] * score * 100
    for show, score in desc_ranking:
        if show in tv_sim_score_sum:
            tv_sim_score_sum[show] += weights['descriptions'] * score * 100
        else:
            tv_sim_score_sum[show] = weights['descriptions'] * score * 100

    tv_sim_score_sum = {k: v for k, v in sorted(tv_sim_score_sum.items(), key=lambda item: -item[1])}
    # print(tv_sim_score_sum)
    index = 0
    for key, _ in tv_sim_score_sum.items():
        if capitalize_show_name(key) is not None:
            results.append(capitalize_show_name(key))
            index += 1
        if index == n:
            break
    return results

# TESTS
# the_walking_dead_results = final_search("The Walking Dead", 10)
# print(the_walking_dead_results)
# sherlock_results = final_search("Sherlock", 10, "dogs")
# print(sherlock_results)
# its_always_sunny_results = final_search("It's Always Sunny in Philadephia", 10) # no reviews, no description, no transcripts in transcript2
# print(its_always_sunny_results) 
# insecure_results = final_search("insecure", 10, "Los Angeles")
# print(insecure_results)

# test2 = final_search("Sherlock", 10, genre="Animation")
# print(test2)