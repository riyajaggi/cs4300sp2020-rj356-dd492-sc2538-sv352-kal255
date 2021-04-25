import pandas as pd
import json
import re


def get_imbd_ds():
    count = 0
    tv_shows_file = 'datasets/TV_info_df2.csv'
    df = pd.read_csv(tv_shows_file, na_values='')
    df = df.fillna('')
    result = df.to_dict(orient='records')
    imbd_dict = {}
    
    print(len(result))
    for show in result:
        val = {
            k.lower().strip(): "" if v==-1 or v=="-1" else v
            for k, v in show.items() if k!="Unnamed: 0" and k!= "title" and k!="years"
            }
        val["genre"] = list(val["genre"].split(", "))
        val["rating"] = -1 if val["rating"] == "" else int(val["rating"]) 
        # print(val["runtime"])
        try:
            val["runtime"] = int(val["runtime"][:val["runtime"].index(" ")])
        except:
            val["runtime"] = -1
        # print(show["years"])
        years = show["years"]
        if not any(str.isdigit(c) for c in years):
            val["start year"] = -1
            val["end year"] = -1
        elif bool(re.match(r"\(\D", years)):
            lst = years.split(" ")
            # print(lst)
            x = lst[0][1]
            start_year = lst[1].index("(") + 1
            # print(start_year)
            show["title"] = show["title"] + " " + x
            # print(show["title"])
            # print(lst[1][start_year:lst[1].index("–")])
            try:
                val["start year"] = int(lst[1][start_year:lst[1].index("–")])
            except:
                val["start year"] = int(lst[1][start_year:lst[1].index(")")])
        else:
            start_year = years.index("(") + 1
            # print(years[start_year:years.index("–")])
            try:
                val["start year"] = int(years[start_year:years.index("–")])
            except: 
                val["start year"] = int(years[start_year:years.index(")")])
        try: 
            end_year = years[years.index("–")+1:-1]
            try:
                val["end year"] = int(end_year)
            except:
                val["end year"] = 0
        except:
            val["end year"] = val["start year"]
        if show["title"] in imbd_dict.keys():
            print(show["title"] +" duplicate")
            # print(imbd_dict[show["title"]])
            # print(val)
            # print()
            count+=1;
            if val["start year"] != -1:
                # print("here")
                new_title = show["title"] + " " + str(val["start year"])
                print(new_title)
                imbd_dict[new_title] = val
            else:
                print("ELSE")
        else:
            imbd_dict[show["title"]] = val
    
    print("Count: " + str(count))
    return imbd_dict


def compare():
    a_file = open("datasets/p2/imdb2.json", "r")
    imdb2 = json.load(a_file)
    tv_shows_file = 'datasets/TV_info_df2.csv'
    df = pd.read_csv(tv_shows_file, na_values='')
    df = df.fillna('')
    result = df.to_dict(orient='records')
    result_lst = [show["title"] for show in result]
    print("length of result: " + str(len(result_lst)))
    imdb_lst = imdb2.keys()
    print("length of imdb list: " + str(len(imdb_lst)))
    ans = list(set(imdb_lst) - set(result_lst))
    # print(len(ans))
    # print(ans)


def main():
    imbd_dict = get_imbd_ds()
    print(len(imbd_dict))
    a_file = open("datasets/p2/imdb2.json", "w")
    json.dump(imbd_dict, a_file)
    a_file.close()
    compare()

if __name__ == "__main__":
    main()
