import graphene

from django.conf import settings
from django.contrib.auth import get_user_model, password_validation

from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt import relay
from graphql_jwt.exceptions import JSONWebTokenError, PermissionDenied
from graphql_jwt.decorators import login_required

from graphql import GraphQLError

from django.core.exceptions import (
    ValidationError,
)

from ..error_codes import AccountErrorCode

from ...core.mutations import validation_error_to_error_type, ModelMutation
from ...core.types.common import AccountError
from ...core.utils.url import validate_safesens_url

from ..models import User
from ..types import UserType
from ..utils import CustomerTypes




#---------------------------------------------------------------------------------
class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(description="The email address of the user.", required=True)
    password = graphene.String(description="Password.", required=True)
    user_type = graphene.Enum.from_enum(CustomerTypes)(description="The role of the use to register.", required=True)
    redirect_url = graphene.String(
        description=(
            "Base of safesens URL that will be needed to create confirmation URL."
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

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        response = super().mutate(root, info, **data)
        response.requires_confirmation = settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL
        return response

    @classmethod
    def clean_input(cls, info, instance, data, input_cls=None):
        password = data["password"]
        try:
            password_validation.validate_password(password, instance)
        except ValidationError as error:
            raise GraphQLError(error.messages[0])

            
        if not settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            return super().clean_input(info, instance, data, input_cls=None)
        elif not data.get("redirect_url"):
            # TODO: Learn about django email verification
            raise ValidationError(
                {
                    "redirect_url": ValidationError(
                        "This field is required.", code=AccountErrorCode.REQUIRED
                    )
                }
            )

        try:
            validate_safesens_url(data["redirect_url"])
        except ValidationError as error:
            raise ValidationError(
                {
                    "redirect_url": ValidationError(
                        error.message, code=AccountErrorCode.INVALID
                    )
                }
            )

        return super().clean_input(info, instance, data, input_cls=None)

    @classmethod
    def save(cls, info, user, cleaned_input):
        password = cleaned_input["password"]
        user.set_password(password)
        if settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            user.is_active = False
            user.save()
            emails.send_account_confirmation_email(user, cleaned_input["redirect_url"])
        else:
            user.save()
        

    @classmethod
    def populate_required_fields(cls, info, instance, data):
        instance.manager = info.context.user
        super().populate_required_fields(info, instance, data)

#---------------------------------------------------------------------------------

class CreateToken(relay.JSONWebTokenMutation):
    """Mutation that authenticates a user and returns token and user data.

    It overrides the default graphql_jwt.ObtainJSONWebToken to wrap potential
    authentication errors in our Error type, which is consistent to how the rest of
    the mutation works.
    """

    account_errors = graphene.List(
        graphene.NonNull(AccountError),
        description="List of errors that occurred executing the mutation.",
        required=True,
    )
    user = graphene.Field(UserType, description="A user instance.")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            result = super().mutate(root, info, **kwargs)
        except JSONWebTokenError as e:
            account_errors = [
                AccountError(
                    field="email",
                    message="Please, enter valid credentials",
                    code=AccountErrorCode.INVALID_CREDENTIALS,
                )
            ]
            
            return cls(user=None, token="", account_errors=account_errors)
        except ValidationError as e:
            errors = validation_error_to_error_type(e)
            return cls.handle_typed_errors(errors)
        else:
            return result

    @classmethod
    def handle_typed_errors(cls, errors: list):
        account_errors = [
            AccountError(field=e.field, message=e.message, code=code)
            for e, code, _params in errors
        ]
        return cls(user=None, token="", account_errors=account_errors)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user, account_errors=[])

class VerifyToken(Verify):
    """Mutation that confirms if token is valid and also returns user data."""

    account_errors = graphene.List(
        graphene.NonNull(AccountError),
        description="List of errors that occurred executing the mutation.",
        required=True,
    )

    user = graphene.Field(UserType)

    def resolve_user(self, _info, **_kwargs):
        username_field = get_user_model().USERNAME_FIELD
        kwargs = {username_field: self.payload.get(username_field)}
        return User.objects.get(**kwargs)

    @classmethod
    def mutate(cls, root, info, token, **kwargs):
        try:
            return super().mutate(root, info, token, **kwargs)
        except JSONWebTokenError as e:
            print(str(e))
            
            return None
