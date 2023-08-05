import unittest

import requests_mock

from securenative.context.securenative_context import SecureNativeContext


class ContextBuilderTest(unittest.TestCase):

    def test_create_context_from_request(self):
        with requests_mock.Mocker(real_http=True) as request:
            request.server_name = "www.securenative.com"
            request.request_uri = "/login"
            request.query_string = "param1=value1&param2=value2"
            request.method = "Post"
            request.url = "www.securenative.com"
            request.request_uri = "/login/param1=value1&param2=value2"
            request.META = {
                "REMOTE_ADDR": "51.68.201.122"
            }
            request.headers = {
                "x-securenative": "71532c1fad2c7f56118f7969e401f3cf080239140d208e7934e6a530818c37e544a0c2330a487bcc6fe4f662a57f265a3ed9f37871e80529128a5e4f2ca02db0fb975ded401398f698f19bb0cafd68a239c6caff99f6f105286ab695eaf3477365bdef524f5d70d9be1d1d474506b433aed05d7ed9a435eeca357de57817b37c638b6bb417ffb101eaf856987615a77a"}

            context = SecureNativeContext.from_http_request(request, None)

            self.assertEqual(context.client_token,
                             "71532c1fad2c7f56118f7969e401f3cf080239140d208e7934e6a530818c37e544a0c2330a487bcc6fe4f662a57f265a3ed9f37871e80529128a5e4f2ca02db0fb975ded401398f698f19bb0cafd68a239c6caff99f6f105286ab695eaf3477365bdef524f5d70d9be1d1d474506b433aed05d7ed9a435eeca357de57817b37c638b6bb417ffb101eaf856987615a77a")
            self.assertEqual(context.ip, "51.68.201.122")
            self.assertEqual(context.method, "Post")
            self.assertEqual(context.url, "www.securenative.com")
            self.assertEqual(context.remote_ip, "")
            self.assertEqual(context.headers, {
                "x-securenative": "71532c1fad2c7f56118f7969e401f3cf080239140d208e7934e6a530818c37e544a0c2330a487bcc6fe4f662a57f265a3ed9f37871e80529128a5e4f2ca02db0fb975ded401398f698f19bb0cafd68a239c6caff99f6f105286ab695eaf3477365bdef524f5d70d9be1d1d474506b433aed05d7ed9a435eeca357de57817b37c638b6bb417ffb101eaf856987615a77a"})
            self.assertIsNone(context.body)

    def test_create_context_from_request_with_cookie(self):
        with requests_mock.Mocker(real_http=True) as request:
            request.server_name = "www.securenative.com"
            request.request_uri = "/login"
            request.query_string = "param1=value1&param2=value2"
            request.method = "Post"
            request.url = "www.securenative.com"
            request.request_uri = "/login/param1=value1&param2=value2"
            request.META = {
                "REMOTE_ADDR": "51.68.201.122"
            }
            request.cookies = {"_sn":
                                   "71532c1fad2c7f56118f7969e401f3cf080239140d208e7934e6a530818c37e544a0c2330a487bcc6fe4f662a57f265a3ed9f37871e80529128a5e4f2ca02db0fb975ded401398f698f19bb0cafd68a239c6caff99f6f105286ab695eaf3477365bdef524f5d70d9be1d1d474506b433aed05d7ed9a435eeca357de57817b37c638b6bb417ffb101eaf856987615a77a"}

            context = SecureNativeContext.from_http_request(request, None)

            self.assertEqual(context.client_token,
                             "71532c1fad2c7f56118f7969e401f3cf080239140d208e7934e6a530818c37e544a0c2330a487bcc6fe4f662a57f265a3ed9f37871e80529128a5e4f2ca02db0fb975ded401398f698f19bb0cafd68a239c6caff99f6f105286ab695eaf3477365bdef524f5d70d9be1d1d474506b433aed05d7ed9a435eeca357de57817b37c638b6bb417ffb101eaf856987615a77a")
            self.assertEqual(context.ip, "51.68.201.122")
            self.assertEqual(context.method, "Post")
            self.assertEqual(context.url, "www.securenative.com")
            self.assertEqual(context.remote_ip, "")
            self.assertIsNone(context.body)

    def test_create_default_context_builder(self):
        context = SecureNativeContext()

        self.assertIsNone(context.client_token)
        self.assertIsNone(context.ip)
        self.assertIsNone(context.method)
        self.assertIsNone(context.url)
        self.assertIsNone(context.remote_ip)
        self.assertIsNone(context.headers)
        self.assertIsNone(context.body)

    def test_create_custom_context_with_context_builder(self):
        context = SecureNativeContext("SECRET_TOKEN", "10.0.0.0", "10.0.0.1", {"header1": "value1"}, "/some-url", "Get",
                                      "{ \"name\": \"YOUR_NAME\" }")

        self.assertEqual(context.url, "/some-url")
        self.assertEqual(context.client_token, "SECRET_TOKEN")
        self.assertEqual(context.ip, "10.0.0.0")
        self.assertEqual(context.body, "{ \"name\": \"YOUR_NAME\" }")
        self.assertEqual(context.method, "Get")
        self.assertEqual(context.remote_ip, "10.0.0.1")
        self.assertEqual(context.headers, {"header1": "value1"})
