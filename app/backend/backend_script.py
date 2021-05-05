import re
import os
import numpy as np
import json
import app.backend.adhoc_similarity as adhoc_similarity
import pickle
import app.backend.edit_distance as ed

with open('./datasets/p2/tv_shows_to_index_final.json') as a_file:
  tv_shows_to_index = json.load(a_file)
with open('./datasets/p2/merged_tv_shows_final.json') as merged_tv_file:
  merged_tv_shows = json.load(merged_tv_file)

def capitalize_show_name(show):
    """
    Returns the name of the given show capitalized

    Parameter show: a show title
    Precondition: a non-empty string
    """
    if show is not None:
        for capitalized_show, _ in tv_shows_to_index.items():
            if capitalized_show.lower() == show.lower():
                return capitalized_show


def jaccardRanking(show, N=3):
    """
    given an input string show name, return a ranked list of the N most similar shows 
    using the jaccSimMat (using N = 3 for demo)
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

    description_dict = pickle.load( open( "datasets/p2/description_similarity_100.p", "rb" ) )
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
    
def select_weights(query_show, free_search, various_weight_combos):
    """
    Returns weights represented for the final result similarity score
    based on the query inputs

    Parameter query_show: the given show
    Precondition: None or non-empty string

    Parameter free_search: a query with extra information to include in the 
    search 
    Precondition: None or non-empty string

    Parameter various_weight_combos: a dictionary with different weight combinations
    Precondition: a dictionary with at least three keys: "show & free_search", 
    "just show", and "just free search" and values must be floats between 0 and 1 
    """
    weights = {}
    if query_show and free_search:
        weights = various_weight_combos['show & free search']
    elif query_show:
        weights = various_weight_combos['just show']
    elif free_search:
        weights = various_weight_combos['just free search']
    return weights
    
def final_search(slider_weights, query_show=None, n=10, free_search=None, genre=None, 
streaming_platform=None, not_like_show=None, not_like_free_search=None):
    """
    Returns: A ranked list of similar shows based on reviews, descriptions, 
    transcripts,and other optional arguments.

    Parameter slider_weights: a dictionary with input weights for sliders
    Precondition: a dictionary with four keys: "similarity",  "not like", 
    "keyword", and "tv shows" and values must be floats between 0 and 1

    (Optional if free_search is not None) 
    Parameter query_show: the given show
    Precondition: (Default is None) None or non-empty string

    (Optional) Parameter n: the number of similar shows to output
    Precondition: (Default is 10) an integer

    (Optional if query_show is not None) 
    Parameter free_search: a query with extra information to include in the 
    search 
    Precondition: (Default is None) None or non-empty string

    (Optional) Parameter genre: genre that all the resulting shows must be in
    Precondition: (Default is None) None or non-empty string representation of 
    a valid genres

    (Optional) Parameter streaming platform: streaming platform that all the 
    resulting shows must be on
    Precondition: (Default is None) None or non-empty string representation of 
    a valid streaming platforms
    
    (Optional) Parameter streaming platform: streaming platform that all the 
    resulting shows must be on
    Precondition: (Default is None) None or non-empty string representation of 
    a valid streaming platforms

    (Optional) Parameter not_like_show: the show that you dont want the results 
    to be like
    Precondition: (Default is None) None or non-empty string

    (Optional) Parameter not_like_free_search: a query with extra information 
    to not include in the search 
    Precondition: (Default is None) None or non-empty string
    """

    various_weight_combos = {
        'just show' : {
            'transcripts' : .1,
            'reviews' : .45,
            'descriptions' : .45,
        },
        'show & free search' : {
            'transcripts' : .1 * slider_weights["tv show"],
            'reviews' : .45 * slider_weights["tv show"] ,
            'descriptions' : .45 * slider_weights["tv show"] ,
            'free search' : slider_weights["keyword"] ,
        },
        'just free search' : {
            'free search' : 1,
        }
    }
    results = []
    not_like_tv_sim_score_sum = tv_sim_score_sum = {}
    weights = not_like_weights = {}
    capitalized_query = capitalize_show_name(query_show)
    capitalized_not_like_query = capitalize_show_name(not_like_show)

    weights = select_weights(query_show, free_search, various_weight_combos)
    not_like_weights = select_weights(not_like_show, not_like_free_search,various_weight_combos)

    # EDIT DISTANCE
    if not capitalized_query and capitalized_query not in tv_shows_to_index.keys():
        query_show = ed.edit_search(query_show)[0][1]
        print(query_show)
        capitalized_query = capitalize_show_name(query_show)
    if not_like_show and not capitalized_not_like_query and capitalized_not_like_query not in tv_shows_to_index.keys():
        not_like_show = ed.edit_search(not_like_show)[0][1]
        print(not_like_show)
        capitalized_not_like_query = capitalize_show_name(not_like_show)
        print(capitalized_not_like_query)

    if not_like_show and slider_weights['not like'] > 0:
        transcripts_ranking = jaccardRanking(not_like_show, n) # list of tv shows
        reviews_ranking = reviewRanking(not_like_show, 100) # list of tv shows and sim scores
        if reviews_ranking is None:
            reviews_ranking = []
        desc_ranking = descriptionRanking(not_like_show, 100)
        for i in range(len(transcripts_ranking)):
            show = transcripts_ranking[i]
            lowercase_show = show.lower()
            score = (.5 - ((i+1)/100))
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights['transcripts'] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights['transcripts'] * score * 100
        for show, score in reviews_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights['reviews'] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights['reviews'] * score * 100
        for show, score in desc_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights['descriptions'] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights['descriptions'] * score * 100

    if not_like_free_search and slider_weights['not like'] > 0:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(not_like_free_search, n*2) # list of tv shows and sim scores
        for show, score in free_search_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights['free search'] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights['free search'] * score * 100
    
    shows_not_to_include = [capitalized_query]
    if not_like_show or not_like_free_search:
        shows_not_to_include = [capitalized_not_like_query]
        not_like_tv_sim_score_sum = {k: v for k, v in sorted(not_like_tv_sim_score_sum.items(), key=lambda item: -item[1])}
        n_not_like_shows = len(not_like_tv_sim_score_sum)
        n_not_including = int(slider_weights['not like'] * n_not_like_shows)
        print(n_not_including)
        count = 0
        for key, _ in not_like_tv_sim_score_sum.items():
            if count == n_not_including:
                break
            capitalized_show = capitalize_show_name(key)
            if capitalized_show:
                shows_not_to_include.append(capitalized_show)
                count += 1

    # print(shows_not_to_include)
    if query_show:
        transcripts_ranking = jaccardRanking(query_show, n) # list of tv shows
        reviews_ranking = reviewRanking(query_show, 100) # list of tv shows and sim scores
        if reviews_ranking is None:
            reviews_ranking = []
        desc_ranking = descriptionRanking(query_show, 100)
        for i in range(len(transcripts_ranking)):
            show = transcripts_ranking[i]
            lowercase_show = show.lower()
            score = (.5 - ((i+1)/100))
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights['transcripts'] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights['transcripts'] * score * 100
        for show, score in reviews_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights['reviews'] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights['reviews'] * score * 100
        for show, score in desc_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights['descriptions'] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights['descriptions'] * score * 100

    if free_search:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(free_search, 100) # list of tv shows and sim scores
        for show, score in free_search_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights['free search'] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights['free search'] * score * 100
    

    tv_sim_score_sum = {k: v for k, v in sorted(tv_sim_score_sum.items(), key=lambda item: -item[1])}
    n_sim_shows = len(tv_sim_score_sum)
    # print(tv_sim_score_sum)
    # print(n_sim_shows)

    count = 0
    starting_index = int(n_sim_shows - (slider_weights['similarity'] * n_sim_shows) - n)
    if starting_index < 0:
        starting_index = 0
    elif starting_index > n_sim_shows - n:
        starting_index = n_sim_shows - n
    index = 0
    for key, _ in tv_sim_score_sum.items():
        capitalized_show = capitalize_show_name(key)
        if index >= starting_index:
            if capitalized_show and not capitalized_show in shows_not_to_include:
                show_info = merged_tv_shows[tv_shows_to_index[capitalized_show]]
                results.append(capitalized_show)
                count += 1
        index += 1
        if count == n:
            break
    return (capitalized_query, capitalized_not_like_query, results)

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

# test2 = final_search("Elementary", 10)
# print(test2)

# test2 = final_search("Sherlock", 10, genre="Drama", streaming_platform="HBO")
# print(test2)

# test2 = final_search("Sherlock", 10,)
# print(test2)
