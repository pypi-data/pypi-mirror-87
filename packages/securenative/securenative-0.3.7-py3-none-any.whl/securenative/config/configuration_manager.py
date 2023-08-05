import os
from configparser import ConfigParser

from securenative.config.securenative_options import SecureNativeOptions
from securenative.logger import Logger


class ConfigurationManager(object):
    DEFAULT_CONFIG_FILE = "securenative.ini"
    CUSTOM_CONFIG_FILE_ENV_NAME = "SECURENATIVE_CONFIG_FILE"
    config = ConfigParser()

    @classmethod
    def read_resource_file(cls, resource_path):
        try:
            cls.config.read(resource_path)
        except Exception as e:
            Logger.debug("Invalid config file; {}, using default options".format(e))

        properties = {}
        for key, value in cls.config.defaults().items():
            properties[key.upper()] = value

        return properties

    @classmethod
    def _get_resource_path(cls, env_name):
        env_value = os.environ.get(env_name)

        if env_value:
            return env_value

        return os.environ.get(cls.DEFAULT_CONFIG_FILE)

    @classmethod
    def _get_env_or_default(cls, properties, key, default):
        if os.environ.get(key):
            if "," in os.environ.get(key):
                return os.environ.get(key).split(",")
            return os.environ.get(key)
        if properties.get(key):
            if "," in properties.get(key):
                return properties.get(key).split(",")
            return properties.get(key)
        return default

    @classmethod
    def load_config(cls, resource_path):
        options = SecureNativeOptions()

        if not resource_path:
            resource_path = os.environ.get(cls.CUSTOM_CONFIG_FILE_ENV_NAME)

        properties = cls.read_resource_file(resource_path)

        return SecureNativeOptions(api_key=cls._get_env_or_default(properties, "SECURENATIVE_API_KEY", options.api_key),
                                   api_url=cls._get_env_or_default(properties, "SECURENATIVE_API_URL", options.api_url),
                                   interval=cls._get_env_or_default(properties, "SECURENATIVE_INTERVAL",
                                                                    options.interval),
                                   max_events=cls._get_env_or_default(properties, "SECURENATIVE_MAX_EVENTS",
                                                                      options.max_events),
                                   timeout=cls._get_env_or_default(properties, "SECURENATIVE_TIMEOUT", options.timeout),
                                   auto_send=cls._get_env_or_default(properties, "SECURENATIVE_AUTO_SEND",
                                                                     options.auto_send),
                                   disable=cls._get_env_or_default(properties, "SECURENATIVE_DISABLE", options.disable),
                                   log_level=cls._get_env_or_default(properties, "SECURENATIVE_LOG_LEVEL",
                                                                     options.log_level),
                                   fail_over_strategy=cls._get_env_or_default(properties,
                                                                              "SECURENATIVE_FAILOVER_STRATEGY",
                                                                              options.fail_over_strategy),
                                   proxy_headers=cls._get_env_or_default(properties, "SECURENATIVE_PROXY_HEADERS",
                                                                         options.proxy_headers),
                                   pii_headers=cls._get_env_or_default(properties, "SECURENATIVE_PII_HEADERS",
                                                                       options.pii_headers),
                                   pii_regex_pattern=cls._get_env_or_default(properties,
                                                                             "SECURENATIVE_PII_REGEX_PATTERN",
                                                                             options.pii_regex_pattern))
