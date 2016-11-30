from flask import *
from extensions import db
import config
import requests

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods = ['GET'])
def wiki_route():
    search = False;
    docs = []
    query = request.args.get('q')
    weight = request.args.get('w')

    if query is not None and weight is not None:
        search = True

        # Sends get request to index server
        response = requests.get('http://' + config.env['host'] + ':' + str(config.env['port'] - 1) + '/?q=' + query + "&w=" + weight)
	print(response)

        response_json = json.loads(response.text)
        
        for item in response_json['hits']:
            # print item
            cur = db.cursor()
            cur.execute('SELECT * FROM ' + 'Documents WHERE docid = ' + str(item['docid']))
            docs.append(cur.fetchall()[0])

    options = {
        'search': search,
        'docs': docs
    }
    return render_template("wikipedia.html", **options)
