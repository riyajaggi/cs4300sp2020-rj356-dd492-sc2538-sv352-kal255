import json
from collections import Counter
import math
import app.backend.cosine_similarity as cosine_similarity
from app.backend.rocchio import rocchio_update_addhoc
# import cosine_similarity as cosine_similarity

with open('./datasets/p2/tv_shows_reviews_description.json') as tv_shows_reviews_description_file:
  tv_shows_reviews_description = json.load(tv_shows_reviews_description_file)
with open('./datasets/p2/tv_shows_to_index_final.json') as tv_shows_to_index_file:
  tv_show_to_index = json.load(tv_shows_to_index_file)
with open('./datasets/p2/index_to_tv_shows_final.json') as index_to_tv_show_file:
  index_to_tv_show = json.load(index_to_tv_show_file)
with open("./datasets/p2/relevance.json") as f:
  query_obj = json.load(f)
f.close()

# def build_inverted_index(reviews_description_dict):
#   """
#   Returns: An inverted index represented by a dict with words as keys and show
#   index-tf dictionaries as values

#   Parameter reviews_description_dict: a dictionary with info about reviews 
#   and descriptions
#   Precondtion: review dictionary
#   """  
#   result = {}

#   for show in reviews_description_dict:
#     show_info = reviews_description_dict[show]
#     index = tv_show_to_index[show]
#     all_tokens = cosine_similarity.tokenize(show_info['description'])
#     show_reviews = show_info['reviews']
#     for review in show_reviews:
#           all_tokens += cosine_similarity.tokenize(review)
#     count_dict = Counter(all_tokens)
#     for word, count in count_dict.items():
#         if word in result.keys():
#           if index in result[word].keys():
#             result[word][index] += count
#           else:
#             result[word][index] = count
#         else:
#             result[word] = { index : count }
#     count_dict = {}
        
#   return result

# TESTS FOR INVERTED INDEX
# print(tv_shows_reviews_description['the walking dead'])
# print(index_to_tv_show["29"])
# print(inverted_index['zombie'])
# print(inverted_index['smart'])

# inverted_index = build_inverted_index(tv_shows_reviews_description)
# idf_dict = cosine_similarity.compute_idf(inverted_index, len(index_to_tv_show))
# show_norms = cosine_similarity.compute_show_norms(inverted_index, idf_dict, len(index_to_tv_show))
# inverted_index = {key: val for key, val in inverted_index.items() if key in idf_dict}

# SAVING DATA AS JSON AFTER RUNNING LOCALLY
# a_file = open("datasets/p2/adhoc_inverted_index.json", "w")
# json.dump(inverted_index, a_file)
# b_file = open("datasets/p2/adhoc_show_norms.json", "w")
# json.dump(show_norms, b_file)
# c_file = open("datasets/p2/adhoc_idf_dict.json", "w")
# json.dump(idf_dict, c_file)

# LOADING SAVED JSON
with open('./datasets/p2/adhoc_inverted_index.json') as a_file:
  inverted_index = json.load(a_file)
with open('./datasets/p2/adhoc_show_norms.json') as b_file:
  show_norms = json.load(b_file)
with open('./datasets/p2/adhoc_idf_dict.json') as c_file:
  idf_dict = json.load(c_file)


def index_search(query, index, idf, show_norms):
  """
  Returns: A list of score-show tuples in descending order from most similar 
  shows to least similar shows.
  
  Parameter query: query
  Precondition: string

  Parameter index: inverted index
  Precondition: dictionary with words as keys and show-tf tuples as values

  Parameter idf: computed idf values
  Precondition: dictionary with words as keys and idf as values

  Parameter: computed norms for every show
  Precondition: list with length of the number of shows with reviews
  """  

  result = []
  numerators = {}
  lowercase_query = query.lower()
  #rememebr query_obj
  q1 = rocchio_update_addhoc(query, query_obj['words'], index, idf)
  print(query_obj)
  
  tokenized_query = cosine_similarity.tokenizeQuotes(lowercase_query)
  query_tfs = Counter(tokenized_query)
  query_norm = 0
  
  query_norm = math.sqrt(q1.dot(q1))

  cnt = 0
  for token, q_tf in query_tfs.items():
    if token.find(" ") >= 0:
      multi_word_dict = cosine_similarity.create_multi_word_dict(index, token)
      show_count_tf_dict = multi_word_dict['shows_count_tf_dict']
      token_idf = cosine_similarity.compute_idf_multi_words(index, token, len(index_to_tv_show))
      for show in show_count_tf_dict.keys():
        if show_count_tf_dict[show]['count'] == multi_word_dict['n_words_in_quotes']:
          if q_tf != 0 and token_idf != 0:
            numerator = q1[cnt] * show_count_tf_dict[show]['tf'] * token_idf
            if show in numerators:
              numerators[show] += numerator
            else:
              numerators[show] = numerator
    else:   
      if token in index and token in idf:
          token_idf = idf[token]
          for show, show_tf in index[token].items():
              if q_tf != 0 and token_idf != 0:
                  numerator = q1[cnt] * show_tf * token_idf
                  if show in numerators:
                      numerators[show] += numerator
                  else:
                      numerators[show] = numerator
    cnt+=1

  for show, numerator in numerators.items():
      denominator = query_norm * show_norms[int(show)]
      score = numerator / denominator
      result.append((score, show))
  
  result = sorted(result, key = lambda x: -x[0])
  return result

def find_n_similar_shows_free_search(query, n):
  """ 
  Returns: A list with the top n most similar shows based on free search query.

  Parameter query: the query
  Precondition: string

  Parameter n:  the amount of similar shows to return.
  Precondition: Any integer between 1 and the length of tv_shows_reviews_description.
  """
  
  results = index_search(query, inverted_index, idf_dict, show_norms)
  final_show_list  = []
  
  if len(results)==0:
    return final_show_list

  for i in range(0,n+1):
    final_show_list.append((index_to_tv_show[str(results[i][1])], results[i][0]))
  return final_show_list


# TESTS FOR FREE SEARCH
# test_anthology = find_n_similar_shows_free_search("anthology", 10)
# print(test_anthology)
# print()
# test_dogs = find_n_similar_shows_free_search("dogs", 10)
# print(test_dogs)
# print()
# test_cars = find_n_similar_shows_free_search("i really like cars", 10)
# print(test_cars)
# print()
# test_school = find_n_similar_shows_free_search("school is hard", 10)
# print(test_school)
# print()
# test_funny = find_n_similar_shows_free_search("funny work", 10)
# print(test_funny)
# print()

# test_new_york = find_n_similar_shows_free_search('"New York"', 10)
# print(test_new_york)
# test_los_angeles = find_n_similar_shows_free_search('"Los Angeles"', 10)
# print(test_los_angeles)
# test_LA_and_NY = find_n_similar_shows_free_search('"Los Angeles" and  "New York"', 10)
# print(test_LA_and_NY)
# print()
