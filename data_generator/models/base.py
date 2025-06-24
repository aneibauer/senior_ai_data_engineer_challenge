from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from data_generator.models.technical import TechnicalContext
from data_generator.models.ml import MLContext
from data_generator.models.event_data import EventData

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
    event_data: EventData
    technical_context: Optional[TechnicalContext] = None
    ml_context: Optional[MLContext] = None
