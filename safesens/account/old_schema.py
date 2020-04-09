import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from .models import User
from ..device.models import Device
from ..device.types import DeviceType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["password"]

class AccountQuery(graphene.ObjectType):
    user             = graphene.Field(UserType, email=graphene.String())
    user_home_device = graphene.Field(DeviceType, email=graphene.String(required=True))

    def resolve_user(self, info, email=None, **kwargs):
        if email:
            return User.objects.get(Q(email=email))
        return None

    def resolve_user_home_device(self, info, email=None, **kwargs):
        user = None
        if email:
            try:
                user = User.objects.get(Q(email=email))
            except User.DoesNotExist:
                raise GraphQLError("UserNotFound: User with the given email does not exist.")

            home_device_imei = user.home_device_imei
            if home_device_imei == "":
                raise GraphQLError("DeviceIMEIEmpty: No home device set.")

            try:
                return user.device_set.get(Q(imei=home_device_imei))
            except Device.DoesNotExist:
                raise GraphQLError("DeviceNotFound: User does not have the the device with the imei.")
        else:
            GraphQLError("UserEmailEmpty: No email was provided.")

        return None