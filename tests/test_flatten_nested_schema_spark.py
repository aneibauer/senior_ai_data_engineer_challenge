import pytest
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, StructType

from utils.flatten_nested_schema_spark import flatten_df

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    yield spark
    spark.stop()

def test_flatten_df_with_nested_schema(spark):
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("info", StructType([
            StructField("name", StringType(), True),
            StructField("address", StructType([
                StructField("city", StringType(), True),
                StructField("zip", StringType(), True)
            ]), True)
        ]), True)
    ])

    data = [
        (1, ("Alice", ("Wonderland", "12345"))),
        (2, ("Bob", ("Builderland", "67890")))
    ]

    df = spark.createDataFrame(data, schema=schema)
    flat_df = flatten_df(df)
    flat_df.printSchema()
    flat_df.show()

    # The flattened columns should be: id, info_name, info_address_city, info_address_zip
    expected_columns = {"id", "info_name", "info_address_city", "info_address_zip"}
    assert set(flat_df.columns) == expected_columns