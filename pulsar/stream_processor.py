"""
Pulsar Event Stream Producer

A basic event producer that generates synthetic e-commerce events and publishes them
to Apache Pulsar topics with tenant-based partitioning. Currently supports continuous
and burst mode event generation for testing and development purposes.

Current Features:
- Multi-tenant event generation with tenant-specific topics
- Configurable event generation rates and burst modes
- Basic Pulsar client connection with retry logic
- JSON serialization with orjson for performance

Future Enhancements:
- 
"""

# Your senior-level implementation here
import pulsar
import orjson
from time import sleep
import os
from pathlib import Path
import json
import time

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

    payload = orjson.dumps(event.model_dump(mode="python"))
    producer.send(payload)

    print(f"------------- Sent event to {topic}") #TODO: make more sophisticated logger wrapper
    producer.close()


def create_pulsar_client_with_retries(retries=10, delay=10):
    
    pulsar_host = os.getenv("PULSAR_HOST", "localhost") # Defaults to localhost if not set. able to run locally or in docker
    print(f"--------------------- pulsar_host: {pulsar_host}")
    
    # Retry logic for Pulsar client connection. Ran into connection issues with Pulsar in Docker, so implemented this
    for attempt in range(retries):
        try:
            client = pulsar.Client(f"pulsar://{pulsar_host}:6650")
            print("✅ Connected to Pulsar!")
            return client
        except Exception as e:
            print(f"⚠️  Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise RuntimeError(f"❌ Could not connect to Pulsar after {retries} attempts.")


def run_event_loop(rate_per_sec: float = 0.1):

    client = create_pulsar_client_with_retries()
    topic_set = set() # Set to store pulsar topics for each event
    merchant_ids = set()  # Set to store unique merchant IDs for the events

    try:
        while True:
            event = assemble_event()
            topic_set.add(f"persistent://public/default/{event.tenant_id}.events")  # Collect unique topics
            merchant_ids.add(event.tenant_id)  # Collect unique tenant IDs
            print("-------------------------------------------")
            print(f"Generated event: {event.model_dump_json()}")  # Log the event for debugging
            print("-------------------------------------------")

            #write to local file for debugging
            file_path = Path(f"/tmp/test_json_payloads/event_{event.tenant_id}.json")
            event_json = event.model_dump_json()
            with file_path.open("w") as f:
                json.dump(event_json, f, indent=4)


            send_event_to_pulsar(event, client)
            sleep(1 / rate_per_sec)

    except KeyboardInterrupt:
        print("🛑 Stopping...")
    finally:
        print(f"Topics used: {', '.join(topic_set)}")
        client.close()
    return topic_set, merchant_ids


def run_burst_mode(burst_size: int = 10, delay_between_events: float = 0.1):
    """
    Sends a burst of events to Pulsar and exits.

    Args:
        burst_size: Number of events to send in the burst.
        delay_between_events: Time (in seconds) between each event.
    """
    client = create_pulsar_client_with_retries()
    topic_set = set() # Set to store pulsar topics for each event
    merchant_ids = set()  # Set to store unique merchant IDs for the events

    try:
        for _ in range(burst_size):
            event = assemble_event()
            topic_set.add(f"persistent://public/default/{event.tenant_id}.events")  # Collect unique topics
            merchant_ids.add(event.tenant_id)  # Collect unique tenant IDs
            print("-------------------------------------------")
            print(f"Generated event: {event.model_dump_json()}")
            print("-------------------------------------------")

            #write to local file for debugging
            file_path = Path(f"/tmp/test_json_payloads/event_{event.tenant_id}.json")
            event_json = event.model_dump_json()
            with file_path.open("w") as f:
                json.dump(event_json, f, indent=4)
            
            # Send the event to Pulsar    
            send_event_to_pulsar(event, client)
            sleep(delay_between_events)
    finally:
        client.close()
        print(f"Burst of {burst_size} events sent.")
        print(f"Topics used: {', '.join(topic_set)}")
    return topic_set, merchant_ids


if __name__ == "__main__":

    ## For continuous event generation
    topic_set, merchant_ids = run_event_loop(rate_per_sec=0.05)  
    
    ## Adjust rate as needed
    # run_event_loop(rate_per_sec=1)  # For testing, send 1 event per second
    # run_event_loop(rate_per_sec=10)  # For testing, send 10 events per second

    ## For burst mode event generation
    # topic_set, merchant_ids = run_burst_mode(burst_size=5, delay_between_events=0.1)
    
    print(merchant_ids)