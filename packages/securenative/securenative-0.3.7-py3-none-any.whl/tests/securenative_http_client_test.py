import unittest

import responses

from securenative.config.securenative_options import SecureNativeOptions
from securenative.http.securenative_http_client import SecureNativeHttpClient


class SecureNativeHttpClientTest(unittest.TestCase):

    @responses.activate
    def test_should_make_simple_post_call(self):
        options = SecureNativeOptions(api_key="YOUR_API_KEY", auto_send=True, interval=10,
                                      api_url="https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/track",
                      json={"event": "SOME_EVENT_NAME"}, status=200)
        client = SecureNativeHttpClient(options)
        payload = "{\"event\": \"SOME_EVENT_NAME\"}"

        res = client.post("track", payload)

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, payload)
