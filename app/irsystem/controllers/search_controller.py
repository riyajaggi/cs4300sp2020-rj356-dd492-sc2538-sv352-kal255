from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

# from scripts.transcript_similarity import *
from app.backend.backend_script import *

# from scripts.transcripts.genre_sim≈ilarity import *
from app.backend.desc import *

from app.backend.relevance import updateData

project_name = "Stream On"
net_id = "Divya Damodaran: dd492, Riya Jaggi: rj356, Siddhi Chordia: sc2538, Sidharth Vadduri: sv352, Kendall Lane: kal255"


@irsystem.route("/", methods=["GET"])
def search():
    query = request.args.get("search")
    free_search = request.args.get("freeSearch")
    # genre is a comma seperate string of genres; it is an empty string when there are no genres
    genre = request.args.get("genre")
    # subscription is a comma seperate string of subscriptions; it is an empty string when there are no subscriptions
    subscription = request.args.get("subscriptions")

    not_tv_show = request.args.get("not-tv")
    not_keyword = request.args.get("not-keyword")

    # seasMin is a string representing min seasons; default is 1
    seasMin = request.args.get("seasonMin")
    # seasMax is a string representing max seasons; default is 187
    seasMax = request.args.get("seasonMax")

    # yearMin is a string representing min years; default is 1946
    yearMin = request.args.get("yearMin")
    # yearMax is a string representing max years; default is 2021
    yearMax = request.args.get("yearMax")

    # simWeight is a string representing weight of similarity 1-100; default is 100
    simWeight = request.args.get("similarity-weight")
    # notWeight is a string representing weight of <not like> 1-100; default is 0
    notWeight = request.args.get("not-weight")

    #keywordWeight is a string representing weight of keyword 1-100; default is 100 if only keyword, 50 if both, 0 if not at all
    showKeywordWeight = request.args.get("show-keyword-weight")
    #showWeight is a string representing weight of show 1-100; default is 100 if only show, 50 if both, 0 if not at all
    notLikeShowKeywordWeight = request.args.get("not-like-show-keyword-weight")

    if query == "":
        query = None
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
            "similarity" : int(simWeight) / 100,
            "not like" : int(notWeight) / 100,
            "show/keyword" : int(showKeywordWeight) / 100,
            "not like show/keyword" :  int(notLikeShowKeywordWeight) / 100
        }
        query_show, not_like_query_show, data = final_search(
            slider_weights,
            query_show=query,
            n=10,
            free_search=free_search,
            genre=genre,
            not_like_show=not_tv_show,
            not_like_free_search=not_keyword,
        )

        output_query_msg = ""
        if (query and query_show) or free_search:
            output_query = ""
            if query and free_search:
                output_query = query_show + " (" + str(100 - int(showKeywordWeight)) + "%) and " + free_search + " (" + showKeywordWeight + "%) "
            elif query:
                output_query = query_show + " "
            elif free_search:
                output_query = free_search + " "
            output_query_msg += simWeight + "% Similar to " + output_query + " "

        if (not_tv_show and not_like_query_show) or not_keyword:
            output_query = ""
            if not_tv_show and not_keyword:
                output_query = not_like_query_show + " (" + str(100 - int(notLikeShowKeywordWeight)) + "%) and " + not_keyword + " (" + notLikeShowKeywordWeight + "%) " 
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

        return render_template(
            "results.html",
            descr=descript,
            data=data,
            show=query,
            keyword=free_search,
            output_query=output_query_msg,
        )
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


@irsystem.route(
    "/addrel/<int:rel>/<string:result>/<string:show>/<string:keywords>", methods=["POST"]
)
def relevence(rel, result, show, keywords):
    print("enterned")
    print(rel)
    print(result)
    print(show)
    result = result.lower()
    if show != "None" and keywords != "None":
        print("oh noosssssss")
        show = show.lower()
        updateData(result, rel, show=show, keywords=keywords)
    elif show != "None":
        show = show.lower()
        updateData(result, rel, show=show)
    else:
        result = result.lower()
        updateData(result, rel, keywords=keywords)

    return {"success": True}
