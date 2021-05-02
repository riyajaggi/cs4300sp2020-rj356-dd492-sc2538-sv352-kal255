from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
# from scripts.transcript_similarity import *
from scripts.backend_script import *
from scripts.transcripts.genre_similarity import *
from scripts.desc import *

project_name = "Stream On"
net_id = "Divya Damodaran: dd492, Riya Jaggi: rj356, Siddhi Chordia: sc2538, Sidharth Vadduri: sv352, Kendall Lane: kal255"


@irsystem.route('/', methods=['GET'])
def search():
    tv_show = request.args.get('search')
    free_search = request.args.get('free_search')
    # genre = request.args.get('genre')
    # genre = "Comedy"
    if not tv_show:
        data = []
        output_message = ''
        genre_list = ''
    else:
        output_message = "Your results for " + tv_show
        # data = jaccardRanking(query)
        # genre_list = genre_jacc_sim(genre)
        if free_search is not None:
            data = final_search(tv_show, 10)
        else:
            data = final_search(tv_show, 10, free_search)
        descript = des(data)
        return render_template('results.html', descr=descript, data=data)

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, genre_list=genre_list)
