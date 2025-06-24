"""
Spark Streaming `consumer` for real-time commerce event processing.

This module implements a Spark Structured Streaming application that consumes events
from Apache Pulsar topics and processes them in real-time. It handles schema conversion,
data flattening, and outputs processed events as parquet files for downstream batch processing.

Key Features:
- Real-time streaming from Pulsar topics using pattern-based subscription
- Dynamic schema conversion from Pydantic models to Spark StructType
- JSON parsing and data structure flattening for analytics-friendly format
  * Note - current implementation doesn't flatten all the way. Needs improvement.
- Microbatch processing with parquet output for efficient storage
- Checkpoint management for fault tolerance and exactly-once processing

Data Flow:
1. Subscribes to merchant event topics in Pulsar
2. Parses JSON payloads using predefined schemas
3. Flattens nested structures to simple columns
4. Writes processed data as parquet files for batch consumption

Future Enhancements:
- Schema evolution support with versioned storage
- Data quality validation and error handling
- Multiple output sinks (cloud storage, datalake, etc.)
- Real-time analytics and aggregations
- Monitoring and alerting for stream health
- Full flattening of nested structures for easier analytics
"""

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

# For debugging purposes, also defined a simple schema
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


    # generated unique subscription names to avoid conflicts
    subscription_name = f"spark-sub-{datetime.now().strftime('%Y%m%d%H%M%S')}"


    # read stream from Pulsar topics
    # connector subscribes to all topics matching the pattern "merchant_*.events"
    # spark ingests messages in parallel
    df = spark.readStream \
        .format("pulsar") \
        .option("service.url", "pulsar://pulsar:6650") \
        .option("topicsPattern", "persistent://public/default/merchant_.*.events") \
        .option("subscription.name", subscription_name) \
        .option("subscription.type", "Exclusive") \
        .load()

    df.printSchema()

    # ** spark processes microbatches of data

    # Cast binary value (json payload) to string
    parsed_df = df.select(col("value").cast("string").alias("json_str"))
    parsed_df.printSchema()
    

    # Parse JSON string into structured data using the schema
    structured_df = parsed_df.select(from_json(col("json_str"), event_schema).alias("event"))
    structured_df.printSchema()
    

    # Flatten the structured data to access fields directly, minimal example
    flattened_df = flatten_df_leaf_names_deduped(structured_df)
    flattened_df.printSchema()

    # Get only the simple columns for now (not arrays or structs). jdbc to postgres process doesn't support these
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