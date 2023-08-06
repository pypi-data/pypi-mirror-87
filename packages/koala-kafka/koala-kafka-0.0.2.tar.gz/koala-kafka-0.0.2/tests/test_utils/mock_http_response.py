import requests
from tests.test_utils.constants import SCHEMA_REGISTRY_ADDRESS, ALL_TOPICS, TOPIC_VERSIONS, TOPIC_NAME1, LAST_VERSION, \
    TOPIC_NAME2, LAST_SCHEMA_HTTP_RESPONSE_TOPIC1, LAST_SCHEMA_HTTP_RESPONSE_TOPIC2


class MockResponse:
    def __init__(self, response_json, status_code):
        self._response_json = response_json
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

    def json(self):
        return self._response_json

    def raise_for_status(self):
        if self._status_code >= 400:
            raise requests.exceptions.HTTPError(self._status_code)


# Mock method used to replace requests.get
def mock_requests_get(address, **kwargs):
    if address == f"{SCHEMA_REGISTRY_ADDRESS}/subjects":
        return MockResponse(ALL_TOPICS, 200)
    elif address == f"{SCHEMA_REGISTRY_ADDRESS}/subjects/{TOPIC_NAME1}/versions":
        return MockResponse(TOPIC_VERSIONS, 200)
    elif address == f"{SCHEMA_REGISTRY_ADDRESS}/subjects/{TOPIC_NAME2}/versions":
        return MockResponse(TOPIC_VERSIONS, 200)
    elif address == f"{SCHEMA_REGISTRY_ADDRESS}/subjects/{TOPIC_NAME1}/versions/{LAST_VERSION}":
        return MockResponse(LAST_SCHEMA_HTTP_RESPONSE_TOPIC1, 200)
    elif address == f"{SCHEMA_REGISTRY_ADDRESS}/subjects/{TOPIC_NAME2}/versions/{LAST_VERSION}":
        return MockResponse(LAST_SCHEMA_HTTP_RESPONSE_TOPIC2, 200)
    else:
        return MockResponse(None, 404)
