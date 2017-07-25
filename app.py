import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, Response

app = Flask(__name__)

def json_resp(data, status):
    return Response(json.dumps(data, 
    default=json_util.default, indent=4),
    mimetype="application/json",
    status=status)

@app.route('/_healthcheck')
def healthcheck():
    return json_resp({'error': None}, 200)

@app.route('/<host>:<int:db_port>/<database>/<collection>/<command>')
def run_command(host, db_port, database, collection, command):
    try:
        auth = request.authorization
        username = auth.username
        password = auth.password
    except:
        return json_resp({'error': 'missing credentials'}, 401)
    try:
        client = MongoClient(host, db_port, serverSelectionTimeoutMS=5000)
        db = client[database]
        db.authenticate(username, password)
        collection = db[collection]
        if request.args.get('q'):
            query = json.loads(request.args.get('q'))
        else:
            query = None
        if command == 'command':
            data = db.command(query)
        elif command == 'find':
            data = list(collection.find(query))
        else:
            raise ValueError('unsupported')
        client.close()
    except Exception as error:
        return json_resp({'error': str(error)}, 500)
    return json_resp(data, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
