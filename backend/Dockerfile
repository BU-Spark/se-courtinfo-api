FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client && \
    apt install -y tesseract-ocr


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .