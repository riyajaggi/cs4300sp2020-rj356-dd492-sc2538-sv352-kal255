import json
import numpy as np


def possible_genres(
    mat="datasets/p2/index_to_tv_shows_final.json",
    info="datasets/p2/merged_tv_shows_final.json",
):

    """
    returns a dictionary of format {genre:count} where count is the number of shows that fall into the genre. only include genres that appear more than once.
    """
    result = {}
    above_1 = {}
    index_mat = json.load(open(mat))
    show_info = json.load(open(info))
    for i in range(len(index_mat.keys())):
        show = index_mat[str(i)]
        for genre in show_info[i]["show_info"]["genre"]:
            if genre in result.keys():
                result[genre] += 1
                if genre in above_1.keys():
                    above_1[genre] += 1
                else:
                    above_1[genre] = 1
            else:
                result[genre] = 1
    #print(above_1)
    return above_1


genres = possible_genres()

def genre_matrix_generator (genre_dict = genres, info="datasets/p2/merged_tv_shows_final.json"):
    """
    returns a matrix with genres as rows and movies as columns with each value being a 1 if the movie is of the genre and 0 if not
    """
    genre_list = list(genre_dict.keys())
    show_info = json.load(open(info))
    result = np.zeros((len(genre_list), len(show_info)))

    for i in range(len(show_info)):
        for j in range(len(genre_list)):
            #print(genre_list)
            genre = genre_list[j]
            show_genre_list = show_info[i]["show_info"]["genre"]

            if(genre in show_genre_list ):
                    result[j][i] = 1
    
    #print (result)
    return result

genre_matrix = genre_matrix_generator()
       