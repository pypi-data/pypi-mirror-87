import json

from securenative.enums.api_route import ApiRoute
from securenative.enums.failover_strategy import FailOverStrategy
from securenative.enums.risk_level import RiskLevel
from securenative.logger import Logger
from securenative.models.sdk_event import SDKEvent
from securenative.models.verify_result import VerifyResult


class ApiManager(object):

    def __init__(self, event_manager, securenative_options):
        self.event_manager = event_manager
        self.options = securenative_options

    def track(self, event_options):
        Logger.debug("Track event call")
        event = SDKEvent(event_options, self.options)
        return self.event_manager.send_async(event, ApiRoute.TRACK.value)

    def verify(self, event_options):
        Logger.debug("Verify event call")
        event = SDKEvent(event_options, self.options)
        try:
            res = json.loads(self.event_manager.send_sync(event, ApiRoute.VERIFY.value).text)
            return VerifyResult(res["riskLevel"], res["score"], res["triggers"])
        except Exception as e:
            Logger.debug("Failed to call verify; {}".format(e))
            if self.options.fail_over_strategy is FailOverStrategy.FAIL_OPEN.value:
                return VerifyResult(RiskLevel.LOW.value, 0, [])
            return VerifyResult(RiskLevel.HIGH.value, 1, [])
