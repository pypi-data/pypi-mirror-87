import json
import threading
import time

from securenative.config.securenative_options import SecureNativeOptions
from securenative.http.securenative_http_client import SecureNativeHttpClient
from securenative.logger import Logger


class QueueItem:
    def __init__(self, url, body, retry):
        self.url = url
        self.body = body
        self.retry = retry


class EventManager:
    def __init__(self, options=SecureNativeOptions(), http_client=None):
        if options.api_key is None:
            raise ValueError('API key cannot be None, please get your API key from SecureNative console.')

        if not http_client:
            self.http_client = SecureNativeHttpClient(options)
        else:
            self.http_client = http_client

        self.queue = list()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

        self.options = options
        self.send_enabled = False
        self.attempt = 0
        self.coefficients = [1, 1, 2, 3, 5, 8, 13]
        self.thread = None
        self.interval = options.interval

    def send_async(self, event, resource_path):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        item = QueueItem(
            resource_path,
            json.dumps(EventManager.serialize(event)),
            False
        )

        self.queue.append(item)
        if self._is_queue_full():
            self.queue = self.queue[:len(self.queue - 1)]

    def flush(self):
        for item in self.queue:
            self.http_client.post(item.url, item.body)

    def send_sync(self, event, resource_path):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        Logger.debug("Attempting to send event {}".format(event))
        res = self.http_client.post(
            resource_path,
            json.dumps(EventManager.serialize(event))
        )
        if res is None or res.status_code != 200:
            Logger.info("SecureNative failed to call endpoint {} with event {}.".format(resource_path, event))

        return res

    def _is_queue_full(self):
        return len(self.queue) > self.options.max_events

    def run(self):
        while True:
            if len(self.queue) > 0 and self.send_enabled:
                for item in self.queue:
                    try:
                        res = self.http_client.post(item.url, item.body)
                        if res.status_code == 401:
                            item.retry = False
                        elif res.status_code != 200:
                            item.retry = True
                        self.queue.remove(item)

                        Logger.debug("Event successfully sent; {}".format(item.body))
                    except Exception as e:
                        Logger.error("Failed to send event; {}".format(e))
                        if item.retry:
                            if len(self.coefficients) == self.attempt + 1:
                                self.attempt = 0

                            back_off = self.coefficients[self.attempt] * self.options.interval
                            Logger.debug("Automatic back-off of {}".format(back_off))
                            self.send_enabled = False
                            time.sleep(back_off)
                            self.send_enabled = True
                time.sleep(self.interval/1000)

    def start_event_persist(self):
        Logger.debug("Starting automatic event persistence")
        if self.options.auto_send or self.send_enabled:
            self.send_enabled = True
        else:
            Logger.debug("Automatic event persistence is disabled, you should persist events manually")

    def stop_event_persist(self):
        if self.send_enabled:
            Logger.debug("Attempting to stop automatic event persistence")
            try:
                self.flush()
                if self.thread:
                    self.thread.stop()
            except ValueError as e:
                Logger.error("Could not stop event scheduler; {}".format(e))

            Logger.debug("Stopped event persistence")

    @staticmethod
    def serialize(obj):
        return {
            "rid": obj.rid,
            "eventType": obj.event_type if isinstance(obj.event_type, str) else obj.event_type.value,
            "userId": obj.user_id,
            "userTraits": {
                "name": obj.user_traits.name if obj.user_traits else "",
                "email": obj.user_traits.email if obj.user_traits else "",
                "phone": obj.user_traits.phone if obj.user_traits else "",
                "createdAt": obj.user_traits.created_at if obj.user_traits else "",
            },
            "request": {
                "cid": obj.request.cid if obj.request else "",
                "vid": obj.request.vid if obj.request else "",
                "fp": obj.request.fp if obj.request else "",
                "ip": obj.request.ip if obj.request else "",
                "remoteIp": obj.request.remote_ip if obj.request else "",
                "method": obj.request.method if obj.request else "",
                "url": obj.request.url if obj.request else "",
                "headers": obj.request.headers if obj.request else None
            },
            "timestamp": obj.timestamp,
            "properties": obj.properties,
        }
