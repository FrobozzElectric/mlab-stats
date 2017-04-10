# mlabs-stats
This is a simple service for getting stats over HTTP for a mongodb instance running in mLab or anywhere the HTTP interface is disabled.

# Usage
```shell
$ pip install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl http://${DB_USER}:${DB_PASS}@localhost:${PORT}/{DB_HOST}:${DB_PORT}/${DB}/${DB_COMMAND}
```
