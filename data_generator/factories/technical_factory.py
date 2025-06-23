from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import random
import uuid

from data_generator.models.technical import (
    InfrastructureMetadata,
    PerformanceTelemetry,
    SecurityFlags,
    SecurityContext,
    TransformationTypes,
    DownstreamTargets,
    UpstreamSystems,
    DataLineage,
    TechnicalContext
)   

# --- Data Generators ---
def make_infrastructure_metadata() -> InfrastructureMetadata:
    return InfrastructureMetadata(
        processing_region=random.choice(['us-east-1', 'eu-west-1', 'ap-southeast-1']),
        availability_zone=random.choice(['us-east-1a', 'us-east-1b', 'eu-west-1a']),
        server_instance=f"i-{uuid.uuid4().hex[:8]}",
        load_balancer=f"lb-{uuid.uuid4().hex[:6]}",
        cdn_edge_location=random.choice(['edge-nyc', 'edge-lon', 'edge-sin'])
    )

def make_performance_telemetry() -> PerformanceTelemetry:
    return PerformanceTelemetry(
        request_id=str(uuid.uuid4()),
        trace_id=str(uuid.uuid4()),
        parent_span_id=str(uuid.uuid4()),
        processing_time_ms=random.randint(10, 5000),
        memory_usage_mb=random.randint(128, 8192),
        cpu_utilization=round(random.uniform(0.01, 1.0), 2),
        network_latency_ms=random.randint(1, 500),
        database_query_time_ms=random.randint(1, 1000),
        cache_hit_ratio=round(random.uniform(0.0, 1.0), 2)
    )

def make_security_flags() -> SecurityFlags:
    return SecurityFlags(
        suspicious_user_agent=random.choice([True, False]),
        tor_exit_node=random.choice([True, False]),
        known_bot=random.choice([True, False]),
        geo_blocked=random.choice([True, False])
    )

def make_security_context() -> SecurityContext:
    return SecurityContext(
        request_signature=f"sig_{uuid.uuid4().hex[:10]}",
        api_key_hash=f"key_{uuid.uuid4().hex[:10]}",
        rate_limit_remaining=random.randint(0, 1000),
        security_flags=make_security_flags()
    )

def make_data_lineage() -> DataLineage:
    return DataLineage(
        upstream_systems=random.sample(list(UpstreamSystems), k=random.randint(1, len(UpstreamSystems))),
        transformation_applied=random.sample(list(TransformationTypes), k=random.randint(1, len(TransformationTypes))),
        downstream_targets=random.sample(list(DownstreamTargets), k=random.randint(1, len(DownstreamTargets)))
    )

def make_technical_context() -> TechnicalContext:
    return TechnicalContext(
        infrastructure_metadata=make_infrastructure_metadata(),
        performance_telemetry=make_performance_telemetry(),
        security_context=make_security_context(),
        data_lineage=make_data_lineage()
    )

# if __name__ == "__main__":
#     # Example usage
#     tech_context = make_technical_context()
#     print(tech_context.model_dump_json(indent=2))