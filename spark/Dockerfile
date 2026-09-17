FROM quay.io/jupyter/pyspark-notebook:latest

USER root

# PostgreSQL JDBC driver
RUN wget -O /usr/local/spark/jars/postgresql-42.7.7.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.7.jar

USER ${NB_UID}