import copy
import json

SCHEMA_REGISTRY_ADDRESS = "https://schema-registry.com"

TOPIC_NAME1 = "aapen-test-topic1-value"
TOPIC_NAME2 = "aapen-test-topic2-value"
TOPIC_VERSIONS = [1, 2]
LAST_VERSION = max(TOPIC_VERSIONS)

ALL_TOPICS = [
    "aapen-test-topic1-key",
    TOPIC_NAME1,
    "topic2-value",
    TOPIC_NAME2,
]

EXPECTED_OPEN_TOPICS = [
    TOPIC_NAME1,
    TOPIC_NAME2,
]

EXPECTED_TOPIC_OBJECT_OUT_TOPIC1 = {
    "topic_name": TOPIC_NAME1
}

EXPECTED_TOPIC_OBJECT_OUT_TOPIC2 = {
    "topic_name": TOPIC_NAME2
}

INVALID_TOPIC_FIELD_OBJECT_IN = {
    "custom_value": "value"
}

VALID_TOPIC_FIELD_OBJECT_IN_TOPIC1 = {
    "name": "value",
    "custom_value": "value"
}

EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC1 = {
    "topic_name": TOPIC_NAME1,
    "field_name": "value",
    "custom_value": "value"
}

LAST_SCHEMA_TOPIC1 = {
    "type": "record",
    "name": "navn",
    "namespace": "something",
    "fields": [copy.deepcopy(VALID_TOPIC_FIELD_OBJECT_IN_TOPIC1)]
}

LAST_SCHEMA_HTTP_RESPONSE_TOPIC1 = {
    "subject": "aapen-topic-value",
    "version": 1,
    "id": 712,
    "schema": json.dumps(LAST_SCHEMA_TOPIC1)
}

VALID_TOPIC_FIELD_OBJECT_IN_TOPIC2 = {
    "name": "value",
    "custom_value": "value"
}

EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC2 = {
    "topic_name": TOPIC_NAME2,
    "field_name": "value",
    "custom_value": "value"
}

LAST_SCHEMA_TOPIC2 = {
    "type": "record",
    "name": "navn",
    "namespace": "something",
    "fields": [copy.deepcopy(VALID_TOPIC_FIELD_OBJECT_IN_TOPIC2)]
}

LAST_SCHEMA_HTTP_RESPONSE_TOPIC2 = {
    "subject": "aapen-topic-value",
    "version": 1,
    "id": 712,
    "schema": json.dumps(LAST_SCHEMA_TOPIC2)
}
