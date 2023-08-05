import hmac
import hashlib


class SignatureUtils(object):
    SignatureHeader = "x-securenative"

    @staticmethod
    def is_valid_signature(api_key, payload, header_signature):
        try:
            key = api_key.encode('utf-8')
            body = payload.encode('utf-8')
            comparison_signature = hmac.new(key, body, hashlib.sha512).hexdigest()
            return hmac.compare_digest(comparison_signature, header_signature)
        except Exception:
            return False
