FROM python:3.8.3-slim-buster

ADD requirements.txt /langauge/core/dispatcher/requirements.txt
WORKDIR /
ENV PYTHONPATH /

RUN pip3 install -r /langauge/core/dispatcher/requirements.txt

ADD . /langauge/core/dispatcher

# run the worker
ENTRYPOINT celery -A langauge.core.dispatcher.tasks.pubMedBERT worker --loglevel=INFO --concurrency=2