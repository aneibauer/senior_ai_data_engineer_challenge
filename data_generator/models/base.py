from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
import random

class SourceSystem(Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API = "api"
    batch_import = "batch_import"
# This enum can be extended with more source systems as needed.


class ProcessingFlags(BaseModel):
    requires_enrichment: bool
    pii_contains: bool
    gdpr_subject: bool
    audit_required: bool


class EventMetadata(BaseModel):
    event_id: str
    correlation_id: str
    causation_id: Optional[str]
    timestamp: datetime
    ingestion_timestamp: datetime
    source_system: SourceSystem
    event_version: str
    processing_flags: ProcessingFlags


class Event(BaseModel):
    schema_version: str
    tenant_id: str
    partition_key: str
    event_metadata: EventMetadata
    event_data: dict  # Placeholder until EventData model is defined
    technical_context: Optional[dict] = None  # To be replaced with TechnicalContext
    ml_context: Optional[dict] = None         # To be replaced with MLContext


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

#tested and working
if __name__ == "__main__":
    event = make_base_event()
    print(event.model_dump_json(indent=2))  # Print the event in a readable JSON form