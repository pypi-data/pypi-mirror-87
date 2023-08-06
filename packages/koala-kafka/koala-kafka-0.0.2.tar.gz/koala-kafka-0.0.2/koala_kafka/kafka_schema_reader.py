import json
import os

import requests
import logging
import sys
from typing import Sequence

from koala_kafka.exceptions.exceptions import EnvironmentVariableNotSet
from koala_kafka.exceptions.exceptions import SchemaRegistryError


class KafkaSchemaReader:

    def __init__(self, schema_registry: str = None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        if not schema_registry:
            self._schema_registry_address = self._get_schema_registry_address()
        else:
            self._schema_registry_address = schema_registry

    def read(self) -> tuple:
        topics = []
        topic_fields = []
        for topic_name in self._topic_names():
            topics.append({"topic_name": topic_name})
            try:
                topic_fields += self._read_topics(topic_name)
            except TypeError:
                # No fields in topic
                pass

        self._logger.info(f"Gathered metadata on {len(topics)} kafka topics and {len(topic_fields)} topic fields "
                          f"from {self._schema_registry_address}")
        return topics, topic_fields

    def _topic_names(self):
        try:
            all_topics = requests.get(f"{self._schema_registry_address}/subjects").json()
        except requests.exceptions.HTTPError as err:
            self._logger.error("Error reading kafka topic names from schema registry")
            raise SchemaRegistryError(err)
        else:
            return self._open_topics(all_topics)

    @staticmethod
    def _open_topics(all_topics: Sequence) -> Sequence:
        return [topic for topic in all_topics if topic.startswith("aapen") and topic.endswith("value")]

    def _read_topics(self, topic_name):
        topic_fields = self._read_schema(topic_name)["fields"]
        return [self._prepare_topic_field_object(topic_field, topic_name) for topic_field in topic_fields]

    def _read_schema(self, topic):
        schema_version = self._last_schema_version(topic)
        return self._last_schema(topic, schema_version)

    def _last_schema_version(self, topic):
        try:
            versions = requests.get(f"{self._schema_registry_address}/subjects/{topic}/versions").json()
        except requests.exceptions.HTTPError as err:
            self._logger.error("Error reading last schema version number of kafka topic from schema registry")
            raise SchemaRegistryError(err)
        else:
            return max(versions)

    def _last_schema(self, topic, schema_version):
        try:
            schema = requests.get(f"{self._schema_registry_address}/subjects/"
                                  f"{topic}/versions/{schema_version}").json()
        except requests.exceptions.HTTPError as err:
            self._logger.error("Error reading schema for kafka topic from schema registry")
            raise SchemaRegistryError(err)
        else:
            return json.loads(schema["schema"])

    @staticmethod
    def _prepare_topic_field_object(topic_field, topic_name):
        try:
            topic_field["field_name"] = topic_field.pop("name")
        except KeyError as missing_key:
            raise SchemaRegistryError(f"Invalid kafka topic field, field {missing_key} missing")
        else:
            return dict(topic_name=topic_name, **topic_field)

    @staticmethod
    def _get_schema_registry_address():
        try:
            address = os.environ["SCHEMA_REGISTRY"]
        except KeyError as missing_env:
            raise EnvironmentVariableNotSet(f"{missing_env}")
        else:
            return address
