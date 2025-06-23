# ./spark/Dockerfile
FROM bitnami/spark:latest

WORKDIR /app

# Copy Spark streaming app into the container
COPY consumer.py .

# Add entrypoint to run Spark job
CMD [ "/opt/bitnami/spark/bin/spark-submit", "--master", "local[*]", "consumer.py" ]