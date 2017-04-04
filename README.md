# mlabs-stats
This is a simple service for getting stats over HTTP for a mongodb instance running in mlabs or anywhere the HTTP interface is disabled.

# Usage
```shell
$ pip install -r requirements.txt
$ gunicorn --bind 0.0.0.0:${PORT} wsgi:app
$ curl http://db_user:db_pass@localhost:${PORT}/stats?host=${DB_HOST}&port=${DB_PORT}&db=${DB}
```
