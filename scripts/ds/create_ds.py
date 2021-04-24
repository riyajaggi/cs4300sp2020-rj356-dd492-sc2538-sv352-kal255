# DESCRIPTION: This script creates the data structures using the kaggle data set and the data
# set from the web-scrapping IMDb.
#
# The outline of the data structures for tv_shows and reviews is described in ds.md
#
# DATE: Saturday, April 10, 2021

import pandas as pd
import json
import sys
import math as Math
import pickle


def make_tv_show_ds():
    """
    Returns a tuple of tv_shows, index_to_tv_shows and tv_shows_to_index

    tv_shows is a list of dictionaries represent one tv_show with its data from the kaggle sets.

    index_to_tv_shows is a dictionary with the index as the key and the tv_show as the value (parallel
    to the tv_shows list)

    tv_shows_to_index is a dictionary with the tv_show as the key and the index as the value (parallel
    to the tv_shows list)
    """
    kaggle_file = "datasets/kaggle_data.csv"
    df = pd.read_csv(kaggle_file, na_values="")
    df = df.fillna("")
    result = df.to_dict(orient="records")
    print(len(result))

    tv_shows = []
    index_to_tv_shows = {}
    tv_shows_to_index = {}

    for show in result:
        # d = []
        val = {
            k.lower().strip(): "" if v == -1 or v == "-1" else v
            for k, v in show.items()
            if k != "Unnamed: 0" and k != "Title" and k != "IMDb"
        }
        val["streaming platform"] = list(
            val["streaming platform"].replace(",", ", ").split(", ")
        )
        val["genre"] = list(val["genre"].replace(",", ", ").split(", "))
        seasons = val["no of seasons"]
        if seasons != "":
            val["no of seasons"] = int(seasons[0 : seasons.index("S")].strip())
        val["runtime"] = -1
        val["start year"] = -1
        val["end year"] = -1
        if val["imdb rating"] == "":
            val["imdb rating"] = -1 
        if val["no of seasons"] == "":
            val["no of seasons"] = -1 
        if val["year"] == "":
            val["year"] = -1 
        d = {"show_title": show["Title"], "show_info": val}
        tv_shows.append(d)
        index_to_tv_shows[show["Unnamed: 0"]] = show["Title"]

    tv_shows_to_index = {v: k for k, v in index_to_tv_shows.items()}
    print(len(tv_shows))
    print("Data structures created for tv shows")
    return (tv_shows, index_to_tv_shows, tv_shows_to_index)


def make_reviews_ds():
    """
    Returns a dictionary of reviews with the tv_show as the key and dictionary of multiple reviews
    for that show as the value.
    """
    imbd_file = "datasets/TV_reviews_df.csv"
    # get only the columns you want from the csv file
    df = pd.read_csv(imbd_file, na_values="")
    df = df.fillna("")
    result = df.to_dict(orient="records")

    reviews = {}
    for show in result:
        d = {}
        val = {
            k: "" if v == "NaN" else v
            for k, v in show.items()
            if k != "Unnamed: 0" and k != "TV_show" and k != "review_title"
        }
        val["review_content"] = (
            val["review_content"]
            .replace("<br/>", "")
            .replace("\n", "")
            .replace("&amp", "")
        )
        if show["TV_show"] not in reviews.keys():
            d[show["review_title"]] = val
            reviews[show["TV_show"]] = d
        else:
            d = reviews[show["TV_show"]]
            d[show["review_title"]] = val
            reviews[show["TV_show"]] = d
    # print(len(reviews))
    # print(reviews["Friends"])
    print("Data structures created for reviews")
    return reviews


def make_info_ds():
    """
    Returns a list of all streaming platforms, list of genre

    Prints the count of all streaming platforms, max and min year, year count,
    range of imdb rating, content rating, genre count, max and min seasons, min start date, max
    end date, max and min runtime and chart of that
    """
    a_file = open("datasets/final/merged_tv_shows.json", "r")
    tv_shows = json.load(a_file)

    # streaming_platform_set = {} # dic with count
    years_set = set()  # start date set
    imdb_rating_dict = {}  # 0 1 2 3 4 5 6 7 with count
    seasons_dict = {}  # dict with count
    genre_dict = {}  # dict with count
    max_runtime = 0
    min_runtime = sys.maxsize
    content_rating_dict = {}  # dict with count
    streaming_platform_dict = {}  # keys are the platforms; values the count
    new_json = {}

    count = 0

    for show_dict in tv_shows:
        count += 1
        show_info = show_dict["show_info"]
        years_set.add(show_info["start year"])

        # print(show_info["imdb rating"])
        # print(type(Math.floor(show_info["imdb rating"])))
        imdb_rating_dict[Math.floor(show_info["imdb rating"])] = (
            imdb_rating_dict[Math.floor(show_info["imdb rating"])] + 1
            if Math.floor(show_info["imdb rating"]) in imdb_rating_dict.keys()
            else 1
        )

        content_rating_dict[show_info["content rating"]] = (
            content_rating_dict[show_info["content rating"]] + 1
            if show_info["content rating"] in content_rating_dict.keys()
            else 1
        )

        seasons_dict[show_info["no of seasons"]] = (
            seasons_dict[show_info["no of seasons"]] + 1
            if show_info["no of seasons"] in seasons_dict.keys()
            else 1
        )

        for g in show_info["genre"]:
            genre_dict[g] = genre_dict[g] + 1 if g in genre_dict.keys() else 1

        if show_info["runtime"] > max_runtime:
            max_runtime = show_info["runtime"]
        if show_info["runtime"] < min_runtime:
            min_runtime = show_info["runtime"]

        for p in show_info["streaming platform"]:
            streaming_platform_dict[p] = (
                streaming_platform_dict[p] + 1
                if g in streaming_platform_dict.keys()
                else 1
            )

    new_json = {
        "years_set": list(years_set),
        "imdb_rating_dict": imdb_rating_dict,
        "seasons_dict": seasons_dict,
        "genre_dict": genre_dict,
        "max_runtime": max_runtime,
        "min_runtime": min_runtime,
        "content_rating_dict": content_rating_dict,
        "streaming_platform_dict": streaming_platform_dict,
        "streaming_platform_list": list(streaming_platform_dict.keys()),
        "genre_list": list(genre_dict.keys()),
        "content_rating_list": list(content_rating_dict.keys()),
        "min_seasons": min(list(seasons_dict.keys())),
        "max_seasons": max(list(seasons_dict.keys())),
        "shows_count": count,
        "max_year": 2021,
        "min_year": min(list(years_set))
    }
    # print()
    # print(new_json)
    # print()
    return new_json


def main():
    print()
    # ======= MAKE TV SHOWS AND SAVE JSON =========
    # (tv_shows, index_to_tv_shows, tv_shows_to_index) = make_tv_show_ds()

    # a_file = open("datasets/final/tv_shows.json", "w")
    # json.dump(tv_shows, a_file)
    # a_file.close()
    # print("Made tv shows json")

    # a_file = open("datasets/final/index_to_tv_shows.json", "w")
    # json.dump(index_to_tv_shows, a_file)
    # a_file.close()

    # a_file = open("datasets/final/tv_shows_to_index.json", "w")
    # json.dump(tv_shows_to_index, a_file)
    # a_file.close()

    # ======= MAKE REVIEWS AND SAVE JSON =========
    # reviews = make_reviews_ds()

    # print(len(reviews))
    # a_file = open("datasets/final/reviews.json", "w")
    # json.dump(reviews, a_file)
    # a_file.close()

    # ======= PRINT SAMPLE OUTPUT =========
    # printing sample output
    # print("\n==Printing sample output==\n")
    # print("Number of TV shows: " + str(len(tv_shows)))
    # # print("Number of Reviews: " + str(len(reviews)))
    # print("\nList of TV Shows with reviews: ")
    # for rev in reviews.keys():
    #     print("\t" + rev)
    # print("\n Example TV show (Friends): ")
    # print(tv_shows[tv_shows_to_index["Friends"]])
    # print("\n Example review (Friends): ")
    # print(reviews["Friends"])

    # ======= MAKE INFO AND SAVE JSON =========
    info_json = make_info_ds()
    print(info_json)
    with open("datasets/final/info.p", "wb") as f:
        pickle.dump(info_json, f)
    # a_file.close()
    print("Made info json")


if __name__ == "__main__":
    main()
    print("\nEND OF SCRIPT")
