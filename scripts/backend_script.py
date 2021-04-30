import re
import os
import numpy as np
import json
import review_similarity
import adhoc_similarity

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
def final_search(query_show, n,  free_search=None, genre=None, ):
    """
    """

    weights = {
        'transcripts' : .20 ,
        'reviews' : .80,
        'descriptions' : 0,
        'genre' : 0,
        'free search' : 0,
    }

    results = []
    tv_sim_score_sum = {}
    transcripts_ranking = jaccardRanking(query_show, n) # list of tv shows
    reviews_ranking = review_similarity.find_n_similar_shows_reviews(query_show, n*2) # list of tv shows and sim scores
    # desc_ranking = 
    free_search_ranking = []
    if free_search is not None:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(free_search, n*2) # list of tv shows and sim scores
        weights['transcripts'] = .15
        weights['reviews'] = .50
        # weights['descriptions'] = .45
        weights['free search'] = .35
        for show, score in free_search_ranking:
            if show in tv_sim_score_sum:
                tv_sim_score_sum[show] += weights['free search'] * score * 100
            else:
                tv_sim_score_sum[show] = weights['free search'] * score * 100
    genre_search_ranking = []
    # if genre is not None:
    #     # genre_ranking =   
    
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
    
    tv_sim_score_sum = {k: v for k, v in sorted(tv_sim_score_sum.items(), key=lambda item: item[1])}
    index = 0
    for key, _ in tv_sim_score_sum.items():
        results.append(key)
        index += 1
        if index == n:
            break
    return results

the_walking_dead_results = final_search("The Walking Dead", 10)
print(the_walking_dead_results)



