import pulsar
import json
from uuid import uuid4

# This script sends a test event to a Pulsar topic using the Pulsar Python client.
# this assumes you have a Pulsar broker running locally on port 6650.
# /bin/pulsar standalone starts the pulsar server locally.

client = pulsar.Client("pulsar://localhost:6650")
producer = client.create_producer("persistent://public/default/test-topic")

test_payload = {
    "event_id": str(uuid4()),
    "message": "hello from Addy's laptop!"
}

producer.send(json.dumps(test_payload).encode("utf-8"))
producer.send(json.dumps({"msg": "test from Addy again"}).encode("utf-8"))
print("Event sent!")

client.close()