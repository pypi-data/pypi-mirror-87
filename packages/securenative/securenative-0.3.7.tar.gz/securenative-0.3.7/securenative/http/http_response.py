class HttpResponse(object):

    def __init__(self, ok, status_code, body):
        self.ok = ok
        self.status_code = status_code
        self.body = body
