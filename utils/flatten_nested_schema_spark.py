from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType
from collections import defaultdict

def flatten_df_leaf_names_deduped(df: DataFrame) -> DataFrame:
    """
    Flattens a nested Spark DataFrame by selecting all leaf columns and deduplicating column names.

    For each leaf column in the DataFrame:
    - If the leaf name is unique, it is used as the column alias.
    - If the leaf name is duplicated (appears in multiple nested paths), the alias is constructed by joining the last two segments of the full path with an underscore (e.g., 'address_city').

    Args:
        df (DataFrame): The input Spark DataFrame with potentially nested (struct) columns.

    Returns:
        DataFrame: A flattened DataFrame with deduplicated column names.
    """
    # Step 1: Collect all full paths and their leaf names
    paths = []

    def _collect_paths(schema, prefix=""):
        for field in schema.fields:
            full_path = f"{prefix}.{field.name}" if prefix else field.name
            if isinstance(field.dataType, StructType):
                _collect_paths(field.dataType, full_path)
            else:
                paths.append((full_path, field.name))

    _collect_paths(df.schema)

    # Step 2: Count duplicates of leaf names
    name_counts = defaultdict(int)
    for _, name in paths:
        name_counts[name] += 1

    # Step 3: Create column expressions with deduped aliases
    cols = []
    for full_path, name in paths:
        if name_counts[name] == 1:
            alias = name
        else:
            # Use last two segments if duplicate exists: e.g., address_city
            segments = full_path.split(".")
            alias = "_".join(segments[-2:]) if len(segments) >= 2 else full_path
        cols.append(col(full_path).alias(alias))

    return df.select(*cols)