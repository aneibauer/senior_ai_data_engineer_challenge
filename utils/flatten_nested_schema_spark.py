from pyspark.sql.functions import col
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType

def flatten_df(df: DataFrame, separator: str = "_") -> DataFrame:
    def _flatten(schema, prefix=None):
        cols = []
        for field in schema.fields:
            name = field.name
            full_name = f"{prefix}.{name}" if prefix else name
            alias = full_name.replace(".", separator)
            if isinstance(field.dataType, StructType):
                cols.extend(_flatten(field.dataType, full_name))
            else:
                cols.append(col(full_name).alias(alias))
        return cols

    return df.select(*_flatten(df.schema))