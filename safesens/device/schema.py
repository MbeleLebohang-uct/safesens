import graphene

from graphql_jwt.decorators import login_required
from graphql_jwt.exceptions import PermissionDenied

from ..core.fields import FilterInputConnectionField

from .models import Device
from .types import Device as DeviceType

from .mutations.device import (
    DeviceAssignUser,
    DeviceUnassignUser,
    DeviceUpdate
)

from .filters import (
    DeviceFilterInput,
)

from .sorters import (
    DeviceOrder,
)

from .resolvers import (
    resolve_devices,
)


class DeviceQuery(graphene.ObjectType):
    device = graphene.Field(
        DeviceType,
        id=graphene.Argument(
            graphene.ID, description="ID of the device.", required=True
        ),
        description="Look up a device that belong to authenticate user by ID.",
    )

    home_device = graphene.Field(
        DeviceType,
        description="Get the home device for the authenticate user.",
    )

    devices = FilterInputConnectionField(
        DeviceType,
        filter=DeviceFilterInput(description="Filtering options for devices."),
        sort_by=DeviceOrder(description="Sort devices."),
        description="List of devices that are belong to the authenticated user.",
    )

    @login_required
    def resolve_device(self, info, id):
        device = graphene.Node.get_node_from_global_id(info, id, DeviceType)

        try:
            info.context.user.devices.get(imei=device.imei)
        except Device.DoesNotExist:
            raise PermissionDenied()
        
        return device

    @login_required
    def resolve_home_device(self, info):
        home_device_imei = info.context.user.home_device_imei

        if ((home_device_imei == None) or (home_device_imei == "")):
            return None

        device = None
        try:
            device = info.context.user.devices.get(imei=home_device_imei)
        except Device.DoesNotExist:
            return None
        
        return device

    @login_required
    def resolve_devices(self, info, **kwargs):
        return resolve_devices(info, **kwargs)

class DeviceMutation(graphene.ObjectType):
    device_assign_user = DeviceAssignUser.Field()
    device_unassign_user = DeviceUnassignUser.Field()

    device_update = DeviceUpdate.Field()
    