import re
import os
import numpy as np
import json
import app.backend.adhoc_similarity as adhoc_similarity
import pickle
import app.backend.edit_distance as ed
import app.backend.rocchio as rocchio

with open("./datasets/p2/tv_shows_to_index_final.json") as a_file:
    tv_shows_to_index = json.load(a_file)
with open("./datasets/p2/merged_tv_shows_final.json") as merged_tv_file:
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


def transcriptRanking(show, N=3):
    """
    Returns a ranked list of shows and their cosine simliarity scores
    """
    results = rocchio.transcript_similarity(show)

    return results[:N]


def descriptionRanking(show, N=3):
    """
    Returns a ranked list of shows and their cosine similarity scores

    Parameters:
    show - name of tv show to search for (string)
    N - number of shows returned (int)
    """

    description_dict = pickle.load(open("datasets/p2/description_similarity_100.p", "rb"))
    description_dict = {k.lower(): v for k, v in description_dict.items()}

    if show.lower() not in list(description_dict.keys()):
        return []

    result = description_dict[show.lower()][:N]

    return result


def reviewRanking(show, N=3):
    """
    Returns a ranked list of shows and their cosine similarity scores

    Parameters:
    show - name of tv show to search for (string)
    N - number of shows returned (int)
    """

    review_dict = pickle.load(open("datasets/p2/review_similarity.p", "rb"))
    review_dict = {k: v for k, v in review_dict.items()}
    review_show = capitalize_show_name(show)

    if review_show not in list(review_dict.keys()):
        return []
    result = review_dict[review_show][:N]

    return result


# print(reviewRanking("friends"))
    
def select_weights(query_show, free_search, various_weight_combos, not_like=False):
    """
    Returns weights represented for the final result similarity score
    based on the query inputs

    Parameter query_show: the given show
    Precondition: None or non-empty string

    Parameter free_search: a query with extra information to include in the
    search
    Precondition: None or non-empty string

    Parameter various_weight_combos: a dictionary with different weight combinations
    Precondition: a dictionary with at least four keys: "show & free_search", 
    "not like show & free_search", "just show", and "just free search" and values 
    must be floats between 0 and 1 

    Parameter not_like: whether or not this search contains not like inputs
    Precondition: boolean
    """
    weights = {}
    show_and_free_search = 'show & free search'
    if not_like:
        show_and_free_search = 'not like show & free search'
    if query_show and free_search:
        weights = various_weight_combos[show_and_free_search]
    elif query_show:
        weights = various_weight_combos["just show"]
    elif free_search:
        weights = various_weight_combos["just free search"]
    return weights


def create_shows_not_to_include_list(
    capitalized_query,
    not_like_show,
    not_like_free_search,
    not_like_tv_sim_score_sum,
    slider_weights,
    capitalized_not_like_query=None,
):
    """
    Returns a list of shows not to include in the final search results
    """
    shows_not_to_include = [capitalized_query]
    if not_like_show or not_like_free_search:
        shows_not_to_include.append(capitalized_not_like_query)
        not_like_tv_sim_score_sum = {
            k: v
            for k, v in sorted(
                not_like_tv_sim_score_sum.items(), key=lambda item: -item[1]
            )
        }
        n_not_like_shows = len(not_like_tv_sim_score_sum)
        n_not_including = int(slider_weights["not like"] * n_not_like_shows)
        # print(n_not_including)
        count = 0
        for key, _ in not_like_tv_sim_score_sum.items():
            if count == n_not_including:
                break
            capitalized_show = capitalize_show_name(key)
            if capitalized_show:
                shows_not_to_include.append(capitalized_show)
                count += 1
    return shows_not_to_include


def filter_out_shows(filters):
    """
    Returns a list of titles of shows that can be included in the results based on
    the filters entered by the user.

    filters are genre, subscription, season min, season max, year min and year max
    """
    shows_to_include = list(tv_shows_to_index.keys())
    print("before shows to include: " + str(len(shows_to_include)))

    count = 0
    for k, v in filters.items():
        if (k == "genre" or k == "subscription") and v == []:
            count += 1
        elif k == "seasMin" and v == 1:
            count += 1
        elif k == "seasMax" and v == 187:
            count += 1
        elif k == "yearMin" and v == 1946:
            count += 1
        elif k == "yearMax" and v == 2021:
            count += 1

    # if filters are default (i.e. no filters entered) include all shows
    if count == 6:
        return shows_to_include

    # if filters are not default, remove shows from include list
    for show in merged_tv_shows:
        show_title = show["show_title"]
        show_info = show["show_info"]

        # filter out based on genre
        if filters["genre"] != []:
            show_genre = show_info["genre"]
            if len((set(filters["genre"]).intersection(show_genre))) == 0:
                shows_to_include.remove(show_title)
                continue

        # filter out based on subscription
        if filters["subscription"] != []:
            show_subscriptions = show_info["streaming platform"]
            if len((set(filters["subscription"]).intersection(show_subscriptions))) == 0:
                shows_to_include.remove(show_title)
                continue

        # filter out based on min and max seasons
        if (show_info["no of seasons"] < filters["seasMin"]
            or show_info["no of seasons"] > filters["seasMax"]
        ):
            shows_to_include.remove(show_title)
            continue

        # filter out based on min and max years
        if (show_info["start year"] < filters["yearMin"]
            or show_info["start year"] > filters["yearMax"]
        ):
            shows_to_include.remove(show_title)

    print("after shows to include: " + str(len(shows_to_include)))
    return shows_to_include


def final_search(
    slider_weights,
    filters,
    query_show=None,
    n=10,
    free_search=None,
    genre=None,
    streaming_platform=None,
    not_like_show=None,
    not_like_free_search=None,
):
    """
    Returns: A ranked list of similar shows based on reviews, descriptions,
    transcripts,and other optional arguments.

    Parameter slider_weights: a dictionary with input weights for sliders
    Precondition: a dictionary with four keys: "similarity",  "not like", 
    "show/keyword", and "not like show/keyword" and values must be floats 
    between 0 and 1

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
        "just show": {
            "transcripts": 0.25,
            "reviews": 0.40,
            "descriptions": 0.35,
        },
        'just free search' : {
            'free search' : 1,
        },
        'show & free search' : {
            'transcripts' : .25 * (1 - slider_weights["show/keyword"]),
            'reviews' : .40 * (1 - slider_weights["show/keyword"]),
            'descriptions' : .35 * (1 - slider_weights["show/keyword"]),
            'free search' : slider_weights["show/keyword"] ,
        },
        'not like show & free search' : {
            'transcripts' : .25 * (1 - slider_weights["not like show/keyword"]),
            'reviews' : .40 * (1 - slider_weights["not like show/keyword"]),
            'descriptions' : .35 * (1 - slider_weights["not like show/keyword"]),
            'free search' : slider_weights["not like show/keyword"] ,
        }
    }
    results = []
    not_like_tv_sim_score_sum = tv_sim_score_sum = {}
    weights = not_like_weights = {}
    capitalized_query = capitalize_show_name(query_show)
    capitalized_not_like_query = capitalize_show_name(not_like_show)
    weights = select_weights(query_show, free_search, various_weight_combos)
    not_like_weights = select_weights(not_like_show, not_like_free_search, various_weight_combos, True)

    # EDIT DISTANCE
    if not capitalized_query and capitalized_query not in tv_shows_to_index.keys() and query_show!= None:
        query_show = ed.edit_search(query_show)[0][1]
        capitalized_query = capitalize_show_name(query_show)

    shows_to_include = filter_out_shows(filters)

    if not_like_show and slider_weights["not like"] > 0:
        # EDIT DISTANCE
        if not capitalized_not_like_query and capitalized_not_like_query not in tv_shows_to_index.keys():
            not_like_show = ed.edit_search(not_like_show)[0][1]
            capitalized_not_like_query = capitalize_show_name(not_like_show)

        transcripts_ranking = transcriptRanking(not_like_show, 100)  # list of tv shows
        reviews_ranking = reviewRanking(not_like_show, 100)  # list of tv shows and sim scores
        if reviews_ranking is None:
            reviews_ranking = []
        desc_ranking = descriptionRanking(not_like_show, 100)
        for show, score in transcripts_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights["transcripts"] * score * 100 
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights["transcripts"] * score * 100
        for show, score in reviews_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights["reviews"] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights["reviews"] * score * 100
        for show, score in desc_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights["descriptions"] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights["descriptions"] * score * 100

    if not_like_free_search and slider_weights["not like"] > 0:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(
            not_like_free_search, n * 2
        )  # list of tv shows and sim scores
        for show, score in free_search_ranking:
            lowercase_show = show.lower()
            if lowercase_show in not_like_tv_sim_score_sum:
                not_like_tv_sim_score_sum[lowercase_show] += not_like_weights["free search"] * score * 100
            else:
                not_like_tv_sim_score_sum[lowercase_show] = not_like_weights["free search"] * score * 100

    shows_not_to_include = create_shows_not_to_include_list(
        capitalized_query,
        not_like_show,
        not_like_free_search,
        not_like_tv_sim_score_sum,
        slider_weights,
        capitalized_not_like_query,
    )

    if query_show:
        # EDIT DISTANCE
        if not capitalized_query and capitalized_query not in tv_shows_to_index.keys():
            query_show = ed.edit_search(query_show)[0][1]
            capitalized_query = capitalize_show_name(query_show)
        
        transcripts_ranking = transcriptRanking(query_show, 100) # list of tv shows
        reviews_ranking = reviewRanking(query_show, 100) # list of tv shows and sim scores
        if reviews_ranking is None:
            reviews_ranking = []
        desc_ranking = descriptionRanking(query_show, 100)
        for show, score in transcripts_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights["transcripts"] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights["transcripts"] * score * 100
        for show, score in reviews_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights["reviews"] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights["reviews"] * score * 100
        for show, score in desc_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights["descriptions"] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights["descriptions"] * score * 100

    if free_search:
        free_search_ranking = adhoc_similarity.find_n_similar_shows_free_search(free_search, 100)  # list of tv shows and sim scores
        for show, score in free_search_ranking:
            lowercase_show = show.lower()
            if lowercase_show in tv_sim_score_sum:
                tv_sim_score_sum[lowercase_show] += weights["free search"] * score * 100
            else:
                tv_sim_score_sum[lowercase_show] = weights["free search"] * score * 100

    tv_sim_score_sum = { k: v for k, v in sorted(tv_sim_score_sum.items(), key=lambda item: -item[1]) }
    n_sim_shows = len(tv_sim_score_sum)
    # print(tv_sim_score_sum)
    # print(n_sim_shows)

    count = 0
    starting_index = int(n_sim_shows - (slider_weights["similarity"] * n_sim_shows) - n)
    if starting_index < 0:
        starting_index = 0
    elif starting_index > n_sim_shows - n:
        starting_index = n_sim_shows - n
    index = 0
    for key, _ in tv_sim_score_sum.items():
        capitalized_show = capitalize_show_name(key)
        if index >= starting_index:
            if (
                capitalized_show
                and capitalized_show in shows_to_include
                and not capitalized_show in shows_not_to_include
            ):
                show_info = merged_tv_shows[tv_shows_to_index[capitalized_show]]
                results.append(capitalized_show)
                count += 1
        index += 1
        if count == n:
            break
    return (capitalized_query, capitalized_not_like_query, results)


# # TESTS
# filters = {"genre": [], "subscriptions": [], "seasMin": 1, "seasMax": 187, "yearMin": 1946, "yearMax": 2021}
# filters1 = {"genre": [], "subscriptions": ["Netflix"], "seasMin": 1, "seasMax": 187, "yearMin": 2000, "yearMax": 2021}
# the_walking_dead_results = final_search("The Walking Dead", 10)
# print(the_walking_dead_results)

# the_walking_dead_results_2 = final_search("The Walking Dead")
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
