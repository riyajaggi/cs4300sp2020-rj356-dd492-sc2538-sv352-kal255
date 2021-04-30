import json
from collections import Counter
import math
import cosine_similarity
import pickle

a_file = open("datasets/p2/merged_tv_shows_final.json", "r")
tv_shows_dict = json.load(a_file)

index_file = open("datasets/p2/tv_shows_to_index_final.json", "r")
tv_shows_to_index = json.load(index_file)


def build_inverted_index(tv_shows_dict):

    result = {}

    for num in range(len(tv_shows_dict)):
        show = tv_shows_dict[num]
        title = show["show_title"]
        info = show["show_info"]
        tokenized_description = cosine_similarity.tokenize(info["description"])
        count_dict = Counter(tokenized_description)
        for word, count in count_dict.items():
            if word in result.keys():
                if num in result[word].keys():
                    result[word][num] += count
                else:
                    result[word][num] = count
            else:
                result[word] = { num : count }
        count_dict = {}

    return result



inverted_index = build_inverted_index(tv_shows_dict)
idf_dict = cosine_similarity.compute_idf(inverted_index, len(tv_shows_dict))
# print(inverted_index)
show_norms = cosine_similarity.compute_show_norms(
    inverted_index, idf_dict, len(tv_shows_dict)
)
inverted_index = {key: val for key, val in inverted_index.items() if key in idf_dict}


def index_search(query_show, index, idf, show_norms, tv_shows_dict, tv_shows_to_index):
    results = []
    numerators = {}
    query_show = query_show
    query_description = tv_shows_dict[tv_shows_to_index[query_show]]["show_info"][
        "description"
    ]
    query_tfs = {}
    
    tokenized_query = cosine_similarity.tokenize(query_description)
    description_tf = Counter(tokenized_query)
    # print(description_tf)
    for word, count in description_tf.items():
      if word in query_tfs:
        query_tfs[word] += count
      else:
        query_tfs[word] = count

    query_norm = 0

    for token, tf in query_tfs.items():
        if token in idf.keys():
            query_norm += (tf * idf[token]) ** 2
    query_norm = math.sqrt(query_norm)
    # print(query_tfs)
    for token, q_tf in query_tfs.items():
        if token in index and token in idf:
            token_idf = idf[token]
            for show, show_tf in index[token].items():
                if q_tf != 0 and token_idf != 0:
                    numerator = q_tf * token_idf * show_tf * token_idf
                    if show in numerators:
                        numerators[show] += numerator
                    else:
                        numerators[show] = numerator
    # print(numerators)
    for show, numerator in numerators.items():
        denominator = query_norm * show_norms[show]
        score = numerator / denominator
        results.append((score, show))
    
    results = sorted(results, key=lambda x: -x[0])

    return results


def find_n_similar_shows_descriptions(show, n=10):
    if show in tv_shows_to_index.keys():
        results = index_search(
            show,
            inverted_index,
            idf_dict,
            show_norms,
            tv_shows_dict,
            tv_shows_to_index,
        )
        final_show_list = []
        if len(results) == 0:
            return final_show_list
        for i in range(1, n + 1):
            final_show_list.append(
                (
                    tv_shows_dict[results[i][1]]["show_title"],
                    results[i][0],
                )
            )
        return final_show_list
    else:
        return None

# tests
# print(find_n_similar_shows_descriptions("The Office"))
# print(find_n_similar_shows_descriptions("Friends"))
# print(find_n_similar_shows_descriptions("Sherlock"))
# print(find_n_similar_shows_descriptions("The Legend of Korra"))
# print(find_n_similar_shows_descriptions("Lost in Transition"))

def make_descriptions_model():
    print("START OF SCRIPT")
    descriptions_dict = {}
    for show, index in tv_shows_to_index.items():
        lst = find_n_similar_shows_descriptions(show)
        if lst is not None:
            descriptions_dict[show] = lst
        else:
            descriptions_dict[show] = []
        print(show + " " + str(index))
    with open("datasets/p2/description_similarity.p", "wb") as f:
        pickle.dump(descriptions_dict, f)
    # print(descriptions_dict)
    print("END OF SCRIPT")

make_descriptions_model()
            
