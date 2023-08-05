import unittest

from securenative.config.securenative_options import SecureNativeOptions
from securenative.enums.failover_strategy import FailOverStrategy
from securenative.exceptions.securenative_config_exception import SecureNativeConfigException
from securenative.exceptions.securenative_sdk_Illegal_state_exception import SecureNativeSDKIllegalStateException
from securenative.exceptions.securenative_sdk_exception import SecureNativeSDKException
from securenative.securenative import SecureNative


class SecureNativeTest(unittest.TestCase):

    def test_get_sdk_instance_without_init_throws(self):
        with self.assertRaises(SecureNativeSDKIllegalStateException):
            SecureNative.get_instance()

    def test_init_sdk_without_api_key_should_throw(self):
        with self.assertRaises(SecureNativeSDKException):
            SecureNative.init_with_options(SecureNativeOptions())

    def test_init_sdk_with_empty_api_key_should_throw(self):
        with self.assertRaises(SecureNativeConfigException):
            SecureNativeSDKException, SecureNative.init_with_api_key("")

    def test_init_sdk_with_api_key_and_defaults(self):
        SecureNative._flush()
        api_key = "API_KEY"
        securenative = SecureNative.init_with_api_key(api_key)
        options = securenative.get_options()

        self.assertEqual(options.api_key, api_key)
        self.assertEqual(options.api_url, "https://api.securenative.com/collector/api/v1")
        self.assertEqual(options.interval, 1000)
        self.assertEqual(options.timeout, 1500)
        self.assertEqual(options.max_events, 1000)
        self.assertEqual(options.auto_send, True)
        self.assertEqual(options.disable, False)
        self.assertEqual(options.log_level, "CRITICAL")
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_OPEN.value)

    def test_init_sdk_twice_will_throw(self):
        with self.assertRaises(SecureNativeSDKException):
            SecureNative.init_with_api_key("API_KEY")
            SecureNative.init_with_api_key("API_KEY")

    def test_init_sdk_with_api_key_and_get_instance(self):
        SecureNative._flush()
        api_key = "API_KEY"
        securenative = SecureNative.init_with_api_key(api_key)

        self.assertEqual(securenative, SecureNative.get_instance())

    def test_init_sdk_with_options(self):
        SecureNative._flush()
        options = SecureNativeOptions(api_key="API_KEY", log_level="ERROR", max_events=10,
                                      api_url="https://api.securenative-stg.com/collector/api/v1")
        securenative = SecureNative.init_with_options(options)

        options = securenative.get_options()
        self.assertEqual(options.api_key, "API_KEY")
        self.assertEqual(options.max_events, 10)
        self.assertEqual(options.log_level, "ERROR")
