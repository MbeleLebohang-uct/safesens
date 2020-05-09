from enum import Enum


class DeviceErrorCode(Enum):
    PERMISSION_DENIED = "permission_denied"
    GRAPHQL_ERROR = "graphql_error"
    NOT_FOUND = "not_found"