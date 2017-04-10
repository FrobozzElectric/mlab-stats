import json
from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/_healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})

@app.route('/<host>:<int:db_port>/<database>/<command>')
def run_command(host, db_port, database, command):
    try:
        auth = request.authorization
        username = auth.username
        password = auth.password
    except:
        return jsonify({'error': 'missing credentials'}), 401
    try:
        client = MongoClient(host, db_port)
        db = client[database]
        db.authenticate(username, password)
        if request.args.get('arg'):
            arg = request.args.get('arg')
            stats = db.command(command, arg)
        else:
            stats = db.command(command)
        stats['error'] = 'none'
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
