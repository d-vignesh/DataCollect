# base image
FROM python:3-slim

# env variable to send python output to terminal
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /datacollect

# set working directory as our root dir
WORKDIR /datacollect

# copy current directory contents into our project root directory in container
ADD . /datacollect/

# install packages in requirements.txt
RUN pip install -r requirements.txt

# make migrations
CMD python manage.py makemigrations
CMD python manage.py migrate

# start the app
CMD gunicorn --workers 1 --bind :8000 --log-level INFO --worker-class gevent datacollect.wsgi:application