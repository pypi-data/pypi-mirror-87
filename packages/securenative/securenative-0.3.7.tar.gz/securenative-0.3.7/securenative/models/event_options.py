from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException


class EventOptions(object):
    MAX_PROPERTIES_SIZE = 10

    def __init__(self, event, user_id, user_traits=None,
                 context=None, properties=None, timestamp=None):
        if properties is not None and len(properties) > self.MAX_PROPERTIES_SIZE:
            raise SecureNativeInvalidOptionsException(
                "You can have only up to {} custom properties", self.MAX_PROPERTIES_SIZE)

        self.event = event
        self.user_id = user_id
        self.user_traits = user_traits
        self.context = context
        self.properties = properties
        self.timestamp = timestamp
