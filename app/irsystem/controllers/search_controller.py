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
    if free_search == "":
        free_search = None
    genre = request.args.get("genre")
    if genre == "":
        genre = None

    if query or free_search:
        query_show, data = final_search(query_show=query, n=10, free_search=free_search, genre=genre)
        output_query_msg= ""
        if query:
            output_query_msg += "Similar Show: " + query_show + " "
        if free_search:
            output_query_msg += "Keywords: " + free_search + " "
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
