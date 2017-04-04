FROM debian:latest

# Set default environment variables
ENV PORT=8000

EXPOSE ${PORT}

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Add files to image
RUN mkdir /mlab-stats
ADD . /mlab-stats
WORKDIR /mlab-stats
RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 --bind 0.0.0.0:${PORT} --access-logfile - --error-logfile - wsgi:app
