FROM postgres:13

ENV POSTGRES_USER default
ENV POSTGRES_PASSWORD secret123
ENV POSTGRES_DB default_db

COPY init.sql /docker-entrypoint-initdb.d/
