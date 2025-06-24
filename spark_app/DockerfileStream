# ./spark/Dockerfile
FROM bitnami/spark:3.5.0

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project contents into the container
COPY . .

ENV PYTHONPATH=/app:/app/data_generator

# Add entrypoint to run Spark job
CMD [ "/opt/bitnami/spark/bin/spark-submit", "--packages", "io.streamnative.connectors:pulsar-spark-connector_2.12:3.4.0.4", "--master", "local[*]", "spark_app/consumer.py" ]