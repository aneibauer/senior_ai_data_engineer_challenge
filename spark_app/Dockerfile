# ./spark/Dockerfile
FROM bitnami/spark:3.5.0

WORKDIR /app

# Copy Spark streaming app into the container
COPY consumer.py .

# Add entrypoint to run Spark job
CMD [ "/opt/bitnami/spark/bin/spark-submit", "--packages", "io.streamnative.connectors:pulsar-spark-connector_2.12:3.4.0.4", "--master", "local[*]", "consumer.py" ]