import unittest

from securenative.config.securenative_options import SecureNativeOptions
from securenative.enums.event_types import EventTypes
from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException
from securenative.models.event_options import EventOptions
from securenative.models.sdk_event import SDKEvent


class SDKEventTest(unittest.TestCase):

    def test_creating_event_without_user_id_throws(self):
        with self.assertRaises(SecureNativeInvalidOptionsException):
            event_options = EventOptions(EventTypes.LOG_IN, None)
            options = SecureNativeOptions()

            SDKEvent(event_options, options)

    def test_creating_event_without_event_type_throws(self):
        with self.assertRaises(SecureNativeInvalidOptionsException):
            event_options = EventOptions(None, "1234")
            options = SecureNativeOptions()

            SDKEvent(event_options, options)
