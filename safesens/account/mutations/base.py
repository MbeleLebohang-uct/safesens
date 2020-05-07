import graphene

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.tokens import default_token_generator

from ...core.mutations import BaseMutation, ModelMutation
from ...core.types import Output
from ...core.types.common import AccountError

from ..models import User
from ..types import User as UserType
from ..enums import UserRoleEnum

from ..error_codes import AccountErrorCode

INVALID_TOKEN = "Invalid or expired token."

class ConfirmAccount(Output, BaseMutation):
    user = graphene.Field(UserType, description="An activated user account.")

    class Arguments:
        token = graphene.String(
            description="A one-time token required to confirm the account.",
            required=True,
        )
        email = graphene.String(
            description="E-mail of the user performing account confirmation.",
            required=True,
        )

    class Meta:
        description = (
            "Confirm user account with token sent by email during registration."
        )
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        try:
            user = User.objects.get(email=data["email"])
        except ObjectDoesNotExist:
            return cls(success=False, account_errors=[AccountError(field="email", message="User with this email doesn't exist.", code=AccountErrorCode.NOT_FOUND)])
          
        if not default_token_generator.check_token(user, data["token"]):
            return cls(success=False, account_errors=[AccountError(field="email", message=INVALID_TOKEN, code=AccountErrorCode.INVALID)])

        user.is_active = True
        user.save(update_fields=["is_active"])
        return cls(success=True,  user=user)


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(description="Given name.")
    last_name = graphene.String(description="Family name.")
    email = graphene.String(description="The unique email address of the user.")
    home_device_imei = graphene.String(description="The imei of the device to display on user home screen.")
    role = UserRoleEnum(description="User role: TECHNICIAN, CONTRACTOR CUSTOMER, CONTRACTOR or KOVCO STAFF.")

class UserAddressInput(graphene.InputObjectType):
    pass


class AccountInput(UserInput, UserAddressInput):
    pass


class UserCreateInput(AccountInput):
    pass


class BaseAccountCreate(ModelMutation):
    """Base mutation for account create used."""

    class Arguments:
        input = UserCreateInput(
            description="Fields required to create an account.", required=True
        )

    class Meta:
        abstract = True

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        return cleaned_input

    @classmethod
    @transaction.atomic
    def save(cls, info, instance, cleaned_input):
        super().save(info, instance, cleaned_input)