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
    count = -1
    for show in result:
        # d = []
        count += 1
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
        # if show["Title"] in tv_shows_to_index.keys() and val!=tv_shows[tv_shows_to_index[show["Title"]]]:
        #     print(show["Title"] + " duplicate")
        #     if val["year"] != -1:
        #         # print("here")
        #         show["Title"] = show["Title"] + " " + str(val["year"])
        #         print(show["Title"])
        #     else:
        #         print("ELSE")
        d = {"show_title": show["Title"], "show_info": val}
        tv_shows.append(d)
        # index_to_tv_shows[show["Unnamed: 0"]] = show["Title"]
        tv_shows_to_index[show["Title"]] = count

    index_to_tv_shows = {v: k for k, v in tv_shows_to_index.items()}
    print(len(tv_shows))
    # print(index_to_tv_shows)
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
    a_file = open("datasets/p2/merged_tv_shows3.json", "r")
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
        # print(show_dict)
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
            if p in streaming_platform_dict.keys():
                streaming_platform_dict[p] += 1
            else:
                streaming_platform_dict[p] = 1

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
        "min_seasons": min([x for x in seasons_dict.keys() if x!=-1]),
        "max_seasons": max(list(seasons_dict.keys())),
        "shows_count": count,
        "max_year": 2021,
        "min_year": min([x for x in years_set if x!=-1]),
    }
    # print()
    # print(new_json)
    # print()
    return new_json


def create_final_index():
    a_file = open("datasets/p2/merged_tv_shows2.json", "r")
    tv_shows = json.load(a_file)

    count = 0

    tv_shows_to_index = {}
    index_to_tv_shows = {}

    for show in tv_shows:
        tv_shows_to_index[show["show_title"]] = count
        count += 1

    print(len(tv_shows_to_index))

    index_to_tv_shows = {v: k for k, v in tv_shows_to_index.items()}

    print(len(index_to_tv_shows))
    print("Created index for shows!")
    return (tv_shows_to_index, index_to_tv_shows)


def clean_genre():
    a_file = open("datasets/p2/merged_tv_shows3.json", "r")
    tv_shows = json.load(a_file)

    index_file = open("datasets/p2/final/tv_shows_to_index.json")
    tv_shows_to_index = json.load(index_file)

    genre_lst = [
        "",
        "2009",
        "2007",
        "2003",
        "2014",
        "2018",
        "2000",
        "2006",
        "2016",
        "1999",
        "2015",
        "2011",
        "2020",
        "2019",
        "1993",
        "2012",
        "1975",
        "1969",
        "2017",
        "2010",
        "1995",
        "2008",
        "2013",
        "1992",
        "1998",
        "1987",
        "1996",
        "1983",
        "1981",
        "1965",
        "1990",
        "1997",
        "2001",
        "1955",
        "1984",
        "1974",
        "2002",
        "1964",
        "1980",
        "1978",
        "1977",
        "2004",
        "1994",
        "1976",
        "1972",
        "1982",
        "1970",
        "1989",
        "1985",
        "1986",
        "1968",
        "1991",
        "1949",
        "1979",
        "1971",
        "1958",
        "1988",
        "1962",
        "1950",
        "1963",
        "1966",
        "1957",
        "1959",
        "1961",
        "1967",
        "1951",
        "1901",
        "1952",
        "1954",
        "1948",
        "1947",
        "1953",
        "1956",
        "1960",
        "1931",
        "1904",
        "1945",
        "1943",
        "1973",
    ]
    count = 0
    for show in tv_shows:
        if "show_info" and "show_title" not in show.keys():
            print(show)
            continue
        count += 1
        # print(show)
        print()
        show_genre = show["show_info"]["genre"]
        show["show_info"]["genre"] = [x for x in show_genre if x not in genre_lst]
        tv_shows[tv_shows_to_index[show["show_title"]]]["show_info"] = show["show_info"]
    print(count)
    return tv_shows


def add_titles():
    a_file = open("datasets/p2/merged_tv_shows3.json", "r")
    tv_shows = json.load(a_file)

    index_file = open("datasets/p2/final/index_to_tv_shows.json")
    index_to_tv_shows = json.load(index_file)
    # print(index_to_tv_shows[2])

    # for num in range(len(tv_shows)):
    #     if "show_title" not in tv_shows[num].keys():
    #         d = {"show_title": index_to_tv_shows[str(num)], "show_info": tv_shows[num]}
    #         tv_shows[num] = d

    # a2_file = open("datasets/p2/merged_tv_shows3.json", "w")
    # json.dump(tv_shows, a2_file)
    # a2_file.close()
    # print("Add titles json")
    for num in range(len(tv_shows)):
        print(tv_shows[num]["show_title"])
        print()

    return tv_shows


def main():
    print()
    # add_titles()
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
    with open("datasets/p2/final/info.p", "wb") as f:
        pickle.dump(info_json, f)
    # a_file.close()
    print("Made info json")

    # ======= MAKE TV SHOWS INDEX AND SAVE JSON =========
    # (tv_shows_to_index, index_to_tv_shows) = create_final_index()

    # a_file = open("datasets/p2/index_to_tv_shows.json", "w")
    # json.dump(index_to_tv_shows, a_file)
    # a_file.close()

    # a_file = open("datasets/p2/tv_shows_to_index.json", "w")
    # json.dump(tv_shows_to_index, a_file)
    # a_file.close()

    # ======= CLEAN DESCRIPTIONS AND SAVE JSON =========
    # tv_shows = clean_genre()

    # a_file = open("datasets/p2/merged_tv_shows3.json", "w")
    # json.dump(tv_shows, a_file)
    # a_file.close()
    # print("Cleaned tv shows")


if __name__ == "__main__":
    main()
    print("\nEND OF SCRIPT")
