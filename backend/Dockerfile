FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install -y postgresql-client

COPY requirements.txt  /app
RUN pip install -r requirements.txt