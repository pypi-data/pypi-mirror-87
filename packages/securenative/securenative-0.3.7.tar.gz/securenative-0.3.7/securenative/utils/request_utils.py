import re

from securenative.utils.ip_utils import IpUtils


class RequestUtils(object):
    SECURENATIVE_COOKIE = "_sn"
    SECURENATIVE_HEADER = "x-securenative"
    IP_HEADERS = ["HTTP_X_FORWARDED_FOR", "X_FORWARDED_FOR", "REMOTE_ADDR", "x-forwarded-for", "x-client-ip", "x-real-ip", "x-forwarded", "x-cluster-client-ip", "forwarded-for", "forwarded", "via"]
    PII_HEADERS = ['authorization', 'access_token', 'apikey', 'password',  'passwd', 'secret', 'api_key']

    @staticmethod
    def get_secure_header_from_request(headers):
        try:
            return headers[RequestUtils.SECURENATIVE_HEADER]
        except Exception:
            return ""

    @staticmethod
    def get_client_ip_from_request(request, options):
        if options and options.proxy_headers and len(options.proxy_headers) > 0:
            for header in options.proxy_headers:
                try:
                    if request.environ.get(header) is not None:
                        ips = request.environ.get(header).split(',')
                        return RequestUtils.get_valid_ip(ips)
                    if request.headers[header] is not None:
                        ips = request.headers[header].split(',')
                        return RequestUtils.get_valid_ip(ips)
                except Exception:
                    try:
                        if request.headers[header] is not None:
                            ips = request.headers[header].split(',')
                            return RequestUtils.get_valid_ip(ips)
                    except Exception:
                        continue

        for header in RequestUtils.IP_HEADERS:
            try:
                ips = request.headers.get(header).split(',')
                return RequestUtils.get_valid_ip(ips)
            except Exception:
                continue

        for header in RequestUtils.IP_HEADERS:
            try:
                ips = request.META.get(header).split(',')
                return RequestUtils.get_valid_ip(ips)
            except Exception:
                continue

        return ""

    @staticmethod
    def get_remote_ip_from_request(request):
        try:
            if len(request.raw._original_response.fp.raw._sock.getpeername()) > 0:
                return request.raw._original_response.fp.raw._sock.getpeername()[0]
        except Exception:
            return ""

    @staticmethod
    def get_valid_ip(ips):
        if isinstance(ips, list):
            for ip in ips:
                ip = ip.strip()
                if IpUtils.is_valid_public_ip(ip):
                    return ip

            # No public ip found check for no loopback
            for ip in ips:
                ip = ip.strip()
                if not IpUtils.is_loop_back(ip):
                    return ip

        ip = ips.strip()
        if IpUtils.is_valid_public_ip(ip):
            return ip

        if IpUtils.is_loop_back(ip):
            return ip

    @staticmethod
    def get_headers_from_request(headers, options=None):
        h = {}
        if options and options.pii_headers and len(options.pii_headers) > 0:
            for header in headers:
                if header.lower() not in options.pii_headers and header.upper() not in options.pii_headers:
                    h[header] = headers[header]
        elif options and options.pii_regex_pattern:
            for header in headers:
                if not re.search(options.pii_regex_pattern, header):
                    h[header] = headers[header]
        else:
            for header in headers:
                if header.lower() not in RequestUtils.PII_HEADERS and header.upper() not in RequestUtils.PII_HEADERS:
                    h[header] = headers[header]

        return h
