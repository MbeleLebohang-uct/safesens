import graphene

from graphene_federation import key
import graphene_django_optimizer as gql_optimizer

from ..core.types import PermissionDisplay, Address as AddressType
from ..core.connection import CountableDjangoObjectType

from .models import Device

@key("id")
@key("imei")
class Device(CountableDjangoObjectType):
    permissions = graphene.List(
        PermissionDisplay, description="List of device's permissions."
    )

    unit_location = gql_optimizer.field(
        graphene.Field(AddressType, description="Device's address."),
        model_field="address",
    )

    class Meta:
        description = "Represents device data."
        interfaces = [graphene.relay.Node, ]
        model = Device

