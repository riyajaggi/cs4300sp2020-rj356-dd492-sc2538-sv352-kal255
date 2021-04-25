import json
import pandas as pd

def merge_sets():
    tv_shows_file = open("datasets/p2/merged_tv_shows1.json")
    imdb_file = open("datasets/p2/imdb2.json")

    tv_shows_lst = json.load(tv_shows_file)
    imdb_dict = json.load(imdb_file)

    # with open(tv_shows_file) as json_file:
    #     tv_shows_lst = json.parse(json_file)
    updated_count = 0
    not_updated_count = 0
    for show in tv_shows_lst:
        show_name = show["show_title"]
        if show_name in imdb_dict.keys():
            try:
                updated_count +=1
                imdb_data = imdb_dict[show["show_title"]]
                val = show["show_info"]
                val["genre"] = list(set(val["genre"] + imdb_data["genre"]))
                val["imdb rating"] = imdb_data["rating"]
                val["runtime"] = imdb_data["runtime"]
                val["start year"] = imdb_data["start year"]
                val["end year"] = imdb_data["end year"]
                show["show_info"] = val
                print(show_name + " updated!")
            except Exception as e:
                print(e)
                print("ERROR: " + show_name)
                return
        else:
            not_updated_count+=1
    print("\n" + str(updated_count) + " shows updated")
    print("\n" + str(not_updated_count) + " shows not updated")
    return tv_shows_lst

def add_streaming_platforms():
    tv_shows_file = open("datasets/p2/merged_tv_shows2.json")
    tv_shows_lst = json.load(tv_shows_file)

    index_file = open("datasets/p2/tv_shows_to_index.json")
    tv_shows_to_index = json.load(index_file)

    kaggle_file = "datasets/tv_shows.csv"
    df = pd.read_csv(kaggle_file, na_values="")
    df = df.fillna("")
    result = df.to_dict(orient="records")
    # print(result)

    # for x in range(12451):
    #     print(x)
    #     print(tv_shows_lst[x]["show_title"])
    #     print(tv_shows_lst[x]["show_info"])
    #     print()
    # print(tv_shows_lst[2798])

    change = False
    count = 0
    for show in result:
        if show["Title"] not in tv_shows_to_index.keys():
            continue
        merge_item = tv_shows_lst[tv_shows_to_index[show["Title"]]]
        # print("\n" + show["Title"] + " at index " + str(tv_shows_to_index[show["Title"]]))
        # print(merge_item["show_title"])
        if "show_info" not in merge_item.keys():
            continue
        val = merge_item["show_info"]
        if show["Netflix"] == 1 and "Netflix" not in val["streaming platform"]:
            val["streaming platform"] += ["Netflix"]
            change = True
        if show["Hulu"] == 1 and "Hulu" not in val["streaming platform"]:
            val["streaming platform"] += ["Hulu"]
            change = True
        if show["Prime Video"] == 1 and "Prime Video" not in val["streaming platform"]:
            val["streaming platform"] += ["Prime Video"]
            change = True
        if show["Disney+"] == 1 and "Disney+" not in val["streaming platform"]:
            val["streaming platform"] += ["Disney+"]
            change = True
        if change:
            count += 1
            change = False
            print(show["Title"] + " changed!")
        merge_item["show_info"] = val 
        tv_shows_lst[tv_shows_to_index[show["Title"]]]["show_info"] = merge_item["show_info"]
    
    print(count)
    return tv_shows_lst
    # return {}
        

def update_more_shows():
    more_shows = "datasets/more_shows.csv"
    # get only the columns you want from the csv file
    df = pd.read_csv(more_shows, na_values="")
    df = df.fillna("")
    result = df.to_dict(orient="records")

    a_file = open("datasets/p2/final/merged_tv_shows_final.json", "r")
    tv_shows = json.load(a_file)

    index_file = open("datasets/p2/final/tv_shows_to_index_final.json")
    tv_shows_to_index = json.load(index_file)    

    count = 0

    for show in result:
        if show["title"] not in tv_shows_to_index.keys():
            continue
        merge_item = tv_shows[tv_shows_to_index[show["title"]]]
        val = tv_shows[tv_shows_to_index[show["title"]]]
        print(show["title"])
        print()
        val["show_info"]["streaming platform"] += [show["streaming platform"]]
        tv_shows[tv_shows_to_index[show["title"]]]["show_info"] = merge_item["show_info"]
        count+=1
    
    print(str(count) + " shows updated!")
    return tv_shows


def main():
    print()
    # tv_shows_lst = merge_sets()
    # a_file = open("datasets/p2/merged_tv_shows2.json", "w")
    # json.dump(tv_shows_lst, a_file)
    # a_file.close()
    tv_shows_lst = update_more_shows()
    a_file = open("datasets/p2/merged_tv_shows_final.json", "w")
    json.dump(tv_shows_lst, a_file)
    a_file.close()
    print("END OF SCRIPT")



if __name__ == "__main__":
    main()