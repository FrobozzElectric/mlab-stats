import json
from bson import json_util
from pymongo import MongoClient
from flask import abort, Flask, jsonify, make_response, request, Response

app = Flask(__name__)


def abort_request(message, status):
    abort(make_response(jsonify(error=message), status))


def query(collection, request, data):
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
    data['results'].append(list(
            mongo_find(collection, query, sort, limit)))
    return data


def command(db, request, data):
    command = json.loads(request.args.get('command'))
    data['results'].append(db.command(command))
    return data


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


@app.route('/')
def connection_string():
    if not request.args.get('uri'):
        abort_request('missing \'uri\' parameter', 422)
    if not request.args.get('query') and not request.args.get('command'):
        abort_request('missing \'query\' or \'command\'', 422)
    uri = request.args.get('uri').strip('"').strip("'")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        data = {'error': None, 'results': []}
        db = client.get_default_database()
        if request.args.get('query'):
            if not request.args.get('collection'):
                abort_request('missing \'collection\' parameter', 422)
            collection = db[request.args.get('collection')]
            data = query(collection, request, data)
        if request.args.get('command'):
            data = command(db, request, data)
        client.close()
    except Exception as error:
        abort_request(str(error), 500)
    return json_resp(data, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
