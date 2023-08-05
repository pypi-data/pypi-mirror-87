from datetime import datetime


class DateUtils(object):

    @staticmethod
    def to_timestamp(date):
        try:
            if not date or date == "":
                return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f'[:-3] + 'Z')
        except Exception:
            return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
