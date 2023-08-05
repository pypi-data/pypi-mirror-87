import uuid

from securenative.context.securenative_context import SecureNativeContext
from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException
from securenative.models.request_context import RequestContext
from securenative.models.user_traits import UserTraits
from securenative.utils.date_utils import DateUtils
from securenative.utils.encryption_utils import EncryptionUtils


class SDKEvent(object):

    def __init__(self, event_options, securenative_options):
        if event_options.user_id is None or len(event_options.user_id) <= 0 or event_options.user_id == "":
            raise SecureNativeInvalidOptionsException("Invalid event structure; User Id is missing")

        if event_options.event is None or len(event_options.event.value) <= 0 or event_options.event.value == "":
            raise SecureNativeInvalidOptionsException("Invalid event structure; Event Type is missing")

        if event_options.context is not None:
            self.context = event_options.context
        else:
            self.context = SecureNativeContext()

        if self.context.client_token:
            client_token = EncryptionUtils.decrypt(self.context.client_token, securenative_options.api_key)
        else:
            client_token = None

        if event_options.user_traits and isinstance(event_options.user_traits, dict):
            user_traits = UserTraits(event_options.user_traits.get("name", ""),
                                     event_options.user_traits.get("email", ""),
                                     event_options.user_traits.get("phone", ""),
                                     event_options.user_traits.get("created_at", ""))
        elif event_options.user_traits:
            user_traits = event_options.user_traits
        else:
            user_traits = UserTraits()

        self.rid = str(uuid.uuid4())
        self.event_type = event_options.event if event_options.event else ""
        self.user_id = event_options.user_id
        self.user_traits = user_traits
        self.request = RequestContext(cid=client_token.cid if client_token else "",
                                      vid=client_token.vid if client_token else "",
                                      fp=client_token.fp if client_token else "",
                                      ip=self.context.ip if self.context.ip else "",
                                      remote_ip=self.context.remote_ip if self.context.remote_ip else "",
                                      headers=self.context.headers if self.context.headers else None,
                                      url=self.context.url if self.context.url else "",
                                      method=self.context.method if self.context.method else "")

        self.timestamp = DateUtils.to_timestamp(event_options.timestamp)
        self.properties = event_options.properties
