import re
import math

def tokenize(review):
  """
  Returns a list of tokens of the given reviews

  Parameter review: a review for a tv show
  Precondition: a non-empty string
  """
  text = review.lower()
  regex = r'[a-z]+'
  return re.findall(regex, text)

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

