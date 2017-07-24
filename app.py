import json
import time
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
    if request.args.get('delay'):
        delay = request.args.get('delay')
        print(delay)
        time.sleep(int(delay))
    return json_resp({'status': 'ok'}, 200)

@app.route('/<host>:<int:db_port>/<database>/<command>')
def run_command(host, db_port, database, command):
    try:
        auth = request.authorization
        username = auth.username
        password = auth.password
    except:
        return json_resp({'error': 'missing credentials'}, 401)
    try:
        client = MongoClient(host, db_port)
        db = client[database]
        db.authenticate(username, password)
        if request.args.get('arg'):
            arg = request.args.get('arg')
            data = db.command(command, arg)
        else:
            data = db.command(command)
        data['error'] = 'none'
    except Exception as error:
        return json_resp({'error': str(error)}, 500)
    return json_resp(data, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
