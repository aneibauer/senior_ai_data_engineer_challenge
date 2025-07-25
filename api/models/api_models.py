from pydantic import BaseModel, AfterValidator
from typing import Annotated
from enum import Enum
import re
from pydantic import ValidationError


def _validate_timeframe_string(value: str) -> str:
    """
    Validates that the value is a single integer followed by 'h', 'd', or 'm'.
    - 'h': hours (max 48)
    - 'd': days (max 2)
    - 'm': minutes (max 2880)
    """
    match = re.fullmatch(r"(\d+)([hdm])", value)
    if not match:
        raise ValueError("Timeframe must be an integer followed by 'h', 'd', or 'm' (e.g., '2d', '12h', '30m').")
    num, unit = int(match.group(1)), match.group(2)
    if unit == 'd' and not (1 <= num <= 2):
        raise ValueError("Days ('d') must be between 1 and 2.")
    elif unit == 'h' and not (1 <= num <= 48):
        raise ValueError("Hours ('h') must be between 1 and 48.")
    elif unit == 'm' and not (1 <= num <= 2880):
        raise ValueError("Minutes ('m') must be between 1 and 2880.")
    return value


#TODO: future state would pull from a database of tenants. data generator currently collects those and doesn't do anything with them yet
class Tenants(Enum):
    MERCHANT_1 = "merchant_1"
    MERCHANT_2 = "merchant_2"
    MERCHANT_3 = "merchant_3"
    MERCHANT_4 = "merchant_4"
    MERCHANT_5 = "merchant_5"
    MERCHANT_6 = "merchant_6"
    MERCHANT_7 = "merchant_7"
    MERCHANT_8 = "merchant_8"
    MERCHANT_9 = "merchant_9"

class RealTimeMetricsResponse(BaseModel):
    tenant_id: Tenants
    event_count: int
    timeframe: Annotated[str, AfterValidator(_validate_timeframe_string)]