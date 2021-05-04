import re
import math

def tokenize(query):
  """
  Returns a list of tokens of the given query

  Parameter review: a review for a tv show
  Precondition: a non-empty string
  """
  text = query.lower()
  regex = r'[a-z]+'
  return re.findall(regex, text)

def tokenizeQuotes(query):
  """
  Returns a list of tokens of the given query with quotations

  Parameter review: a review for a tv show
  Precondition: a non-empty string
  """
  result = []
  text = query.lower()
  regex = r'"(.*?)"'
  tokenized_quotes = re.findall(regex, text)
  result += tokenized_quotes
  tokenized_text = tokenize(text)

  for token in tokenized_text:
    count = 0
    for token_quote in tokenized_quotes:
      if token in token_quote:
        count += 1
    if count == 0: 
      result.append(token)


  return result

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

def create_multi_word_dict(index, multi_word_query):
  """
  Returns: A dictionary with info about the multi_word_query, including the 
  number of words in the query, and show_tf pairs relating to all of the words 
  in the query.

  Parameter index: inverted index
  Precondition: dictionary with words as keys and show-tf tuples as values
  
  Parameter multi_word_query: the multi-word query
  Precondition: a non-empty string
  """
  result_dict = {}
  quotes_tokens = tokenize(multi_word_query)
  n_words_in_quotes = len(quotes_tokens)
  result_dict['n_words_in_quotes'] = len(quotes_tokens)
  total_show_lst = []
  show_count_tf_dict = {}

  for word in quotes_tokens:
    if word in index:
      show_tf_lst = index[word]
      for show, show_tf in show_tf_lst.items():
        if show in show_count_tf_dict:
          show_count_tf_dict[show]['count'] += 1
          show_count_tf_dict[show]['tf'] += show_tf
        else:
          show_count_tf_dict[show] = {}
          show_count_tf_dict[show]['count'] = 1
          show_count_tf_dict[show]['tf'] = show_tf
  result_dict['shows_count_tf_dict'] = show_count_tf_dict

  return result_dict

def compute_idf_multi_words(index, multi_word_query, n_shows, min_df=15, max_df_ratio=0.90):
  """
  Returns: An idf value for a multi-word ad hoc query 

  Parameter index: inverted index
  Precondition: dictionary with words as keys and show-tf tuples as values
  
  Parameter multi_word_query: the multi-word query
  Precondition: a non-empty string

  Parameter n_shows: the number of shows in the dataset
  Precondition: An integer 

  Parameter min_df: the minimum show frequency
  Precondition: integer

  Parameter max_df_ratio: the max percentage of show a word can appear in
  Precondition: number between and 0 and 1
  """  
  idf = 0
  df = 0
  multi_word_dict = create_multi_word_dict(index, multi_word_query)
  show_count_tf_dict = multi_word_dict['shows_count_tf_dict']
  for show in show_count_tf_dict.keys():
    if show_count_tf_dict[show]['count'] == multi_word_dict['n_words_in_quotes'] :
      df += 1

  df_ratio = df / n_shows
  if df > min_df and df_ratio < max_df_ratio:
    value = math.log(n_shows/(1 + df), 2)
    idf = value
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

