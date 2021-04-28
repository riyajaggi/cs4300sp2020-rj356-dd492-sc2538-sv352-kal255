import numpy as np
import pandas as pd


def insertion_cost(message, j):
    return 1


def deletion_cost(query, i):
    return 1


def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 2


curr_insertion_function = insertion_cost
curr_deletion_function = deletion_cost
curr_substitution_function = substitution_cost


def edit_mat(query, show):

    m = len(query) + 1
    n = len(show) + 1

    matrix = np.zeros((m, n))
    for i in range(1, m):
        matrix[i, 0] = matrix[i-1, 0] + curr_deletion_function(query, i)

    for j in range(1, n):
        matrix[0, j] = matrix[0, j-1] + curr_insertion_function(show, j)

    for i in range(1, m):
        for j in range(1, n):
            matrix[i, j] = min(
                # "down" or delete op
                matrix[i-1, j] + curr_deletion_function(query, i),
                # "right" or insert op
                matrix[i, j-1] + curr_insertion_function(show, j),
                # "diagnol" or sub op
                matrix[i-1, j-1] + \
                curr_substitution_function(query, show, i, j)
            )

    return matrix


def edit_dist(query, show):
    query = query.lower()
    show = show.lower()
    a = edit_mat(query, show)
    return a[(len(query), len(show))]


def edit_search(query, data='datasets/kaggle_data.csv'):
    df = pd.read_csv(data, usecols=['Title'])

    # print(df)

    # for row in df.iterrows():

    # print(row[1])
    a = df.to_dict()
    # print(a['Title'][0])

    ans = []
    for x in range(len(a['Title'])):
        b = edit_dist(query, a['Title'][x])
        ans.append((b, a['Title'][x]))
    ans.sort(key=lambda tup: tup[0])
    # top_10 =[]
    # for y in ans:

    return ans[:10]


#print(edit_dist('hell', 'Hall'))

print(edit_search('braking bad'))
