import unittest

import requests_mock

from securenative.config.securenative_options import SecureNativeOptions
from securenative.utils.request_utils import RequestUtils


class RequestUtilsTest(unittest.TestCase):

    def test_proxy_headers_extraction_from_request_ipv4(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "203.0.113.1"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("203.0.113.1", client_ip)

    def test_proxy_headers_extraction_from_request_ipv6(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "6559:6335:f572:14c6:4198:dd09:ddea:04f4"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("6559:6335:f572:14c6:4198:dd09:ddea:04f4", client_ip)

    def test_proxy_headers_extraction_from_request_multiple_ips(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_HTTP_X_FORWARDED_FOR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "HTTP_X_FORWARDED_FOR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_HTTP_X_FORWARDED_FOR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "HTTP_X_FORWARDED_FOR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_X_FORWARDED_FOR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "X_FORWARDED_FOR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_X_FORWARDED_FOR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "X_FORWARDED_FOR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_REMOTE_ADDR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "REMOTE_ADDR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_REMOTE_ADDR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "REMOTE_ADDR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_for_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_client_ip_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_client_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_real_ip_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_real_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_cluster_client_ip_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-cluster-client-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_cluster_client_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded-for": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_for_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded-for": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_via_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "via": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_via_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "via": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_priority_with_x_forwarded_for(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "203.0.113.1",
                "x-real-ip": "198.51.100.101",
                "x-client-ip": "198.51.100.102"
            }

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("203.0.113.1", client_ip)

    def test_extraction_priority_without_x_forwarded_for(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "198.51.100.101",
                "x-client-ip": "203.0.113.1, 141.246.115.116, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("203.0.113.1", client_ip)

    def test_strip_down_pii_data_from_headers(self):
        headers = {
            'Host': 'net.example.com',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'authorization': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'access_token': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'apikey': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'password': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'passwd': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'secret': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'api_key': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z'
        }

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = headers

        h = RequestUtils.get_headers_from_request(request.headers)

        self.assertEqual(h.get('authorization'), None)
        self.assertEqual(h.get('access_token'), None)
        self.assertEqual(h.get('apikey'), None)
        self.assertEqual(h.get('password'), None)
        self.assertEqual(h.get('passwd'), None)
        self.assertEqual(h.get('secret'), None)
        self.assertEqual(h.get('api_key'), None)

    def test_strip_down_pii_data_from_custom_headers(self):
        headers = {
            'Host': 'net.example.com',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'authorization': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'access_token': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'apikey': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'password': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'passwd': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'secret': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'api_key': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z'
        }

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = headers

        options = SecureNativeOptions(pii_headers=['authorization', 'access_token', 'apikey', 'password',
                                                   'passwd', 'secret', 'api_key'])
        h = RequestUtils.get_headers_from_request(request.headers, options)

        self.assertEqual(h.get('authorization'), None)
        self.assertEqual(h.get('access_token'), None)
        self.assertEqual(h.get('apikey'), None)
        self.assertEqual(h.get('password'), None)
        self.assertEqual(h.get('passwd'), None)
        self.assertEqual(h.get('secret'), None)
        self.assertEqual(h.get('api_key'), None)

    def test_strip_down_pii_data_from_regex_pattern(self):
        headers = {
            'Host': 'net.example.com',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'http_auth_authorization': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_access_token': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_apikey': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_password': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_passwd': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_secret': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z',
            'http_auth_api_key': 'ylSkZIjbdWybfs4fUQe9BqP0LH5Z'
        }

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = headers

        options = SecureNativeOptions(pii_regex_pattern='((?i)(http_auth_)(\w+)?)')
        h = RequestUtils.get_headers_from_request(request.headers, options)

        self.assertEqual(h.get('http_auth_authorization'), None)
        self.assertEqual(h.get('http_auth_access_token'), None)
        self.assertEqual(h.get('http_auth_apikey'), None)
        self.assertEqual(h.get('http_auth_password'), None)
        self.assertEqual(h.get('http_auth_passwd'), None)
        self.assertEqual(h.get('http_auth_secret'), None)
        self.assertEqual(h.get('http_auth_api_key'), None)
