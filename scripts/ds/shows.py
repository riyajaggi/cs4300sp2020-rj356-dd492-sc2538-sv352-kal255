import json

def list_shows():
    a_file = open("datasets/p2/final/merged_tv_shows_final.json", "r")
    tv_shows = json.load(a_file)

    print(len(tv_shows))

    titles = []
    duplicates = []
    duplicate_titles = []

    lst = []

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

    for num in range(len(tv_shows)):
        # print("\n" + str(num) + " " + tv_shows[num]["show_title"])
        title = tv_shows[num]["show_title"] +  " " + str(tv_shows[num]["show_info"]["start year"])
        if tv_shows[num] in tv_shows[:num]:
            # print("duplicate")
            duplicates.append(title)
            lst.append(tv_shows[num])
        elif title in titles:
            duplicate_titles.append(title)
            # print("duplicate title")
        else:
            titles.append(title)
        # show_genre = tv_shows[num]["show_info"]["genre"]
        # tv_shows[num]["show_info"]["genre"] = [x for x in show_genre if x not in genre_lst]

    # for val in lst:
    #     tv_shows.remove(val)

    print("======")
    print("Duplicates: " + str(len(duplicates)))
    print("Duplicate Titles: " + str(len(duplicate_titles)))
    print("\nList of duplicates: " + str(duplicates))
    print("\nList of duplicate titles: " + str(duplicate_titles))

    # a_file = open("datasets/p2/final/merged_tv_shows_final.json", "w")
    # json.dump(tv_shows, a_file)
    # a_file.close()
    print("Cleaned tv shows")
    


list_shows()