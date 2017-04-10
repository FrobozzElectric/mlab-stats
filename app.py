import json
from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/_healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})

@app.route('/stats')
def get_stats():
    try:
        auth = request.authorization
        username = auth.username
        password = auth.password
        host = request.args.get('host')
        database = request.args.get('db')
        db_port = int(request.args.get('port'))
    except:
        return jsonify({'error': 'missing parameters'})
    try:
        client = MongoClient(host, db_port)
        db = client[database]
        db.authenticate(username, password)
        if request.args.get('collection'):
            collection = request.args.get('collection')
            stats = db.command('collStats', collection)
        else:
            stats = db.command('dbStats')
        stats['error'] = 'none'
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
