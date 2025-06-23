from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import random
import uuid

# --- Infrastructure Metadata ---

class InfrastructureMetadata(BaseModel):
    processing_region: str
    availability_zone: str
    server_instance: str
    load_balancer: str
    cdn_edge_location: str


# --- Performance Telemetry ---

class PerformanceTelemetry(BaseModel):
    request_id: str
    trace_id: str
    parent_span_id: str
    processing_time_ms: int
    memory_usage_mb: int 
    cpu_utilization: float = Field(ge=0, le=1, description="CPU utilization percentage")
    network_latency_ms: int
    database_query_time_ms: int
    cache_hit_ratio: float = Field(ge=0, le=1, description="Cache hit ratio between 0 and 1")


# --- Security Context ---

class SecurityFlags(BaseModel):
    suspicious_user_agent: bool
    tor_exit_node: bool
    known_bot: bool
    geo_blocked: bool


class SecurityContext(BaseModel):
    request_signature: str
    api_key_hash: str
    rate_limit_remaining: int
    security_flags: SecurityFlags


# --- Data Lineage ---

class TransformationTypes(Enum):
    PII_TOKENIZATION = 'pii_tokenization'
    GEO_ENRICHMENT = 'geo_enrichment'
    FRAUD_SCORING = 'fraud_scoring'

class DownstreamTargets(Enum):
    DATA_WAREHOUSE = 'data_warehouse'
    ML_FEATURE_STORE = 'ml_feature_store'
    AUDIT_LOG = 'audit_log'

class UpstreamSystems(Enum):
    USER_SERVICE = 'user_service'
    PRODUCT_CATALOG = 'product_catalog'
    INVENTORY_SERVICE = 'inventory_service'

class DataLineage(BaseModel):
    upstream_systems: List[UpstreamSystems]
    transformation_applied: List[TransformationTypes]
    downstream_targets: List[DownstreamTargets]


# --- Full Technical Context ---

class TechnicalContext(BaseModel):
    infrastructure_metadata: InfrastructureMetadata
    performance_telemetry: PerformanceTelemetry
    security_context: SecurityContext
    data_lineage: DataLineage