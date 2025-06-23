# ./spark/Dockerfile
FROM bitnami/spark:latest

WORKDIR /app

# Copy Spark streaming app into the container
COPY consumer.py .

# Add entrypoint to run Spark job
CMD [ "/opt/bitnami/spark/bin/spark-submit", "--packages", "io.streamnative.connectors:pulsar-spark-connector_2.13:3.4.1.3", "--master", "local[*]", "consumer.py" ]