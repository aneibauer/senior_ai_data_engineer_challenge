import os
import shutil
from pyspark.sql import SparkSession
import time
from typing import List

PARQUET_DIR = "/opt/spark/parquet_output"
ARCHIVE_DIR = os.path.join(PARQUET_DIR, "archive")

POSTGRES_URL = "jdbc:postgresql://postgres:5432/events"
POSTGRES_PROPERTIES = { #TODO: don't hardcode these here!
    "user": "user",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

def get_parquet_files(directory, min_age_secs=30) -> List[str]:
    now = time.time()
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if (
            f.endswith(".parquet") and 
            os.path.isfile(os.path.join(directory, f)) and
            (now - os.path.getmtime(os.path.join(directory, f))) > min_age_secs #helps avoid partial writes
        )
    ]

def archive_files(files, archive_dir=ARCHIVE_DIR) -> None:
    os.makedirs(archive_dir, exist_ok=True)
    for f in files:
        shutil.move(f, os.path.join(archive_dir, os.path.basename(f)))


def main():
    spark = SparkSession.builder \
        .appName("BatchParquetToPostgres") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print(f"Looking for parquet files in {PARQUET_DIR}...")
    parquet_files = get_parquet_files(PARQUET_DIR)
    print(parquet_files)
    print(f"Found {len(parquet_files)} parquet files to process.")
    if not parquet_files:
        print("No new parquet files to process.")
        return

    print(f"Processing files: {parquet_files}")

    # Read all new parquet files into a single DataFrame
    df = spark.read.parquet(*parquet_files)

    # Write to Postgres (append mode)
    df.write.jdbc(
        url=POSTGRES_URL,
        table="commerce_events_table",  # should create table from dataframe schema if it doesn't exist
        mode="append",
        properties=POSTGRES_PROPERTIES
    )

    # Archive processed files
    archive_files(parquet_files)
    print(f"Archived files: {parquet_files}")

    spark.stop()

if __name__ == "__main__":
    main()

    # sample_parquet_dir = "./parquet_output"
    # parquet_files = get_parquet_files(sample_parquet_dir, min_age_secs=30)
    # num_parquet_files = len(parquet_files)
    # print(parquet_files)

    # sample_archive = os.path.join(sample_parquet_dir, "archive")
    # print(sample_archive)
    # archive_files(parquet_files, archive_dir=sample_archive)

    # new_parquet_files = get_parquet_files(sample_parquet_dir)
    # num_parquet_files_after = len(new_parquet_files)
    # num_parquet_files_archived = num_parquet_files - num_parquet_files_after
    # print(num_parquet_files_archived)