import configparser
import os
import platform
import unittest

from securenative.config.configuration_manager import ConfigurationManager
from securenative.enums.failover_strategy import FailOverStrategy


class ConfigurationManagerTest(unittest.TestCase):

    def setUp(self):
        self.config_file_path = "/tmp/securenative.ini"

    def clean_settings(self):
        try:
            os.remove(self.config_file_path)
        except FileNotFoundError:
            pass

        try:
            del os.environ["SECURENATIVE_API_KEY"]
            del os.environ["SECURENATIVE_API_URL"]
            del os.environ["SECURENATIVE_INTERVAL"]
            del os.environ["SECURENATIVE_MAX_EVENTS"]
            del os.environ["SECURENATIVE_TIMEOUT"]
            del os.environ["SECURENATIVE_AUTO_SEND"]
            del os.environ["SECURENATIVE_DISABLE"]
            del os.environ["SECURENATIVE_LOG_LEVEL"]
            del os.environ["SECURENATIVE_FAILOVER_STRATEGY"]
            del os.environ["SECURENATIVE_PROXY_HEADERS"]
        except KeyError:
            pass

    def create_ini_file(self, conf):
        os.environ["SECURENATIVE_CONFIG_FILE"] = self.config_file_path

        try:
            os.remove(self.config_file_path)
        except FileNotFoundError:
            pass

        config = configparser.ConfigParser()

        for key, value in conf.items():
            config.set("DEFAULT", key.upper(), value)

        with open(self.config_file_path, "w") as configfile:
            config.write(configfile)

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_parse_config_file_correctly(self):
        self.clean_settings()
        config = {
            "SECURENATIVE_API_KEY": "SOME_API_KEY",
            "SECURENATIVE_APP_NAME": "SOME_APP_NAME",
            "SECURENATIVE_API_URL": "SOME_API_URL",
            "SECURENATIVE_INTERVAL": "1000",
            "SECURENATIVE_HEARTBEAT_INTERVAL": "5000",
            "SECURENATIVE_MAX_EVENTS": "100",
            "SECURENATIVE_TIMEOUT": "1500",
            "SECURENATIVE_AUTO_SEND": "True",
            "SECURENATIVE_DISABLE": "False",
            "SECURENATIVE_LOG_LEVEL": "Critical",
            "SECURENATIVE_FAILOVER_STRATEGY": "fail-closed",
            "SECURENATIVE_PROXY_HEADERS": "CF-Connecting-IP,Some-Random-Ip",
            "SECURENATIVE_PII_HEADERS": "authentication,api_key",
            "SECURENATIVE_PII_REGEX_PATTERN": "/auth/i"
        }

        self.create_ini_file(config)
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)
        self.assertEqual(options.api_key, "SOME_API_KEY")
        self.assertEqual(options.api_url, "SOME_API_URL")
        self.assertEqual(options.auto_send, "True")
        self.assertEqual(options.disable, "False")
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_CLOSED.value)
        self.assertEqual(options.interval, "1000")
        self.assertEqual(options.log_level, "Critical")
        self.assertEqual(options.max_events, "100")
        self.assertEqual(options.timeout, "1500")
        self.assertEqual(options.pii_regex_pattern, "/auth/i")
        self.assertEqual(options.proxy_headers, ["CF-Connecting-IP", "Some-Random-Ip"])
        self.assertEqual(options.pii_headers, ["authentication", "api_key"])

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_ignore_unknown_config_in_properties_file(self):
        self.clean_settings()
        config = {
            "SECURENATIVE_TIMEOUT": "1500",
            "SECURENATIVE_UNKNOWN_KEY": "SOME_UNKNOWN_KEY"
        }

        self.create_ini_file(config)
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)
        self.assertEqual(options.timeout, "1500")

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_handle_invalid_config_file(self):
        self.clean_settings()
        config = {"bla": "bla"}

        self.create_ini_file(config)
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def ignore_invalid_config_file_entries(self):
        self.clean_settings()
        config = {
            "SECURENATIVE_API_KEY": 1,
            "SECURENATIVE_API_URL": 3,
            "SECURENATIVE_TIMEOUT": "bad timeout",
            "SECURENATIVE_FAILOVER_STRATEGY": "fail-what",
        }

        self.create_ini_file(config)
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_OPEN)

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_load_default_config(self):
        self.clean_settings()
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)
        self.assertIsNone(options.api_key)
        self.assertEqual(options.api_url, "https://api.securenative.com/collector/api/v1")
        self.assertEqual(str(options.interval), "1000")
        self.assertEqual(options.timeout, "1500")
        self.assertEqual(str(options.max_events), "1000")
        self.assertEqual(str(options.auto_send), "True")
        self.assertEqual(str(options.disable), "False")
        self.assertEqual(options.log_level, "CRITICAL")
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_OPEN.value)
        self.assertEqual(len(options.proxy_headers), 0)

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_get_config_from_env_variables(self):
        self.clean_settings()

        os.environ["SECURENATIVE_API_KEY"] = "SOME_ENV_API_KEY"
        os.environ["SECURENATIVE_API_URL"] = "SOME_API_URL"
        os.environ["SECURENATIVE_INTERVAL"] = "6000"
        os.environ["SECURENATIVE_MAX_EVENTS"] = "700"
        os.environ["SECURENATIVE_TIMEOUT"] = "1700"
        os.environ["SECURENATIVE_AUTO_SEND"] = "False"
        os.environ["SECURENATIVE_DISABLE"] = "True"
        os.environ["SECURENATIVE_LOG_LEVEL"] = "Debug"
        os.environ["SECURENATIVE_FAILOVER_STRATEGY"] = "fail-closed"
        os.environ["SECURENATIVE_PROXY_HEADERS"] = "CF-Connecting-IP"

        options = ConfigurationManager.load_config(None)

        self.assertEqual(options.api_key, "SOME_ENV_API_KEY")
        self.assertEqual(options.api_url, "SOME_API_URL")
        self.assertEqual(options.interval, "6000")
        self.assertEqual(options.timeout, "1700")
        self.assertEqual(options.max_events, "700")
        self.assertEqual(options.auto_send, "False")
        self.assertEqual(options.disable, "True")
        self.assertEqual(options.log_level, "Debug")
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_CLOSED.value)
        self.assertEqual(options.proxy_headers, "CF-Connecting-IP")

    @unittest.skipIf(platform.system() == "Windows" or platform.system() == "windows", "test not supported on windows")
    def test_default_values_for_invalid_enum_config_props(self):
        self.clean_settings()
        config = {
            "SECURENATIVE_FAILOVER_STRATEGY": "fail-something"
        }

        self.create_ini_file(config)
        options = ConfigurationManager.load_config(None)

        self.assertIsNotNone(options)
        self.assertEqual(options.fail_over_strategy, FailOverStrategy.FAIL_OPEN.value)
