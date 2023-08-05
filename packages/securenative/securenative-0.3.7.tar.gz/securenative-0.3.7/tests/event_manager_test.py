import json
import unittest
from datetime import datetime

import responses

from securenative.config.securenative_options import SecureNativeOptions
from securenative.event_manager import EventManager
from securenative.models.request_context import RequestContext
from securenative.models.user_traits import UserTraits


class SampleEvent(object):

    def __init__(self):
        self.event_type = "custom-event"
        self.timestamp = datetime.now().strftime("%Y-%d-%dT%H:%M:%S.%fZ")
        self.rid = "432532"
        self.user_id = "1"
        self.user_traits = UserTraits("some user", "email@securenative.com", "+12012673412")
        self.request = RequestContext()
        self.properties = []


class EventManagerTest(unittest.TestCase):

    def setUp(self):
        self.event = SampleEvent()

    @responses.activate
    def test_should_successfully_send_sync_event_with_status_code_200(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY",
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        res_body = "{\"data\": true}"
        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/some-path/to-api",
                      json=json.loads(res_body), status=200)
        event_manager = EventManager(options)

        data = event_manager.send_sync(self.event, "some-path/to-api")
        self.assertEqual(res_body, data.text)

    @responses.activate
    def test_should_send_sync_event_and_fail_when_status_code_401(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY",
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/some-path/to-api",
                      json={}, status=401)
        event_manager = EventManager(options)

        res = event_manager.send_sync(self.event, "some-path/to-api")

        self.assertEqual(res.status_code, 401)

    @responses.activate
    def test_should_send_sync_event_and_fail_when_status_code_500(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY",
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/some-path/to-api",
                      json={}, status=500)
        event_manager = EventManager(options)

        res = event_manager.send_sync(self.event, "some-path/to-api")

        self.assertEqual(res.status_code, 500)
