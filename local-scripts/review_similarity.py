# import json
# from collections import Counter
# import math
# import cosine_similarity
# import pickle

# with open('./datasets/p2/tv_shows_to_index_final.json') as a_file:
#   tv_shows_to_index = json.load(a_file)

# with open('./datasets/p2/reviews1.json') as review1_file:
#   review1 = json.load(review1_file)
# with open('./datasets/p2/reviews2.json') as review2_file:
#   review2 = json.load(review2_file)
# reviews_info = dict(list(review1.items()) + list(review2.items()))
# reviews_info = dict((k.lower(), v) for k, v in reviews_info.items()) 
# shows_with_reviews = list(reviews_info.keys())
# for i in range(len(shows_with_reviews)):
#   shows_with_reviews[i] = shows_with_reviews[i].lower()
# with open('./datasets/p2/tv_shows_to_index_final.json') as tv_shows_to_index_file:
#   tv_show_to_index = json.load(tv_shows_to_index_file)
#   lower_show_to_index = {}
#   for show, index in tv_show_to_index.items():
#     lower_show_to_index[show.lower()] = index
# with open('./datasets/p2/index_to_tv_shows_final.json') as index_to_tv_show_file:
#   index_to_tv_show = json.load(index_to_tv_show_file)

# def build_inverted_index(reviews_dict):
#   """
#   Returns: An inverted index represented by a dict with words as keys and show
#   index-tf dictionaries as values

#   Parameter reviews_dict: a dictionary with info about reviews
#   Precondtion: review dictionary
#   """    

#   result = {}
  
#   for show in reviews_dict:
#     show_reviews = reviews_dict[show]
#     if show.lower() in lower_show_to_index:
#       index = lower_show_to_index[show]
#       for review in show_reviews:
#             tokenized_review = cosine_similarity.tokenize(show_reviews[review]['review_content'])
#             count_dict = Counter(tokenized_review)
#             for word, count in count_dict.items():
#                 if word in result.keys():
#                   if index in result[word].keys():
#                     result[word][index] += count
#                   else:
#                     result[word][index] = count
#                 else:
#                     result[word] = { index : count }
#             count_dict = {}
#       index += 1
        
#   return result

# # TESTS FOR INVERTED INDEX
# # print(shows_with_reviews[0])
# # print(inverted_index['zombie'])
# # print(inverted_index['supernatural'])
# # print(inverted_index['smart'])

# inverted_index = build_inverted_index(reviews_info)
# idf_dict = cosine_similarity.compute_idf(inverted_index, len(index_to_tv_show))
# show_norms = cosine_similarity.compute_show_norms(inverted_index, idf_dict, len(index_to_tv_show))
# if inverted_index is not None:
#   inverted_index = {key: val for key, val in inverted_index.items() if key in idf_dict}


# def index_search(query_show, index, idf, show_norms):
#   """
#   Returns: A list of score-show tuples in descending order from most similar 
#   shows to least similar shows.
  
#   Parameter query_show: the given show
#   Precondition: A non-empty lowercase string

#   Parameter index: inverted index
#   Precondition: dictionary with words as keys and show-tf tuples as values

#   Parameter idf: computed idf values
#   Precondition: dictionary with words as keys and idf as values

#   Parameter: computed norms for every show
#   Precondition: list with length of the number of shows with reviews
#   """  
#   result = []
#   numerators = {}
#   lowercase_query = query_show.lower()
#   query_review = reviews_info[lowercase_query]
#   query_tfs = {}
#   for review in query_review:
#     tokenized_query = cosine_similarity.tokenize(query_review[review]['review_content'])
#     review_tf = Counter(tokenized_query)
#     for word, count in review_tf.items():
#       if word in query_tfs:
#         query_tfs[word] += count
#       else:
#         query_tfs[word] = count
#   query_norm = 0
#   for token, tf in query_tfs.items():
#     if token in idf.keys():
#       query_norm += (tf * idf[token])**2
#   query_norm = math.sqrt(query_norm)

#   for token, q_tf in query_tfs.items():
#       if token in index and token in idf:
#           token_idf = idf[token]
#           for show, show_tf in index[token].items():
#               if q_tf != 0 and token_idf != 0:
#                   numerator = q_tf * token_idf * show_tf * token_idf
#                   if show in numerators:
#                       numerators[show] += numerator
#                   else:
#                       numerators[show] = numerator
#   for show, numerator in numerators.items():
#       denominator = query_norm * show_norms[show]
#       score = numerator / denominator
#       result.append((score, show))
  
#   result = sorted(result, key = lambda x: -x[0])
#   return result

# def find_n_similar_shows_reviews(show, n):
#   """ 
#   Returns: A list with the top n most similar shows based on show reviews to
#   the given show.
  
#   Parameter show: the given show
#   Precondition: A non-empty string

#   Parameter n:  the amount of similar shows to return.
#   Precondition: Any integer between 1 and the length of shows_with_reviews.
#   """
#   if show.lower() in shows_with_reviews:
#     results = index_search(show.lower(), inverted_index, idf_dict, show_norms)
#     if results is None:
#       print("Couldn't find results for " + show + ".")
#       return None
#     results_length = len(results)
#     n_results = n
#     if results_length < n_results:
#       n_results = results_length
#     final_show_list  = []

#     for i in range(n_results):
#       final_show_list.append((index_to_tv_show[str(results[i][1])], results[i][0]))
#     return final_show_list
#   else:
#     return None

# # TESTS FOR REVIEWS SIMILARITY
# # test_twd = find_n_similar_shows_reviews("The Walking Dead", 10)
# # print(test_twd)
# # test_twd_lowercase = find_n_similar_shows_reviews("the walking dead", 3)
# # print(test_twd_lowercase)
# # test_sherlock = find_n_similar_shows_reviews("Sherlock", 10)
# # print(test_sherlock)
# # test_shameless = find_n_similar_shows_reviews("shameless", 5)
# # print(test_shameless)
# # test_outlander = find_n_similar_shows_reviews("outlander", 4)
# # print(test_outlander)
# # test_show_no_reviews = find_n_similar_shows_reviews("askdfjl", 3)
# # print(test_show_no_reviews)


# # def make_reviews_model():
# #     print("START OF SCRIPT")
# #     reviews_dict = {}
# #     for show, index in tv_shows_to_index.items():
# #         lst = find_n_similar_shows_reviews(show, 250)
# #         if lst is not None:
# #             reviews_dict[show] = lst
# #         else:
# #             reviews_dict[show] = []
# #         print(show + " " + str(index))
# #     # a_file = open("datasets/p2/review_similarity.json", "w")
# #     # json.dump(reviews_dict, a_file)
# #     with open("datasets/p2/review_similarity.p", "wb") as f:
# #       pickle.dump(reviews_dict, f)
# #     # print(descriptions_dict)
# #     print("END OF SCRIPT")

# make_reviews_model()