from enum import IntEnum


class ErrorCodes(IntEnum):
    ERROR_NONE = 0,
    ERROR_GIT_MISSING = 1,
    ERROR_INVALID_CONFIG = 2,
    ERROR_ABORTED_BY_USER = 255,
