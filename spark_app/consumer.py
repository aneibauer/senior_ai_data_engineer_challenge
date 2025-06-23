from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType
import os

# Optional: Load schema from a predefined Pydantic model or infer manually
event_schema = StructType().add("value", StringType())  # We’ll parse JSON later

def main():
    # Create Spark session with Pulsar connector
    spark = SparkSession.builder \
        .appName("PulsarConsumer") \
        .master("local[*]") \
        .config("spark.jars", "/opt/spark/jars/pulsar-spark-connector_2.12-3.1.0.1.jar") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Read stream from Pulsar topic(s)
    # connector subscribes to all topics matching the pattern "merchant_*.events"
    # spark ingests messages inparallel
    df = spark.readStream \
        .format("pulsar") \
        .option("service.url", "pulsar://pulsar:6650") \
        .option("startingOffsets", "earliest") \
        .option("topic", "persistent://public/default/merchant_*.events") \
        .load()

    # spark processes microbatches of data
    # Extract and parse the JSON from the message value
    parsed = df.selectExpr("CAST(value AS STRING) as json_str")

    # Optional: Save each raw message to a JSON file (e.g., for audit/debugging)
    query = parsed.writeStream \
        .outputMode("append") \
        .format("json") \
        .option("path", "/opt/spark/output") \
        .option("checkpointLocation", "/opt/spark/checkpoints") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()