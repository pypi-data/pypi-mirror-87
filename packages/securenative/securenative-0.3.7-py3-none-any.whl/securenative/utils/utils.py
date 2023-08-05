class Utils(object):

    @staticmethod
    def is_null_or_empty(string):
        if not string or len(string) == 0:
            return True
        return False
