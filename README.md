# mongodb-over-http 
This is a simple service for running one-off queries over HTTP for mongodb. Useful for pinging a
database to make sure you can establish a new connection.

# Usage
```shell
$ pip install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl http://localhost:${PORT}/?uri=${MONGO_URI}&collection=${MONGO_COLLECTION}&query=${MONGO_QUERY}
```
