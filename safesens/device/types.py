import graphene

from graphene_federation import key

from ..core.types import PermissionDisplay
from ..core.connection import CountableDjangoObjectType

from .models import Device

# @key("id")
# @key("imei")
# class Device(CountableDjangoObjectType):
#     permissions = graphene.List(
#         PermissionDisplay, description="List of device's permissions."
#     )

#     class Meta:
#         description = "Represents device data."
#         interfaces = [relay.Node, ]
#         model = Device


class Device(CountableDjangoObjectType):
    class Meta:
        description = "Device object."
        model = Device
        interfaces = [graphene.relay.Node]

