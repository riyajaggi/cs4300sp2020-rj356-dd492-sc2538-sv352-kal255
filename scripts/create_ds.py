# import csv

# filename = 'datasets/kaggle_data.csv'

# with open(filename, 'r') as data:
#     tv_shows = csv.DictReader(data)

# for x in tv_shows:
#     print(x)
#     break

import pandas as pd
filename = 'datasets/kaggle_data.csv'
# get only the columns you want from the csv file
df = pd.read_csv(filename)
result = df.to_dict(orient='records')

tv_shows = []
index_to_tv_shows = {}
tv_shows_to_index = {}
# print(result)
for show in result:
    d = {}
    val = {
        k.lower().strip(): "" if v==-1 or v=="NaN" else v
        for k, v in show.items() if k!="Unnamed: 0" and k!= "Title"
        }
    d[show["Title"]] = val
    tv_shows.append(d)
    index_to_tv_shows[show["Unnamed: 0"]] = show["Title"]

# cleaning the ds
for show in tv_shows:
    print(show)
    val["streaming platform"] = val["streaming platform"].replace(",", ", ")
    # for k,v in val.items():
    #     if v == -1 or v == "nan":
    #         val[k] = ""
        

tv_shows_to_index = {v: k for k, v in index_to_tv_shows.items()}

# for x in range(10):
#     print(tv_shows[0])
#     print()

filename_scraped = 'datasets/TV_reviews_df.csv'
# get only the columns you want from the csv file
df = pd.read_csv(filename_scraped)
result = df.to_dict(orient='records')

reviews = {}
for show in result:
    d = {}
    val = {k: "" if v=="NaN" else v for k, v in show.items() if k!="Unnamed: 0" and k!="TV_show" and k!="review_title"}
    if show["TV_show"] not in reviews.keys():
        d[show["review_title"]] = val
        reviews[show["TV_show"]] = d
    else:
        d = reviews[show["TV_show"]]
        d[show["review_title"]] = val
        reviews[show["TV_show"]] = d
print(len(reviews))
print(reviews["Friends"])

