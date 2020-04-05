from graphene_django.types import DjangoObjectType
from .models import Device

class DeviceType(DjangoObjectType):
    class Meta:
        model = Device