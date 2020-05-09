from enum import Enum

from django.contrib.auth.models import Permission


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class AccountPermissions(BasePermissionEnum):
    MANAGE_STAFF = "account.manage_staff"
    IS_TECHNICIAN = "account.is_technician"
    IS_CONTRACTOR = "account.is_contractor"
    IS_CONTRACTOR_CUSTOMER = "account.is_contractor_customer"

class DevicePermissions(BasePermissionEnum):
    MANAGE_DEVICES = "device.manage_devices"
    ASSIGN_DEVICES = "device.assign_devices"

PERMISSIONS_ENUMS = [
    DevicePermissions,
    AccountPermissions
]

def get_permissions_enum_list():
    permissions_list = [
        (enum.name, enum.value)
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    ]
    return permissions_list