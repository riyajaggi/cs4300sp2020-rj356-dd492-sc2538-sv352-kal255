import requests
from requests import get
import re
import json
from app.backend.cosine_similarity import tokenizeQuotes
"""
def commaSep(word):
    lst = []
    i = 0
    while i < len(word):
        comma = word.find(' ', i)
        if comma != -1:
            wrd = word[i: comma].strip().lower()
            if wrd == "not":
                comma = word.find(',', comma+1)
                if comma != -1:
                    wrd = word[i: comma].strip().lower()
                    lst.append(wrd)
                    i = comma+1
                else:
                    lst.append(wrd)
                    i = len(word)
            else:
                lst.append(wrd)
                i = comma+1
        else:
            lst.append(word[i:].strip())
            i = len(word)
"""

def loadData():
    with open("datasets/p2/relevance.json") as f:
        data = json.load(f)
    f.close()
    return data

def resetjson():
    """
    """
    data = {"shows": {"scores":{}, "relevant": {}, "irrelevant": {}}, "words": {"scores":{}, "relevant": {}, "irrelevant": {}}}
    return data

def updateRelevanceShow(show, result, rel):
    """
    """
    total_data = loadData()
    data = total_data["shows"]

    if not show in data["scores"].keys():
        data["scores"][show] = {}
        data["relevant"][show] = []
        data["irrelevant"][show] = []

    show_results = data["scores"][show]
    if result in data["scores"][show].keys():

        prev_score = show_results[result][0]/ show_results[result][1]

        show_results[result] = [show_results[result][0]+rel,
        show_results[result][1]+1]

        score = show_results[result][0]/ show_results[result][1]
        #make relevant
        if score >= 0.75 and show_results[result][1]>3:
            if prev_score <=0.25 and show_results[result][1]>4:
                data["irrelevant"][show].remove(result)
                data["relevant"][show].append(result)
            elif prev_score < 0.75:
                data["relevant"][show].append(result)
        #make irrelevant
        elif score <= 0.25 and show_results[result][1]>3:
            if prev_score >=0.75 and show_results[result][1]>4:
                data["relevant"][show].remove(result)
                data["irrelevant"][show].append(result)
            elif prev_score > 0.25:
                data["irrelevant"][show].append(result)
        #make neutral
        else:
            if prev_score >=0.75 and show_results[result][1]>4:
                data["relevant"][show].remove(result)
            elif prev_score <=0.25 and show_results[result][1]>4:
                data["irrelevant"][show].remove(result)



    else:
        show_results[result] = [rel, 1]

    return data

def updateRelevanceWords(keywords, result, rel):
    """
    """
    total_data = loadData()
    data = total_data["words"]

    words_lst = tokenizeQuotes(keywords)

    for show in words_lst:

        if not show in data["scores"].keys():
            data["scores"][show] = {}
            data["relevant"][show] = []
            data["irrelevant"][show] = []

        show_results = data["scores"][show]
        if result in data["scores"][show].keys():

            prev_score = show_results[result][0]/ show_results[result][1]

            show_results[result] = [show_results[result][0]+rel,
            show_results[result][1]+1]

            score = show_results[result][0]/ show_results[result][1]
            #make relevant
            if score >= 0.75 and show_results[result][1]>3:
                if prev_score <=0.25 and show_results[result][1]>4:
                    data["irrelevant"][show].remove(result)
                    data["relevant"][show].append(result)
                elif prev_score < 0.75:
                    data["relevant"][show].append(result)
            #make irrelevant
            elif score <= 0.25 and show_results[result][1]>3:
                if prev_score >=0.75 and show_results[result][1]>4:
                    data["relevant"][show].remove(result)
                    data["irrelevant"][show].append(result)
                elif prev_score > 0.25:
                    data["irrelevant"][show].append(result)
            #make neutral
            else:
                if prev_score >=0.75 and show_results[result][1]>4:
                    data["relevant"][show].remove(result)
                elif prev_score <=0.25 and show_results[result][1]>4:
                    data["irrelevant"][show].remove(result)



        else:
            show_results[result] = [rel, 1]

    return data   

def updateData(result, rel, show = None, keywords = None):
    all_data = loadData()
    show_data = all_data["shows"]
    keyword_data = all_data["words"]
    if show != None:
        show_data = updateRelevanceShow(show, result, rel)
    if keywords!= None:
        keyword_data = updateRelevanceWords(keywords, result, rel)

    data = {"shows": show_data, "words": keyword_data}
    a_file = open("datasets/p2/relevance.json", "w")
    json.dump(data, a_file)
    a_file.close()

def resetData():
    data = resetjson()

    a_file = open("datasets/p2/relevance.json", "w")
    json.dump(data, a_file)
    a_file.close()

#resetData()
#Call updateData()
