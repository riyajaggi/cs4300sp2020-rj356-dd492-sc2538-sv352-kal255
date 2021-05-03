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
    genre = None
    num = 3
    if not query:
        data = []
        output_message = ""
        genre_list = ""
    else:
        output_message = "Your results for " + query
        # data = jaccardRanking(query)
        # genre_list = genre_jacc_sim(genre)
        data = final_search(query_show=query, n=num, free_search=None, genre = genre)
        if len(data) == 0:
            abort(500)
        descript = des(data)
        return render_template("results.html", descr=descript, data=data, n=num)

    return render_template(
        "search.html",
        name=project_name,
        netid=net_id,
        output_message=output_message,
        data=data,
        genre_list=genre_list,
    )
