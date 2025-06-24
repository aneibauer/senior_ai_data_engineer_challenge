from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
import random

from data_generator.models.base import SourceSystem, ProcessingFlags, EventMetadata, Event


def make_event_metadata() -> EventMetadata:
    return EventMetadata(
        event_id=str(uuid.uuid4()),
        correlation_id=str(uuid.uuid4()),
        causation_id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        ingestion_timestamp=datetime.now(),
        source_system=random.choice(list(SourceSystem)),
        event_version="1.0",
        processing_flags=ProcessingFlags(
            requires_enrichment=random.choice([True, False]),
            pii_contains=random.choice([True, False]),
            gdpr_subject=random.choice([True, False]),
            audit_required=random.choice([True, False])
        )
    )

# see data_generator.data_generator.assemble_event() for implementation
def make_base_event() -> Event:
    return Event(
        schema_version="2.1",
        tenant_id="merchant_12345",
        partition_key="us-east-hash",
        event_metadata=make_event_metadata(),
        event_data={},  # fill this in later with full nested structure
        technical_context={},
        ml_context={}
    )

# #tested and working
# if __name__ == "__main__":
#     event = make_base_event()
#     print(event.model_dump_json(indent=2))  # Print the event in a readable JSON form