FROM debian:latest

# Set default environment variables
ENV PORT=8000
ENV THREADS=1
ENV WORKERS=6

EXPOSE ${PORT}

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Add files to image
RUN mkdir /mlab-stats
ADD . /mlab-stats
WORKDIR /mlab-stats
RUN pip3 install -r requirements.txt

CMD gunicorn \
    -w ${WORKERS} \
    --threads ${THREADS} \
    --bind 0.0.0.0:${PORT} \
    --access-logfile - \
    --error-logfile - \
    -k gevent \
    --worker-connections 1000 \
    wsgi:app
