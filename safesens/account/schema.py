import graphene
import django_filters
import graphql_jwt
from graphql import GraphQLError
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import User
from .constants import Messages
from .bases import Output
from .types import UserNode
from .enums import UserRoleEnum

from .mutations.account import (
    AccountRegister,
    VerifyToken
)

from . import UserRole


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['email']


class Register(Output, graphene.relay.ClientIDMutation):
    user = graphene.Field(UserNode)

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        role = UserRoleEnum(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        current_user = info.context.user or None
        role = input.get('role')

        if not current_user.is_authenticated:
            return cls(success=False, errors=Messages.NOT_AUTHENICATED)

        if current_user.is_technician():
            return cls(success=False, errors=Messages.TECHNICIAN_UNAUTHORISED)

        if current_user.is_contractor() and role!=UserRole.CONTRACTOR_CUSTOMER:
            return cls(success=False, errors=Messages.CONTRACTOR_UNAUTHORISED)

        if current_user.is_contractor_customer() and role!=UserRole.TECHNICIAN:
            return cls(success=False, errors=Messages.CUSTOMER_UNAUTHORISED)

        if (current_user.is_staff() or current_user.is_superuser) and role!=UserRole.CONTRACTOR and role!=UserRole.STAFF:
            return cls(success=False, errors=Messages.STAFF_UNAUTHORISED)
       
        user = User.objects.create_user(
            email=input.get('email'),
            is_active=True,
            role=role,
            password=input.get('password'),
            manager=current_user
        )

        return Register(user=user)

class AccountQuery(graphene.ObjectType):
    own_users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)
    get_technicians = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)

    def resolve_get_technicians(self, info, **kwargs):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise GraphQLError("Permision Denied: User not authenticated.")
            
        return User.objects.filter(Q(manager=current_user) and Q(role=UserRole.TECHNICIAN))

    def resolve_own_users(self, info, **kwargs):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise GraphQLError("Permision Denied: User not authenticated.")

        return User.objects.filter(Q(manager=current_user))


class AccountMutation(graphene.ObjectType):
    register = Register.Field()
    account_register = AccountRegister.Field()

    token_create = graphql_jwt.ObtainJSONWebToken.Field()
    verify_auth = VerifyToken.Field()
    refresh_auth = graphql_jwt.Refresh.Field()