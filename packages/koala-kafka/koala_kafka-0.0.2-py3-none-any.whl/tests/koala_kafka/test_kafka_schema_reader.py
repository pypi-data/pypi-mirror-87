import os
import unittest
from unittest import mock

from koala_kafka.exceptions.exceptions import SchemaRegistryError, EnvironmentVariableNotSet
from koala_kafka.kafka_schema_reader import KafkaSchemaReader
from tests.test_utils.constants import ALL_TOPICS, EXPECTED_OPEN_TOPICS, TOPIC_NAME1, INVALID_TOPIC_FIELD_OBJECT_IN, \
    SCHEMA_REGISTRY_ADDRESS, LAST_VERSION, EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC1, VALID_TOPIC_FIELD_OBJECT_IN_TOPIC1, \
    LAST_SCHEMA_TOPIC1, EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC2, EXPECTED_TOPIC_OBJECT_OUT_TOPIC1, \
    EXPECTED_TOPIC_OBJECT_OUT_TOPIC2
from tests.test_utils.mock_http_response import mock_requests_get


class TestKafkaSchemaReaderStaticMethods(unittest.TestCase):

    def test__open_topics_valid(self):
        open_topics = KafkaSchemaReader._open_topics(ALL_TOPICS)
        self.assertEqual(open_topics, EXPECTED_OPEN_TOPICS)

    def test__prepare_topic_field_object_valid(self):
        topic_object_out = KafkaSchemaReader._prepare_topic_field_object(VALID_TOPIC_FIELD_OBJECT_IN_TOPIC1, TOPIC_NAME1)
        self.assertEqual(topic_object_out, EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC1)

    def test__prepare_topic_field_object_raises_SchemaRegistryError(self):
        with self.assertRaises(SchemaRegistryError):
            topic_object_out = KafkaSchemaReader._prepare_topic_field_object(INVALID_TOPIC_FIELD_OBJECT_IN, TOPIC_NAME1)

    def test__get_schema_registry_address_valid(self):
        os.environ["SCHEMA_REGISTRY"] = SCHEMA_REGISTRY_ADDRESS
        actual_schema_registry_address = KafkaSchemaReader._get_schema_registry_address()
        self.assertEqual(actual_schema_registry_address, SCHEMA_REGISTRY_ADDRESS)

    def test__get_schema_registry_address_raises_EnvironmentVariableNotSet(self):
        with self.assertRaises(EnvironmentVariableNotSet):
            actual_schema_registry_address = KafkaSchemaReader._get_schema_registry_address()


class TestKafkaSchemaReaderClassInstantiation(unittest.TestCase):

    def setUp(self):
        os.environ["SCHEMA_REGISTRY"] = SCHEMA_REGISTRY_ADDRESS

    def tearDown(self):
        del os.environ["SCHEMA_REGISTRY"]

    def test_KafkaSchemaReader_instantiation_registry_address_from_env(self):
        schema_reader = KafkaSchemaReader()
        self.assertEqual(schema_reader._schema_registry_address, SCHEMA_REGISTRY_ADDRESS)

    def test_KafkaSchemaReader_instantiation_registry_address_from_input_param(self):
        param_specified_schema_registry = "https://param-specified-schema-registry.com"
        schema_reader = KafkaSchemaReader(schema_registry=param_specified_schema_registry)
        self.assertEqual(schema_reader._schema_registry_address, param_specified_schema_registry)


class TestKafkaSchemaReader(unittest.TestCase):

    def setUp(self):
        os.environ["SCHEMA_REGISTRY"] = SCHEMA_REGISTRY_ADDRESS
        self.schema_reader = KafkaSchemaReader()

    def tearDown(self):
        del os.environ["SCHEMA_REGISTRY"]

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test__topic_names_valid(self, mock_get):
        open_topics = self.schema_reader._topic_names()
        self.assertEqual(open_topics, EXPECTED_OPEN_TOPICS)

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test__last_schema_version_valid(self, mock_get):
        last_version = self.schema_reader._last_schema_version(TOPIC_NAME1)
        self.assertEqual(last_version, LAST_VERSION)

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test__last_schema_valid(self, mock_get):
        last_version = self.schema_reader._last_schema(TOPIC_NAME1, LAST_VERSION)
        self.assertEqual(last_version, LAST_SCHEMA_TOPIC1)

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test__read_schema_valid(self, mock_get):
        schema = self.schema_reader._read_schema(TOPIC_NAME1)
        self.assertEqual(schema, LAST_SCHEMA_TOPIC1)

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test__read_topics_valid(self, mock_get):
        topic_fields = self.schema_reader._read_topics(TOPIC_NAME1)
        self.assertEqual(topic_fields, [EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC1])

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_read_valid(self, mock_get):
        topics, topic_fields = self.schema_reader.read()
        self.assertEqual(topics, [EXPECTED_TOPIC_OBJECT_OUT_TOPIC1, EXPECTED_TOPIC_OBJECT_OUT_TOPIC2])
        self.assertEqual(topic_fields, [EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC1, EXPECTED_TOPIC_FIELD_OBJECT_OUT_TOPIC2])
