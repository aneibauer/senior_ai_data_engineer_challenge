import pytest
from unittest.mock import MagicMock, patch
import orjson

from scripts.stream_processor import send_event_to_pulsar

class DummyEvent:
    def __init__(self, tenant_id, data):
        self.tenant_id = tenant_id
        self._data = data

    def model_dump(self, mode="python"):
        return self._data

def test_send_event_to_pulsar_serialization():
    # Arrange
    event_data = {"foo": "bar", "num": 123}
    event = DummyEvent(tenant_id="tenant123", data=event_data)
    mock_client = MagicMock()
    mock_producer = MagicMock()
    mock_client.create_producer.return_value = mock_producer

    # Act
    send_event_to_pulsar(event, mock_client)

    # Assert
    # Check that the payload sent is the correct orjson serialization of the dict
    expected_payload = orjson.dumps(event_data) #binary representation
    mock_producer.send.assert_called_once_with(expected_payload)
    mock_producer.close.assert_called_once()