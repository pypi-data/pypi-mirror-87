class VerifyResult(object):

    def __init__(self, risk_level=None, score=None, triggers=None):
        self.risk_level = risk_level
        self.score = score
        self.triggers = triggers
