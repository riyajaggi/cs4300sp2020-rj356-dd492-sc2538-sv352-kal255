from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import re
import os



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
        name = name[len(transcriptsFolder)+1:]


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


def build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=10):
    """Returns a TfidfVectorizer object with certain preprocessing properties.

    Params: {max_n_terms: Integer,
             max_prop_docs: Float,
             min_n_docs: Integer}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(max_features = max_n_terms, stop_words = 'english', min_df= min_n_docs, max_df = max_prop_docs)

def write():
    tfidf_vec = build_vectorizer()
    data, movie_name_to_index, movie_index_to_name = allShowTokens("../transcripts")
    tfidf_mat = tfidf_vec.fit_transform([d['script'] for d in data]).toarray()
    print(movie_name_to_index)
    np.save('input_doc_mat.npy', tfidf_mat)


    idx = {"movie_name_to_index": movie_name_to_index, "movie_index_to_name": movie_index_to_name}
    a_file = open("index.json", "w")
    json.dump(idx, a_file)
    a_file.close()

    # print the array

write()
