import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import User

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['email']

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        interfaces = (graphene.relay.Node, )

class AccountQuery(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)

