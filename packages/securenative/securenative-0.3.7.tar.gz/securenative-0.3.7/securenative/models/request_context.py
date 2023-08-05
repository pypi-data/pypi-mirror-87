class RequestContext(object):

    def __init__(self, cid=None, vid=None, fp=None, ip=None,
                 remote_ip=None, headers=None, url=None, method=None):
        self.cid = cid
        self.vid = vid
        self.fp = fp
        self.ip = ip
        self.remote_ip = remote_ip
        self.headers = headers
        self.url = url
        self.method = method
