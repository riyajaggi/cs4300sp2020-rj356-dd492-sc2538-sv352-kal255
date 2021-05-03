import requests
from requests import get
import re
import json

def loadData():
    with open("relevance.json") as f:
        data = json.load(f)
    f.close()
    return data

def resetjson():
    """
    """
    data = {"scores":{}, "relevant": {}, "irrelevant": {}}
    return data

def updateRelevance(show, result, rel):
    """
    """
    data = loadData()

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
        if score > 0.75:
            if prev_score <0.25:
                data["irrelevant"][show].remove(result)
                data["relevant"][show].append(result)
            elif prev_score <= 0.75:
                data["relevant"][show].append(result)
        #make irrelevant
        elif score < 0.25:
            if prev_score >0.75:
                data["relevant"][show].remove(result)
                data["irrelevant"][show].append(result)
            elif prev_score >= 0.25:
                data["irrelevant"][show].append(result)
        #make neutral
        else:
            if prev_score >0.75:
                data["relevant"][show].remove(result)
            elif prev_score <0.25:
                data["irrelevant"][show].remove(result)



    else:
        show_results[result] = [rel, 1]
        if rel == 1:
            data["relevant"][show].append(result)
        else:
            data["irrelevant"][show].append(result)

    return data

def updateData(show, result, rel):

    data = updateRelevance(show, result, rel)

    a_file = open("relevance.json", "w")
    json.dump(data, a_file)
    a_file.close()

def resetData():
    data = resetjson()

    a_file = open("relevance.json", "w")
    json.dump(data, a_file)
    a_file.close()

resetData()
#Call updateData()
