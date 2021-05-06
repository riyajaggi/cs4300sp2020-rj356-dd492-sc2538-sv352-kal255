import json
import numpy as np

def format_des(show_info):
    formatted_des = {}
    end_year = show_info["end year"] if show_info["end year"] != 0 else ""
    formatted_des["Years"] = str(show_info["start year"]) + " - " + str(end_year)
    formatted_des["Seasons"] = str(show_info["no of seasons"])
    formatted_des["Runtime"] = str(show_info["runtime"]) + " mins"
    formatted_des["Streaming Platforms"] = ", ".join(show_info["streaming platform"])
    formatted_des["Genre"] = ", ".join(show_info["genre"])
    formatted_des["Content Rating"] = show_info["content rating"].title()
    formatted_des["IMBd rating"] = str(show_info["imdb rating"])
    formatted_des["Description"] = str(show_info["description"])

    return formatted_des

def des(shows):
    show_descriptions = []
    shows_lst = json.load(open("datasets/p2/merged_tv_shows_final.json", "r"))
    tv_shows_to_index = json.load(open("datasets/p2/tv_shows_to_index_final.json", "r"))

    for show in shows:
        if show not in tv_shows_to_index.keys():
            d = "no description"
        else:
            d = format_des(shows_lst[tv_shows_to_index[show]]["show_info"])
        show_descriptions.append(d)

    return show_descriptions

# 
# print(des(["Game of Thrones", "Friends"]))
