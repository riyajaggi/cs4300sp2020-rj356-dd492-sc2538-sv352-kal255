import json
from collections import Counter
import math
import scripts.cosine_similarity as cosine_similarity

with open('./datasets/p2/tv_shows_reviews_description.json') as tv_shows_reviews_description_file:
  tv_shows_reviews_description = json.load(tv_shows_reviews_description_file)
with open('./datasets/p2/tv_shows_to_index_final.json') as tv_shows_to_index_file:
  tv_show_to_index = json.load(tv_shows_to_index_file)
with open('./datasets/p2/index_to_tv_shows_final.json') as index_to_tv_show_file:
  index_to_tv_show = json.load(index_to_tv_show_file)

def build_inverted_index(reviews_description_dict):
  """
  Returns: An inverted index represented by a dict with words as keys and show
  index-tf dictionaries as values

  Parameter reviews_description_dict: a dictionary with info about reviews 
  and descriptions
  Precondtion: review dictionary
  """  
  result = {}

  for show in reviews_description_dict:
    show_info = reviews_description_dict[show]
    index = tv_show_to_index[show]
    all_tokens = cosine_similarity.tokenize(show_info['description'])
    show_reviews = show_info['reviews']
    for review in show_reviews:
          all_tokens += cosine_similarity.tokenize(review)
    count_dict = Counter(all_tokens)
    for word, count in count_dict.items():
        if word in result.keys():
          if index in result[word].keys():
            result[word][index] += count
          else:
            result[word][index] = count
        else:
            result[word] = { index : count }
    count_dict = {}
        
  return result

# TESTS FOR INVERTED INDEX
# print(tv_shows_reviews_description['the walking dead'])
# print(index_to_tv_show["29"])
# print(inverted_index['zombie'])
# print(inverted_index['smart'])

inverted_index = build_inverted_index(tv_shows_reviews_description)
idf_dict = cosine_similarity.compute_idf(inverted_index, len(index_to_tv_show))
show_norms = cosine_similarity.compute_show_norms(inverted_index, idf_dict, len(index_to_tv_show))
inverted_index = {key: val for key, val in inverted_index.items() if key in idf_dict}

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
  tokenized_query = cosine_similarity.tokenize(lowercase_query)
  query_tfs = Counter(tokenized_query)
  query_norm = 0
  for token, tf in query_tfs.items():
      if token in idf.keys():
          query_norm += (tf * idf[token])**2
  query_norm = math.sqrt(query_norm)

  for token, q_tf in query_tfs.items():
    if token in index and token in idf:
        token_idf = idf[token]
        for show, show_tf in index[token].items():
            if q_tf != 0 and token_idf != 0:
                numerator = q_tf * token_idf * show_tf * token_idf
                if show in numerators:
                    numerators[show] += numerator
                else:
                    numerators[show] = numerator
  for show, numerator in numerators.items():
      denominator = query_norm * show_norms[show]
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
  for i in range(1,n+1):
    final_show_list.append((index_to_tv_show[str(results[i][1])], results[i][0]))
  return final_show_list

# TESTS FOR FREE SEARCH
# test_anthology = find_n_similar_shows_free_search("anthology", 10)
# print(test_anthology)
# test_dogs = find_n_similar_shows_free_search("dogs", 10)
# print(test_dogs)
# test_cars = find_n_similar_shows_free_search("i really like cars", 10)
# print(test_cars)
# test_school = find_n_similar_shows_free_search("school is hard", 10)
# print(test_school)
# test_funny = find_n_similar_shows_free_search("funny work", 10)
# print(test_funny)
