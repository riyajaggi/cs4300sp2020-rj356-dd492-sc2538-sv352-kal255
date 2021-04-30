import json
import re
from collections import Counter
import math

with open('./datasets/p2/reviews1.json') as review1_file:
  review1 = json.load(review1_file)
with open('./datasets/p2/reviews2.json') as review2_file:
  review2 = json.load(review2_file)
reviews_info = dict(list(review1.items()) + list(review2.items()))
reviews_info = dict((k.lower(), v) for k, v in reviews_info.items()) 
shows_with_reviews = list(reviews_info.keys())
for i in range(len(shows_with_reviews)):
  shows_with_reviews[i] = shows_with_reviews[i].lower()
with open('./datasets/p2/merged_tv_shows_final.json') as merged_tv_shows_file:
    tv_show_info = json.load(merged_tv_shows_file)
with open('./datasets/p2/tv_shows_to_index_final.json') as tv_shows_to_index_file:
    tv_show_to_index = json.load(tv_shows_to_index_file)
with open('./datasets/p2/index_to_tv_shows_final.json') as index_to_tv_show_file:
    index_to_tv_show = json.load(index_to_tv_show_file)
tv_shows_reviews_description = {}
for tv_show in tv_show_info:
  title = tv_show['show_title']
  description = tv_show['show_info']['description']
  reviews = []
  if title.lower() in shows_with_reviews:
    reviews_dict = reviews_info[title.lower()]
    for review_title, review_dict in reviews_dict.items():
      reviews.append(review_title + " " + review_dict['review_content'])
  if not (description == "" and reviews == []):
    tv_shows_reviews_description[title] = {'description' : description}
    tv_shows_reviews_description[title]['reviews'] = reviews

# TESTS FOR REVIEW DESCRIPTION DICTIONARY
# print(tv_shows_reviews_description[('The Walking Dead').lower()])
# print(tv_shows_reviews_description[('Outlander').lower()])
# print(tv_shows_reviews_description['insecure'])
# print(tv_shows_reviews_description['chernobyl'])

def tokenize(review):
  """
  Returns a list of tokens of the given reviews

  Parameter review: a review for a tv show
  Precondition: a non-empty string
  """
  text = review.lower()
  regex = r'[a-z]+'
  return re.findall(regex, text)

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
    all_tokens = tokenize(show_info['description'])
    show_reviews = show_info['reviews']
    for review in show_reviews:
          all_tokens += tokenize(review)
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

def compute_idf(index, n_shows, min_df=15, max_df_ratio=0.90):
  """
  Returns: A dictionary of word-idf key-value pairs.

  Parameter index: inverted index
  Precondition: dictionary with words as keys and show-tf tuples as values
    
  Parameter n_shows: the number of tv shows
  Precondition: An integer 

  Parameter min_df: the minimum show frequency
  Precondition: integer

  Parameter max_df_ratio: the max percentage of show a word can appear in
  Precondition: number between and 0 and 1
  """  
  idf = {}
  
  for word, shows in index.items():
      df = len(shows)
      df_ratio = df / n_shows
      if df > min_df and df_ratio < max_df_ratio:
          value = math.log(n_shows/(1 + df), 2)
          idf[word] = value
  
  return idf

# TESTS FOR IDF
# print(len(tv_shows_reviews_description))
# print(idf_dict["zombie"])

def compute_show_norms(index, idf, n_shows):
  """
  Returns: A list of norms for each show

  Parameter index: inverted index
  Precondition: dictionary with words as keys and show-tf tuples as values

  Parameter idf: computed idf values
  Precondition: dictionary with words as keys and idf as values

  Parameter n_shows: the number of tv shows
  Precondition: integer 
  """  
  norms = [0] * n_shows

  for word, idf in idf.items():
      for show_id, tf in index[word].items():
          norms[show_id] += (tf * idf)**2
  for i in range(n_shows):
      norms[i] = math.sqrt(norms[i])
      
  return norms

inverted_index = build_inverted_index(tv_shows_reviews_description)
idf_dict = compute_idf(inverted_index, len(index_to_tv_show))
show_norms = compute_show_norms(inverted_index, idf_dict, len(index_to_tv_show))
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
  tokenized_query = tokenize(lowercase_query)
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
