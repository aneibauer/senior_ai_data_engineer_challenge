from typing import get_args, get_origin, Union, List, Dict, Optional, Type, Any
from enum import Enum
from pydantic import BaseModel
from pyspark.sql.types import *

from data_generator.data_generator import assemble_event
from data_generator.models.base import Event

# Convert Pydantic models to Spark StructType
def pydantic_to_struct_type(model: type[BaseModel]) -> StructType:
    fields = []
    for name, field in model.model_fields.items():
        spark_type = _convert_type(field.annotation)
        fields.append(StructField(name, spark_type, nullable=True))
    return StructType(fields)


def _convert_type(py_type):
    origin = get_origin(py_type)
    args = get_args(py_type)

    # Handle Optional[X]
    if origin is Union and type(None) in args:
        non_none_args = [arg for arg in args if arg is not type(None)]
        return _convert_type(non_none_args[0])  # Simplified for Optional[X]

    # Handle list/array
    if origin in (list, List):
        return ArrayType(_convert_type(args[0]))

    # Handle dict (basic case)
    if origin in (dict, Dict):
        return MapType(StringType(), _convert_type(args[1]))  # Key assumed str

    # Handle Enums
    if isinstance(py_type, type) and issubclass(py_type, Enum):
        return StringType()

    # Handle nested Pydantic models
    if isinstance(py_type, type) and issubclass(py_type, BaseModel):
        return pydantic_to_struct_type(py_type)

    # Handle primitive types
    return _python_type_to_spark_type(py_type)


def _python_type_to_spark_type(py_type):
    mapping = {
        str: StringType(),
        int: IntegerType(),
        float: DoubleType(),
        bool: BooleanType(),
        bytes: BinaryType(),
    }
    return mapping.get(py_type, StringType())  # Fallback to string



if __name__ == "__main__":
    
    event = assemble_event()
    json = event.model_dump_json(indent=2)
    
    for field_name, field_info in Event.model_fields.items():
        print(f"FIELD: {field_name}, FIELD_TYPE: {field_info.annotation}")
        origin = get_origin(field_info.annotation)
        args = get_args(field_info.annotation)
        print(f"ORIGIN: {origin}, ARGS: {args} \n")

    event_schema = pydantic_to_struct_type(Event)
    print(event_schema)
