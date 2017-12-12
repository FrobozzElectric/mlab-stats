import logging
from app import app


class LogFilter(logging.Filter):
    def filter(self, record):
        if '/_healthcheck' in record.getMessage():
            return False
        return True


logger = logging.getLogger('gunicorn.access')
logger.addFilter(LogFilter())

if __name__ == '__main__':
    app.run()
