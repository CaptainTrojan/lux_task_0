FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir scrapy psycopg2-binary

CMD scrapy runspider main.py
