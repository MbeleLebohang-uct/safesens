from graphql_jwt.utils import jwt_payload
from django.contrib.auth.models import  Permission
from ..core.permissions import AccountPermissions, DevicePermissions
from . import UserRole


def create_jwt_payload(user, context=None):
    payload = jwt_payload(user, context)
    payload["role"] = user.role
    payload["is_superuser"] = user.is_superuser
    return payload

def get_user_permissions(role):
    permissions = []
    if role == UserRole.KOVCO_STAFF:
        permissions = [Permission.objects.get(codename=AccountPermissions.MANAGE_STAFF.codename)]
    elif role == UserRole.CONTRACTOR:
        permissions = [Permission.objects.get(codename=AccountPermissions.IS_CONTRACTOR.codename)]
    elif role == UserRole.CONTRACTOR_CUSTOMER:
        permissions = [Permission.objects.get(codename=AccountPermissions.IS_CONTRACTOR_CUSTOMER.codename)]
    elif role == UserRole.TECHNICIAN:
        permissions = [Permission.objects.get(codename=AccountPermissions.IS_TECHNICIAN.codename)]

    permissions.append(Permission.objects.get(codename=DevicePermissions.MANAGE_DEVICES.codename))

    return permissions