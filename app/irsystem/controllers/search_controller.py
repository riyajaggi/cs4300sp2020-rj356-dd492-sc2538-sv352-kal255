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
<<<<<<< HEAD
    query = request.args.get("search")
    free_search = request.args.get("freeSearch")
    genre = None
    num = 3
    if not query:
=======
    tv_show = request.args.get('search')
    free_search = request.args.get('free_search')
    # genre = request.args.get('genre')
    # genre = "Comedy"
    if not tv_show:
>>>>>>> e59287d57ef96d58885479e4e797fcd0ee990300
        data = []
        output_message = ""
        genre_list = ""
        free_search = ""
    else:
        output_message = "Your results for " + tv_show
        # data = jaccardRanking(query)
        # genre_list = genre_jacc_sim(genre)
<<<<<<< HEAD
        data = final_search(query_show=query, n=num, free_search=free_search, genre = genre)
        if len(data) == 0:
            abort(500)
=======
        if free_search is not None:
            data = final_search(tv_show, 10)
        else:
            data = final_search(tv_show, 10, free_search)
>>>>>>> e59287d57ef96d58885479e4e797fcd0ee990300
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
