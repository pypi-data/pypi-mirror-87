class RequestOptions(object):

    def __init__(self, url, body, retry):
        self.url = url
        self.body = body
        self.retry = retry
