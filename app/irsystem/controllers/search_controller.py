from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

# from scripts.transcript_similarity import *
from app.backend.backend_script import *

# from scripts.transcripts.genre_sim≈ilarity import *
from app.backend.desc import *

project_name = "Stream On"
net_id = "Divya Damodaran: dd492, Riya Jaggi: rj356, Siddhi Chordia: sc2538, Sidharth Vadduri: sv352, Kendall Lane: kal255"


@irsystem.route("/", methods=["GET"])
def search():
    query = request.args.get("search")
    free_search = request.args.get("freeSearch")
    #genre is a comma seperate string of genres; it is an empty string when there are no genres
    genre = request.args.get("genre")
    #subscription is a comma seperate string of subscriptions; it is an empty string when there are no subscriptions
    subscription = request.args.get("subscriptions")

    not_tv_show = request.args.get("not-tv")
    not_keyword = request.args.get("not-keyword")

    #seasMin is a string representing min seasons; default is 1
    seasMin = request.args.get("seasonMin")
    #seasMax is a string representing max seasons; default is 187
    seasMax = request.args.get("seasonMax")

    #yearMin is a string representing min years; default is 1946
    yearMin = request.args.get("yearMin")
    #yearMax is a string representing max years; default is 2021
    yearMax = request.args.get("yearMax")


    #simWeight is a string representing weight of similarity 1-100; default is 100
    simWeight = request.args.get("similarity-weight")
    #notWeight is a string representing weight of <not like> 1-100; default is 0
    notWeight = request.args.get("not-weight")

    #keywordWeight is a string representing weight of keyword 1-100; default is 100 if only keyword, 50 if both, 0 if not at all
    keywordWeight = request.args.get("keyword-weight")
    #showWeight is a string representing weight of show 1-100; default is 100 if only show, 50 if both, 0 if not at all
    showWeight = request.args.get("show-weight")


    if free_search == "":
        free_search = None
    if genre == "":
        genre = None
    if not_tv_show == "":
        not_tv_show = None
    if not_keyword == "":
        not_keyword = None

    if query or free_search:
        slider_weights = {
            "similarity" : int(simWeight)/100,
            "not like" : int(notWeight)/100,
            "keyword" : int(keywordWeight)/100,
            "tv show" :  int(showWeight)/100
        }
        query_show, not_like_query_show, data = final_search(slider_weights, query_show=query, n=10, free_search=free_search, genre=genre, not_like_show=not_tv_show, not_like_free_search=not_keyword)
        
        output_query_msg= ""
        if (query and query_show) or free_search:
            output_query = ""
            if query and free_search:
                output_query = query_show + " (" + showWeight + "%) and " + free_search + " (" + keywordWeight + "%) "
            elif query:
                output_query = query_show + " "
            elif free_search:
                output_query = free_search + " "
            output_query_msg += simWeight + "% Similar to " + output_query + " "

        if (not_tv_show and not_like_query_show) or not_keyword:
            output_query = ""
            if not_tv_show and not_keyword:
                output_query = not_tv_show + " (" + showWeight + ") and " +not_keywordfree_search + " (" + keywordWeight + ") " 
            elif not_tv_show:
                output_query = not_like_query_show + " "
            elif not_keyword:
                output_query = not_keyword + " "

            output_query_msg += notWeight + "% Not Like " + output_query

        if genre:
            output_query_msg += "Genre: " + genre + " "    
       
        
        if len(data) == 0:
            abort(500)

        descript = des(data)

        return render_template("results.html", descr=descript, data=data, output_query=output_query_msg)
    else:
        data = []
        output_message = ""
        genre_list = ""
        free_search = ""

    return render_template(
        "search.html",
        name=project_name,
        netid=net_id,
        output_message=output_message,
        data=data,
        genre_list=genre_list,
    )
