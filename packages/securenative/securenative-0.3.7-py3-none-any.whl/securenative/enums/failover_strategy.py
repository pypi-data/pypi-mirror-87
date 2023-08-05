from enum import Enum


class FailOverStrategy(Enum):
    FAIL_OPEN = "fail-open"
    FAIL_CLOSED = "fail-closed"
