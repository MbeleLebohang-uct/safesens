import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

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
    device = graphene.relay.Node.Field(DeviceNode)
    all_devices = DjangoFilterConnectionField(DeviceNode, filterset_class=DeviceFilter)
