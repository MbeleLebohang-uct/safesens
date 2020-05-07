import graphene

import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from ..core.fields import FilterInputConnectionField
from ..core.types import FilterInputObjectType

from .types import User as UserType
from .mutations.account import (
    CreateToken, 
    VerifyToken, 
    AccountRegister,
    AccountUpdate
)

from .mutations.base import (
    ConfirmAccount
)

from .filters import (
    TechnicianFilter,
    UserFilter,
)

from .sorters import (
    UserSortingInput,
)

from .resolvers import (
    resolve_own_technicians,
    resolve_own_users
)


class TechnicianFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = TechnicianFilter


class UserFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = UserFilter


class AccountQuery(graphene.ObjectType):
    own_users = FilterInputConnectionField(
        UserType,
        filter=UserFilterInput(description="Filtering options for all users."),
        sort_by=UserSortingInput(description="Sort all users."),
        description="List of the Kovco's users that are managed by authenticate user.",
    )
    own_technicians = FilterInputConnectionField(
        UserType,
        filter=TechnicianFilterInput(description="Filtering options for technician users."),
        sort_by=UserSortingInput(description="Sort technician users."),
        description="List of the Kovco's technician users.",
    )

    me = graphene.Field(UserType, description="Return the currently authenticated user.")

    @login_required
    def resolve_own_technicians(self, info, query=None, **kwargs):
        return resolve_own_technicians(info, query=query, **kwargs)


    @login_required
    def resolve_own_users(self, info, query=None, **kwargs):
        return resolve_own_users(info, query=query, **kwargs)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return user if user.is_authenticated else None


class AccountMutation(graphene.ObjectType):
    token_create = CreateToken.Field()
    token_verify = VerifyToken.Field()
    token_refresh = graphql_jwt.Refresh.Field()
     
    account_register = AccountRegister.Field()
    account_confirm = ConfirmAccount.Field()

    account_update = AccountUpdate.Field()