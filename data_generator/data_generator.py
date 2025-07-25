"""
Event Data Generator Main Module

This module provides functionality to generate synthetic ecommerce events for testing and development purposes.
It assembles complex Event objects by combining various context data including user behavior, business metrics,
interaction patterns, technical metadata, and machine learning features. The generated events are designed
to simulate real-world ecommerce activities and can be serialized for consumption by downstream systems.

Key Components:
- Event assembly with configurable number of tenants to simulate
- JSON serialization optimized for high throughput
- Modular context generation through specialized data factories
- Schema versioning for backward compatibility and evolution (hard-coded for now)

Future Enhancements:
- Replace random data generation with realistic ecommerce patterns:
  * Time-based seasonality (holiday shopping, weekend patterns)
  * Geographic clustering for user locations and behaviors
  * Product category correlations and cross-selling patterns
  * Realistic user journey flows (browse -> cart -> purchase)
  * Price sensitivity models based on user demographics
  * Inventory constraints affecting product availability
  * Session-based behavior modeling with realistic duration patterns
  * Churn prediction signals and customer lifecycle stages
- Implement data relationships and dependencies between events
- Add configurable business rules and constraints, e.g.:
  * Maximum number of items in cart
  * Minimum purchase amount for discounts
  * User segmentation based on behavior
- Simulate schema evolution with versioning support
- Add more validation via Pydantic and error handling for generated data 

"""

# Your senior-level implementation here
from data_generator.models.base import Event
from data_generator.models.event_data import EventData, EventType, EventSubType
from data_generator.models.user import UserContext
from data_generator.models.business import BusinessContext
from data_generator.models.interaction import InteractionContext
from data_generator.models.technical import TechnicalContext
from data_generator.models.ml import MLContext

from data_generator.factories.base_factory import make_event_metadata
from data_generator.factories.user_factory import make_user_context
from data_generator.factories.business_factory import make_business_context
from data_generator.factories.interaction_factory import make_interaction_context
from data_generator.factories.technical_factory import make_technical_context
from data_generator.factories.ml_factory import make_ml_context

import orjson  # faster than json
import random


def assemble_event(n: int=10) -> Event:
    """
    Assembles and returns an Event object populated with default and generated context data.
    Parameters:
        n (int): Number of tenants to choose from for tenant_id. Default is 10.
    Returns:
        Event: An Event instance with the following fields populated:
            - schema_version: The version of the event schema.
            - tenant_id: Identifier for the tenant (e.g., merchant).
            - partition_key: Key used for partitioning events (customizable).
            - event_metadata: Metadata about the event, generated by make_event_metadata().
            - event_data: EventData object containing event type, subtype, and various context objects.
            - technical_context: Technical context information, generated by make_technical_context().
            - ml_context: Machine learning context information, generated by make_ml_context().
    """
    return Event(
        schema_version="2.1", #TODO: update schema version as needed
        tenant_id=f"merchant_{random.randint(1,n)}",
        partition_key="user_region_hash",  # customize as needed
        event_metadata=make_event_metadata(),
        event_data=EventData(
            event_type=random.choice(list(EventType)),
            event_subtype=random.choice(list(EventSubType)),
            user_context=make_user_context(),
            business_context=make_business_context(),
            interaction_context=make_interaction_context()
        ),
        technical_context=make_technical_context(),
        ml_context=make_ml_context()
    )


def serialize_event(event: Event) -> bytes:
    return orjson.dumps(event.model_dump(mode="json"))


if __name__ == "__main__":
    event = assemble_event()
    payload = serialize_event(event)
    print(payload.decode())
    #payload can be sent to Pulsar 
