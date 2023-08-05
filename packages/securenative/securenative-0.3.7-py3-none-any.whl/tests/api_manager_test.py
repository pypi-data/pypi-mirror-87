import json
import unittest
import responses

from securenative.api_manager import ApiManager
from securenative.config.securenative_options import SecureNativeOptions
from securenative.context.securenative_context import SecureNativeContext
from securenative.enums.event_types import EventTypes
from securenative.enums.risk_level import RiskLevel
from securenative.event_manager import EventManager
from securenative.models.event_options import EventOptions
from securenative.models.user_traits import UserTraits
from securenative.models.verify_result import VerifyResult


class ApiManagerTest(unittest.TestCase):

    def setUp(self):
        self.context = SecureNativeContext(ip="127.0.0.1", headers={
            "user-agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"})

        self.event_options = EventOptions(EventTypes.LOG_IN, "USER_ID",
                                          UserTraits("USER_NAME", "USER_EMAIL", "+12012673412"), context=self.context,
                                          properties={"prop1": "CUSTOM_PARAM_VALUE",
                                                      "prop2": True,
                                                      "prop3": 3})

    @responses.activate
    def test_track_event(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY", auto_send=True, interval=10,
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        expected = "{\"eventType\":\"sn.user.login\",\"userId\":\"USER_ID\",\"userTraits\":{" \
                   "\"name\":\"USER_NAME\",\"email\":\"USER_EMAIL\",\"createdAt\":null},\"request\":{" \
                   "\"cid\":null,\"vid\":null,\"fp\":null,\"ip\":\"127.0.0.1\",\"remoteIp\":null,\"headers\":{" \
                   "\"user-agent\":\"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) " \
                   "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405\"},\"url\":null,\"method\":null}," \
                   "\"properties\":{\"prop2\":true,\"prop1\":\"CUSTOM_PARAM_VALUE\",\"prop3\":3}}"

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/track",
                      json=json.loads(expected), status=200)
        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            api_manager.track(self.event_options)
        finally:
            event_manager.stop_event_persist()

    @responses.activate
    def test_should_timeout_on_post(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY", auto_send=True, timeout=0.000001,
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/verify",
                      json={"event": "SOME_EVENT_NAME"}, status=408)

        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        verify_result = VerifyResult(RiskLevel.LOW.value, 0, [])
        res = api_manager.verify(self.event_options)

        self.assertEqual(res.risk_level, verify_result.risk_level)
        self.assertEqual(res.score, verify_result.score)
        self.assertEqual(res.triggers, verify_result.triggers)

    @responses.activate
    def test_verify_event(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY",
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/verify",
                      json={
                          "riskLevel": "low",
                          "score": 0,
                          "triggers": None
                      }, status=200)
        verify_result = VerifyResult(RiskLevel.LOW, 0, None)

        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        result = api_manager.verify(self.event_options)

        self.assertIsNotNone(result)
        self.assertEqual(result.risk_level, verify_result.risk_level.value)
        self.assertEqual(result.score, verify_result.score)
        self.assertEqual(result.triggers, verify_result.triggers)


if __name__ == '__main__':
    unittest.main()
