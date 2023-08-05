import unittest
from datetime import datetime

from securenative.utils.date_utils import DateUtils


class DateUtilTest(unittest.TestCase):

    def test_to_timestamp(self):
        iso_8601_date = "2020-05-20T15:07:13Z"
        result = DateUtils.to_timestamp(iso_8601_date)

        self.assertEqual(datetime.strptime(iso_8601_date, '%Y-%m-%dT%H:%M:%S.%f'[:-3] + 'Z'), result)

