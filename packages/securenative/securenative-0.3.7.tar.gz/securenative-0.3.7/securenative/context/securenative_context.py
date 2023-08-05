from securenative.utils.request_utils import RequestUtils
from securenative.utils.utils import Utils


class SecureNativeContext(object):

    def __init__(self, client_token=None, ip=None, remote_ip=None, headers=None, url=None, method=None, body=None):
        self.client_token = client_token
        self.ip = ip
        self.remote_ip = remote_ip
        self.headers = headers
        self.url = url
        self.method = method
        self.body = body

    @staticmethod
    def from_http_request(request, options):
        try:
            client_token = request.cookies[RequestUtils.SECURENATIVE_COOKIE]
        except Exception:
            client_token = None

        try:
            headers = RequestUtils.get_headers_from_request(request.headers, options)
        except Exception:
            headers = None

        if Utils.is_null_or_empty(client_token):
            client_token = RequestUtils.get_secure_header_from_request(headers)

        return SecureNativeContext(client_token, RequestUtils.get_client_ip_from_request(request, options),
                                   RequestUtils.get_remote_ip_from_request(request), headers, request.url,
                                   request.method, None)
