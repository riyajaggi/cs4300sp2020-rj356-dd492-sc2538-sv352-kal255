from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import re
import os
import numpy as np
import json

def readTranscript(filePath):
    """
    given a string filePath, return the relevant part of the transcript file
    """
    file = open(filePath, encoding='utf-8')
    fileContents = file.read()
    file.close()
    # print(fileContents)
    if fileContents.find('SUBSLIKESCRIPT') != -1:
        if fileContents.find('Search') == -1:
            start = 0
            end = 0
        else:
            start = fileContents.index('Search') + len('Search')
            end = fileContents.rfind("subslikescript horizontal adaptive media")
    else:
        start = fileContents.index('Print') + 5
        end = fileContents.rfind("Transcripts")
    return fileContents[start: end]

# readTranscript('../transcripts/Avatar The Last Airbender/avatar_scripts_s1_e1.txt')


def listTranscripts(showFolder):
    """
    given a string showFolder (path to show folder), return a list of the transcript files for that show
    """
    result = []
    for sub, dirs, transcripts in os.walk(showFolder):
        for file in transcripts:
            filepath = sub + os.sep + file
            result.append(filepath)
    # print(result)
    return (result)


# listTranscripts("../transcripts/American Crime Story"


# showTokens("../transcripts/American Crime Story")


def allShowTokens(transcriptsFolder):
    """
    given a string path to the transcriptsFolder, return a dictionary of form {show:{token:count}}
    """
    movie_name_to_index = {}
    movie_index_to_name = {}
    incr = 0
    result = []
    for sub, dirs, shows in os.walk(transcriptsFolder):

        contents = ""
        filepath = sub + os.sep
        folder = filepath[:-1]
        name = folder[(folder.rfind("\\")) + 1:]
        name = name[16:]


        for file in shows:
            if(file!=".DS_Store"):
                fileContents = readTranscript(folder+"/"+file)
                contents += fileContents

        if(file!=".DS_Store"):
            result.append({"show_name": name, "script": fileContents})
            movie_name_to_index[name] = incr
            movie_index_to_name[incr] = name
            incr+=1
    return result, movie_name_to_index, movie_index_to_name


def build_vectorizer(max_n_terms=50000, max_prop_docs=0.8, min_n_docs=10):
    """Returns a TfidfVectorizer object with certain preprocessing properties.

    Params: {max_n_terms: Integer,
             max_prop_docs: Float,
             min_n_docs: Integer}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(max_features = max_n_terms, stop_words = 'english', min_df= min_n_docs, max_df = max_prop_docs)

def rocchio_update(query, query_obj, input_doc_mat, \
            movie_name_to_index,a=.3, b=.3, c=.8):
    """Returns a vector representing the modified query vector.

    Note:
        Be sure to handle the cases where relevant and irrelevant are empty lists.

    Params: {query: String (the name of the movie being queried for),
             query_obj: Dict (storing the names of relevant and irrelevant movies for query),
             input_doc_mat: Numpy Array,
             movie_name_to_index: Dict,
             a,b,c: floats (weighting of the original query, relevant movies,
                             and irrelevant movies, respectively)}
    Returns: np.ndarray
    """
    i = movie_name_to_index[query]
    q0 = input_doc_mat[i]

    sum_rel = np.zeros(len(q0))

    if query in query_obj['relevant'].keys():
        rel = query_obj['relevant']
    else:
        rel = []

    for d in rel:
        sum_rel+= input_doc_mat[movie_name_to_index[d]]

    sum_irrel = np.zeros(len(q0))

    if query in query_obj['irrelevant'].keys():
        irrel = query_obj['irrelevant']
    else:
        irrel = []

    for d2 in irrel:
        sum_irrel+= input_doc_mat[movie_name_to_index[d2]]

    if len(rel) == 0 and len(irrel) == 0:
        q1 = q0
    elif len(irrel) == 0:
        q1 = q0
    elif len(rel) == 0:
        q1 = q0
    else:
        q1 = a*q0 + b*(sum_rel/len(rel)) - c*(sum_irrel/len(irrel))

    return np.clip(q1, 0, None)

def rankings_with_rocchio(input_queries, query_obj, input_doc_mat, \
        movie_name_to_index,
          movie_index_to_name, input_rocchio=rocchio_update):
    """Returns a dictionary in the following format:
    {
        'romeo and juliet': [movie1,movie2,movie3,...],
        'star wars': [movie1,movie2,movie3,...],
        'a nightmare on elm street': [movie1,movie2,movie3,...]
    }

    Note: You should use the default rocchio parameters.

        You should NOT return the query itself in the list of most common
        movies.

        Params: {input_queries: Dict of query objects,
             input_doc_mat: np.ndarray,
             movie_name_to_index: Dict,
             movie_index_to_name: Dict,
             input_rocchio: Function}

    Returns: Dict
    """
    ret = {}
    for query in input_queries:
        temp = {}
        new_query = input_rocchio(query, query_obj, input_doc_mat, movie_name_to_index)

        for i in range(len(input_doc_mat)):
            movie = movie_index_to_name[str(i)]
            if movie != query:
                array1 = input_doc_mat[i]
                array2 = new_query
                nrm = np.linalg.norm(array1)*np.linalg.norm(array2)
                if nrm == 0:
                    temp[movie] = 0
                else:
                    temp[movie] = array1.dot(array2)/nrm

        temp = list(temp.items())
        temp.sort(key =lambda x: x[1], reverse = True)
        ret[query] = temp
    return ret

def main():
    with open("test.json") as f:
        query_obj = json.load(f)
    f.close()
    with open("index.json") as i:
        temp = json.load(i)
        movie_name_to_index = temp['movie_name_to_index']
        movie_index_to_name = temp['movie_index_to_name']
    i.close()
    tfidf_mat = np.load('input_doc_mat.npy')
    results = rankings_with_rocchio(["Sherlock"], query_obj, tfidf_mat, movie_name_to_index, \
                movie_index_to_name)
    print(results)

main()
