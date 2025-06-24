from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField
import os
from datetime import datetime

from data_generator.models.base import Event
from scripts.pydantic_to_spark_schema import pydantic_to_struct_type

# Convert Pydantic models to Spark StructType
event_schema = pydantic_to_struct_type(Event)
print("----- Event schema:")
print(event_schema)

simple_schema = StructType([
    StructField("schema_version", StringType(), True),
    StructField("tenant_id", StringType(), True),
    StructField("partition_key", StringType(), True),
    StructField("event_metadata", StringType(), True),
    StructField("event_data", StringType(), True),
    StructField("technical_context", StringType(), True),
    StructField("ml_context", StringType(), True)
])

def main():
    # Create Spark session with Pulsar connector
    spark = SparkSession.builder \
        .appName("PulsarConsumer") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # Read stream from Pulsar topic(s)
    # connector subscribes to all topics matching the pattern "merchant_*.events"
    # spark ingests messages in parallel

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

    # Cast binary value (json payload) to string
    parsed_df = df.select(col("value").cast("string").alias("json_str"))
    parsed_df.printSchema()
    
    # Debug: Print parsed messages to the console
    # parsed_df.writeStream \
    #     .outputMode("append") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start() \
    #     .awaitTermination()
    

    # Parse JSON string into structured data using the schema
    # structured_df = parsed_df.select(from_json(col("json_str"), event_schema).alias("event"))
    structured_df = parsed_df.select(from_json(col("json_str"), simple_schema).alias("event"))
    structured_df.printSchema()


    # Debug: Print messages to the console instead of writing to files
    # query = structured_df.select("event").writeStream \
    #     .outputMode("append") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start()
    

    # Flatten the structured data to access fields directly, minimal example
    flattened_df = structured_df.select(
        col("event.schema_version").alias("schema_version"),
        col("event.tenant_id").alias("tenant_id"),
        col("event.partition_key").alias("partition_key"),
        col("event.event_metadata").alias("event_metadata"),
        col("event.event_data").alias("event_data"),
        col("event.technical_context").alias("technical_context"),
        col("event.ml_context").alias("ml_context")
    )

    # Debug: Print messages to the console instead of writing to files
    query = flattened_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    # Save each raw message to a JSON file
    # query = parsed_df.writeStream \
    #     .outputMode("append") \
    #     .format("json") \
    #     .option("path", "/opt/spark/output") \
    #     .option("checkpointLocation", "/opt/spark/checkpoints") \
    #     .start()


    query.awaitTermination()

if __name__ == "__main__":
    main()