from securenative.enums.failover_strategy import FailOverStrategy


class SecureNativeOptions(object):

    def __init__(self, api_key=None, api_url="https://api.securenative.com/collector/api/v1", interval=1000,
                 max_events=1000, timeout=1500, auto_send=True, disable=False, log_level="CRITICAL",
                 fail_over_strategy=FailOverStrategy.FAIL_OPEN.value, proxy_headers=None,
                 pii_headers=None, pii_regex_pattern=None):

        if proxy_headers is None:
            proxy_headers = []
        if fail_over_strategy != FailOverStrategy.FAIL_OPEN.value and \
                fail_over_strategy != FailOverStrategy.FAIL_CLOSED.value:
            self.fail_over_strategy = FailOverStrategy.FAIL_OPEN.value
        else:
            self.fail_over_strategy = fail_over_strategy

        self.api_key = api_key
        self.api_url = api_url
        self.interval = interval
        self.max_events = max_events
        self.timeout = timeout
        self.auto_send = auto_send
        self.disable = disable
        self.log_level = log_level
        self.proxy_headers = proxy_headers
        self.pii_headers = pii_headers
        self.pii_regex_pattern = pii_regex_pattern
