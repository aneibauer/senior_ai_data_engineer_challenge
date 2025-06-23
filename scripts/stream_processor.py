"""
Senior Data Engineering Challenge: Advanced Real-Time Stream Processor

SENIOR-LEVEL REQUIREMENTS:
Design and implement a production-grade, distributed stream processing system
capable of handling enterprise-scale e-commerce event streams with strict
SLA requirements and multi-tenant isolation.

ADVANCED ARCHITECTURE EXPECTATIONS:
- Process 10K+ events/second with <50ms end-to-end latency
- Implement exactly-once processing semantics with idempotency guarantees
- Design multi-tenant data isolation with performance optimization
- Handle schema evolution without downtime (backward/forward compatibility)
- Implement sophisticated state management with fault tolerance
- Build complex event correlation across sessions, users, and time windows
- Design real-time feature engineering pipeline for ML model serving

COMPLEX EVENT PROCESSING REQUIREMENTS:
- Advanced windowing strategies (tumbling, sliding, session-based)
- Cross-stream joins with temporal constraints
- Complex aggregations with custom business logic
- Event-time vs processing-time handling with watermarking
- Late-arriving data handling with configurable tolerance
- Real-time model scoring integration with sub-millisecond latency

PRODUCTION OPERATIONAL REQUIREMENTS:
- Comprehensive error handling with circuit breakers
- Backpressure management and load shedding
- Distributed tracing and structured logging
- Custom metrics emission for business and technical monitoring
- Graceful shutdown and startup procedures
- Memory management for high-throughput processing

SENIOR EVALUATION CRITERIA:
- Can you architect distributed streaming systems at scale?
- Do you understand streaming semantics and trade-offs?
- Can you implement complex business logic in streaming context?
- Do you design for operational excellence and observability?
- Can you optimize for both performance and resource efficiency?
- Do you handle edge cases and failure scenarios properly?

TECHNOLOGY STACK DECISION:
Choose and justify one of: Kafka+Flink, Pulsar+Spark, or Cloud-Native Beam
Your choice will be evaluated based on requirements fit and trade-off analysis.

This is a senior-level distributed systems challenge requiring deep expertise
in stream processing, event-driven architectures, and production operations.
"""

# Your senior-level implementation here
import pulsar
import orjson
from time import sleep

from data_generator.data_generator import assemble_event
from data_generator.models.base import Event


def send_event_to_pulsar(event:Event, client):
    """
    Sends an event to an Apache Pulsar topic specific to the event's tenant.

    Args:
        event (pydantic Event): The event object to be sent. Must have a `tenant_id` attribute.
        client: The Pulsar client instance used to create the producer.

    Side Effects:
        - Serializes the event to JSON using orjson.
        - Sends the serialized event to the Pulsar topic named after the tenant.
        - Prints a confirmation message to stdout.
        - Closes the Pulsar producer after sending.

    Raises:
        Any exceptions raised by the Pulsar client or orjson during serialization or sending.
    """
    topic = f"persistent://public/default/{event.tenant_id}.events"
    producer = client.create_producer(topic)

    payload = orjson.dumps(event.model_dump_json())
    producer.send(payload)

    print(f"------------- Sent event to {topic}") #TODO: make more sophisticated logger wrapper
    producer.close()


def run_event_loop(rate_per_sec: int = 1):
    client = pulsar.Client("pulsar://localhost:6650")  # Use 'pulsar' if running inside Docker

    try:
        while True:
            event = assemble_event()
            print("-------------------------------------------")
            print(f"Generated event: {event.model_dump_json()}")  # Log the event for debugging
            print("-------------------------------------------")
            send_event_to_pulsar(event, client)
            # sleep(1 / rate_per_sec)
            sleep(15)

    except KeyboardInterrupt:
        print("🛑 Stopping...")
    finally:
        client.close()


#TODO: Burst mode for testing - send x number of events in a short time then stop