import graphene
from django.db.models import Q
from .models import Device
from .types import Device as DeviceType

from .mutations.device import (
    DeviceAssignUser,
    DeviceUnassignUser,
    DeviceUpdate
)

class DeviceQuery(graphene.ObjectType):
    device = graphene.Field(DeviceType, imei=graphene.String())

    def resolve_device(self, info, imei=None, **kwargs):
        if imei:
            return Device.objects.get(Q(imei=imei))

        return None

class DeviceMutation(graphene.ObjectType):
    device_assign_user = DeviceAssignUser.Field()
    device_unassign_user = DeviceUnassignUser.Field()

    device_update = DeviceUpdate.Field()