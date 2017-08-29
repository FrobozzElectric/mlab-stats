# mlabs-stats
This is a simple service for getting stats over HTTP for a mongodb instance running in mLab or anywhere the HTTP interface is disabled.

# Usage
```shell
$ pip install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl http://localhost:${PORT}/?uri=${MONGO_URI}&collection=${MONGO_COLLECTION}&query=${MONGO_QUERY}
```
