import json
from bson import json_util
from pymongo import MongoClient
from flask import abort, Flask, jsonify, make_response, request, Response

app = Flask(__name__)


def abort_request(message, status):
    abort(make_response(jsonify(error=message), status))

def authenticate(request):
    try:
        if request.authorization:
            auth = request.authorization
            username = auth.username
            password = auth.password
        elif request.args.get('auth'):
            auth = request.args.get('auth')
            username = auth.split(':')[0]
            password = auth.split(':')[1]
        else:
            abort_request('missing credentials', 401)
    except:
        abort_request('credentials in incorrect format', 400)
    return username, password


def mongo_find(collection, query, sort, limit):
    if limit and sort:
        return collection.find(query).sort(sort).limit(limit)
    elif sort:
        return collection.find(query).sort(sort)
    elif limit:
        return collection.find(query).limit(limit)
    else:
        return collection.find(query)


def json_resp(data, status):
    return Response(
            json.dumps(
                data,
                default=json_util.default, indent=4),
            mimetype="application/json",
            status=status)


@app.route('/_healthcheck')
def healthcheck():
    return json_resp({'error': None}, 200)


@app.route('/<host>:<int:db_port>/<database>/<collection>')
def run_command(host, db_port, database, collection):
    if not request.args.get('query') and not request.args.get('command'):
        abort_request('missing \'query\' or \'command\'', 422)
    username, password = authenticate(request)
    try:
        data = {'error': None, 'results': []}
        client = MongoClient(host, db_port, serverSelectionTimeoutMS=5000)
        db = client[database]
        db.authenticate(username, password)
        collection = db[collection]
        if request.args.get('query'):
            sort = None
            if request.args.get('sort'):
                sort_raw = json.loads(request.args.get('sort'))
                sort = []
                for key, value in sort_raw.items():
                    sort.append((key, value))
            limit = None
            if request.args.get('limit'):
                limit = int(request.args.get('limit'))
            query = json.loads(request.args.get('query'))
            data['results'].append(list(mongo_find(
                collection,
                query,
                sort,
                limit)))
        if request.args.get('command'):
            command = json.loads(request.args.get('command'))
            data['results'].append(db.command(command))
        client.close()
    except Exception as error:
        abort_request(str(error), 500)
    return json_resp(data, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
