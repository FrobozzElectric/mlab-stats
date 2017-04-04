import json
from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/_healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})

@app.route('/stats')
def get_stats():
    auth = request.authorization
    username = auth.username
    password = auth.password
    host = request.args.get('host')
    database = request.args.get('db')
    db_port = int(request.args.get('port'))
#    print('mongodb://' + username + ':' + password + '@' + host + ':' + str(db_port) + '/' + database)
    try:
        client = MongoClient(host, db_port)
        db = client[database]
        db.authenticate(username, password)
        stats = db.command('dbStats')
    except:
        raise
    return jsonify(stats)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
