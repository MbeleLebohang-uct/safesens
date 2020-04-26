import graphene
from django.conf import settings
from django.contrib.auth import password_validation, get_user_model
from django.core.exceptions import ValidationError

from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError

from ...core.mutations import ModelMutation, validation_error_to_error_type
from ...core.permissions import AccountPermissions
from ...core.types.common import AccountError, Error
from ...core.utils.url import validate_frontend_url

from ..error_codes import AccountErrorCode
from ..enums import UserRoleEnum
from ..models import User
from ..types import UserNode

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
    role = UserRoleEnum(
        description=(
            "User role: TECHNICIAN, CONTRACTOR CUSTOMER, CONTRACTOR or KOVCO STAFF."
        ),
        required=True,
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
        permissions = (AccountPermissions.MANAGE_STAFF, AccountPermissions.IS_CONTRACTOR, AccountPermissions.IS_CONTRACTOR_CUSTOMER,)

    @classmethod
    def mutate(cls, root, info, **data):
        # print("----------------------m1-------------------------")
        # temp = {'input': {'email': 'mblleb006@gmail.com', 'password': 'password123', 'redirect_url': 'localhost:8000', 'role': 'technician'}}
        
        # print(temp)
        # if temp['input']:
        #     temp['input']['manager'] = info.context.user
        # print(temp)

        response = super().mutate(root, info, **data)
        print("----------------------m2-------------------------")
        response.requires_confirmation = settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL
        return response

    
    @classmethod
    def clean_input(cls, info, instance, data, input_cls=None):
        if not settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            return super().clean_input(info, instance, data, input_cls=None)
        elif not data.get("redirect_url"):
            raise ValidationError(
                {
                    "redirect_url": ValidationError(
                        "This field is required.", code=AccountErrorCode.REQUIRED
                    )
                }
            )

        try:
            validate_frontend_url(data["redirect_url"])
        except ValidationError as error:
            raise ValidationError(
                {
                    "redirect_url": ValidationError(
                        error.message, code=AccountErrorCode.INVALID
                    )
                }
            )

        password = data["password"]
        try:
            password_validation.validate_password(password, instance)
        except ValidationError as error:
            raise ValidationError({"password": error})

        return super().clean_input(info, instance, data, input_cls=None)

    @classmethod
    def save(cls, info, user, cleaned_input):
        print("----------------------save-------------------------")
        password = cleaned_input["password"]
        user.set_password(password)
        if settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            user.is_active = False
            user.save()
            emails.send_account_confirmation_email(user, cleaned_input["redirect_url"])
        else:
            user.save()


class VerifyToken(Verify):
    """Mutation that confirms if token is valid and also returns user data."""

    user = graphene.Field(UserNode)

    def resolve_user(self, _info, **_kwargs):
        username_field = get_user_model().USERNAME_FIELD
        kwargs = {username_field: self.payload.get(username_field)}
        return models.User.objects.get(**kwargs)

    @classmethod
    def mutate(cls, root, info, token, **kwargs):
        try:
            return super().mutate(root, info, token, **kwargs)
        except JSONWebTokenError:
            return None
