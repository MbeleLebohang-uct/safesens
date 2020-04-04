import graphene
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["password"]

class AccountQuery(graphene.ObjectType):
    user = graphene.Field(UserType, email=graphene.String())

    def resolve_user(self, info, email=None, **kwargs):
        if email:
            return User.objects.get(Q(email=email))
        return None