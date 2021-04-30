
import json

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

with open("./datasets/p2/tv_shows_reviews_description.json", "w") as tv_shows_reviews_description_file: 
    json.dump(tv_shows_reviews_description, tv_shows_reviews_description_file)