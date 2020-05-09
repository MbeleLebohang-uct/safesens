import graphene

from ...core.mutations import BaseMutation
from ...core.permissions import DevicePermissions
from ...core.types.common import DeviceError

from ..types import Device as DeviceType
from ..error_codes import DeviceErrorCode
from ..models import Device

from ...account.types import User as UserType


class DeviceAssignUser(BaseMutation):
    device = graphene.Field(DeviceType, description="Device to which the user were assigned.")

    class Arguments:
        device_id = graphene.ID(
            description="ID of the device to which user will be assigned.",
            required=True,
        )
        user_id = graphene.ID(
            required=True,
            description= "The ID of the user.",
        )

    class Meta:
        description = "Set the user as one of the managers of this device. The device must belong to the authenticated user"
        error_type_class = DeviceError
        error_type_field = "device_errors"
        model = Device
        permissions = (DevicePermissions.MANAGE_DEVICES, DevicePermissions.ASSIGN_DEVICES)

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, device_id, user_id):
        device = cls.get_node_or_error(
            info, device_id, only_type=DeviceType, field="device_id"
        )

        # check if the current user owns the device they are trying to assign to the other user.
        # if not, return error permission denied

        try:
            info.context.user.devices.get(imei=device.imei)
        except Device.DoesNotExist:
            device_errors = [
                DeviceError(
                    field="device_id",
                    message="Authenticated user does not own the device with the given ID",
                    code=DeviceErrorCode.PERMISSION_DENIED,
                )
            ]
            return cls(device=None, device_errors=device_errors)

        user = cls.get_node_or_error(
            info, user_id, only_type=UserType, field="user_id"
        )

        user.devices.add(device)
        return DeviceAssignUser(device=device, device_errors=[])

    
class DeviceUnassignUser(BaseMutation):
    device = graphene.Field(DeviceType, description="Device to which the user were assigned.")

    class Arguments:
        device_id = graphene.ID(
            description="ID of the device to which user will be assigned.",
            required=True,
        )
        user_id = graphene.ID(
            required=True,
            description= "The ID of the user.",
        )

    class Meta:
        description = "Removes the user assigned as the owner of the device. The device must belong to the authenticated user"
        error_type_class = DeviceError
        error_type_field = "device_errors"
        model = Device
        permissions = (DevicePermissions.MANAGE_DEVICES, DevicePermissions.ASSIGN_DEVICES)

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, device_id, user_id):
        device = cls.get_node_or_error(
            info, device_id, only_type=DeviceType, field="device_id"
        )

        # check if the current user owns the device they are trying to assign to the other user.
        # if not, return error permission denied

        try:
            info.context.user.devices.get(imei=device.imei)
        except Device.DoesNotExist:
            device_errors = [
                DeviceError(
                    field="device_id",
                    message="Authenticated user does not own the device with the given ID",
                    code=DeviceErrorCode.PERMISSION_DENIED,
                )
            ]
            return cls(device=None, device_errors=device_errors)

        user = cls.get_node_or_error(
            info, user_id, only_type=UserType, field="user_id"
        )

        if user == info.context.user:
            device_errors = [
                DeviceError(
                    field="user_id",
                    message="User is not allowed to unassign devices from themselves",
                    code=DeviceErrorCode.PERMISSION_DENIED,
                )
            ]
            return cls(device=None, device_errors=device_errors)

        
        user.devices.remove(device)
        return cls(device=device, device_errors=[])