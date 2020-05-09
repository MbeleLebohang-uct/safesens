import graphene

from ..account import error_codes as account_error_codes
from ..device import error_codes as device_error_codes 
from .permissions import get_permissions_enum_list

PermissionEnum = graphene.Enum("PermissionEnum", get_permissions_enum_list())

AccountErrorCode = graphene.Enum.from_enum(account_error_codes.AccountErrorCode)

DeviceErrorCode = graphene.Enum.from_enum(device_error_codes.DeviceErrorCode)

class OrderDirection(graphene.Enum):
    ASC = ""
    DESC = "-"

    @property
    def description(self):
        if self == OrderDirection.ASC:
            return "Specifies an ascending sort order."
        if self == OrderDirection.DESC:
            return "Specifies a descending sort order."
        raise ValueError("Unsupported enum value: %s" % self.value)