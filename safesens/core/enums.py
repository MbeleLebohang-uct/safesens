import graphene

from ..account import error_codes as account_error_codes
from .permissions import get_permissions_enum_list

PermissionEnum = graphene.Enum("PermissionEnum", get_permissions_enum_list())

AccountErrorCode = graphene.Enum.from_enum(account_error_codes.AccountErrorCode)