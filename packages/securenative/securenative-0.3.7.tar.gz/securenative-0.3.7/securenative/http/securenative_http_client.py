import requests
from requests import Timeout

from securenative.utils.version_utils import VersionUtils


class SecureNativeHttpClient(object):
    AUTHORIZATION_HEADER = "Authorization"
    VERSION_HEADER = "SN-Version"
    USER_AGENT_HEADER = "User-Agent"
    USER_AGENT_HEADER_VALUE = "SecureNative-python"
    CONTENT_TYPE_HEADER = "Content-Type"
    CONTENT_TYPE_HEADER_VALUE = "application/json"

    def __init__(self, securenative_options):
        self.options = securenative_options

    def _headers(self):
        return {
            self.CONTENT_TYPE_HEADER: self.CONTENT_TYPE_HEADER_VALUE,
            self.USER_AGENT_HEADER: self.USER_AGENT_HEADER_VALUE,
            self.VERSION_HEADER: VersionUtils.get_version(),
            self.AUTHORIZATION_HEADER: self.options.api_key
        }

    def post(self, path, body):
        url = "{}/{}".format(self.options.api_url, path)
        try:
            res = requests.post(url=url, data=body, headers=self._headers(), timeout=self.options.timeout / 1000)
            return res
        except Timeout:
            return None
