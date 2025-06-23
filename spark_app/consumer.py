from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType
import os
from datetime import datetime

# Optional: Load schema from a predefined Pydantic model or infer manually
event_schema = StructType().add("value", StringType())  # We’ll parse JSON later

def main():
    # Create Spark session with Pulsar connector
    spark = SparkSession.builder \
        .appName("PulsarConsumer") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Read stream from Pulsar topic(s)
    # connector subscribes to all topics matching the pattern "merchant_*.events"
    # spark ingests messages inparallel

    # Optional: generate unique subscription name for testing
    subscription_name = f"spark-sub-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    df = spark.readStream \
        .format("pulsar") \
        .option("service.url", "pulsar://pulsar:6650") \
        .option("topicsPattern", "persistent://public/default/merchant_.*.events") \
        .option("subscription.name", subscription_name) \
        .option("subscription.type", "Exclusive") \
        .load()


    # df = spark.readStream \
    #     .format("pulsar") \
    #     .option("service.url", "pulsar://pulsar:6650") \
    #     .option("startingOffsets", "earliest") \ #this didn't work
    #     .option("topicsPattern", "persistent://public/default/merchant_*.events") \
    #     .load()

    df.printSchema()

    # spark processes microbatches of data
    # Extract and parse the JSON from the message value
    parsed = df.select(col("value").cast("string").alias("json_str"))

    # Save each raw message to a JSON file
    query = parsed.writeStream \
        .outputMode("append") \
        .format("json") \
        .option("path", "/opt/spark/output") \
        .option("checkpointLocation", "/opt/spark/checkpoints") \
        .start()

    # # Debug: Print messages to the console instead of writing to files
    # query = parsed.writeStream \
    #     .outputMode("append") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()