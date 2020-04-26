import graphene
from django.conf import settings

from ...core.mutations import ModelMutation
from ...core.types.common import AccountError

from ..models import User

from django.db import models

class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(description="The email address of the user.", required=True)
    password = graphene.String(description="Password.", required=True)
    redirect_url = graphene.String(
        description=(
            "Base of frontend URL that will be needed to create confirmation URL."
        ),
        required=False,
    )

class AccountRegister(ModelMutation):
    class Arguments:
        input = AccountRegisterInput(
            description="Fields required to create a user.", required=True
        )

    requires_confirmation = graphene.Boolean(
        description="Informs whether users need to confirm their email address."
    )

    class Meta:
        description = "Register a new user."
        exclude = ["password"]
        model = User
        error_type_class = AccountError
        error_type_field = "account_errors"