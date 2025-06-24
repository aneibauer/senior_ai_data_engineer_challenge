from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
import os
from datetime import datetime

from data_generator.models.base import Event
from utils.pydantic_to_spark_schema import pydantic_to_struct_type
from utils.flatten_nested_schema_spark import flatten_df_leaf_names_deduped

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
    

    # Parse JSON string into structured data using the schema
    structured_df = parsed_df.select(from_json(col("json_str"), event_schema).alias("event"))
    # structured_df = parsed_df.select(from_json(col("json_str"), simple_schema).alias("event"))
    structured_df.printSchema()
    

    # Flatten the structured data to access fields directly, minimal example
    flattened_df = flatten_df_leaf_names_deduped(structured_df)
    flattened_df.printSchema()

    # Get only the simple columns for now (not arrays or structs)
    simple_cols = [
        field.name for field in flattened_df.schema.fields
        if not isinstance(field.dataType, (ArrayType, StructType))
    ]
    print("Simple columns:", simple_cols)

    # Debug: Print messages to the console instead of writing to files
    # query = flattened_df.writeStream \
    #     .outputMode("append") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start()

    # Save each microbatch as parquet files
    # future: write to versioned storage based on schema version to support schema evolution
    query = flattened_df.select([col for col in simple_cols]).writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", "/opt/spark/parquet_output") \
        .option("checkpointLocation", "/opt/spark/checkpoints") \
        .option("fs.permissions.umask-mode", "022") \
        .start()


    query.awaitTermination()

if __name__ == "__main__":
    main()