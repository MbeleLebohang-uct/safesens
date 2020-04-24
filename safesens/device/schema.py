import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from ..account.models import User
from .models import Device

class DeviceFilter(django_filters.FilterSet):
    class Meta:
        model = Device
        fields = ['imei']

class DeviceNode(DjangoObjectType):
    class Meta:
        model = Device
        fields = []
        interfaces = (graphene.relay.Node, )

class DeviceQuery(graphene.ObjectType):
    user_devices = DjangoFilterConnectionField(DeviceNode, filterset_class=DeviceFilter)

    def resolve_user_devices(self, info, **kwargs):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise GraphQLError("Permision Denied: User not authenticated.")

        return current_user.device_set.all()
            