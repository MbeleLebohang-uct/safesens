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
from ...core.permissions import AccountPermissions
from ...core.types.common import AccountError
from ...core.types.exceptions import (
    InvalidPassword, 
    GraphQLAuthError, 
    InvalidRedirectUrl
)
from ...core.types import Output
from ...core.utils.url import validate_safesens_url

from ..models import User
from ..types import UserType
from ..enums import UserRoleEnum
from ..emails import send_account_confirmation_email
from ..utils import get_user_permissions
from .. import UserRole


class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(description="The email address of the user.", required=True)
    password = graphene.String(description="Password.", required=True)
    role = UserRoleEnum(
        description=(
            "User role: TECHNICIAN, CONTRACTOR CUSTOMER, CONTRACTOR or KOVCO STAFF."
        ),
        required=True,
    )
    redirect_url = graphene.String(
        description=(
            "Base of safesens URL that will be needed to create confirmation URL."
        ),
        required=False,
    )

class AccountRegister(Output, ModelMutation):
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
    @login_required
    def mutate(cls, root, info, **data):
        response = super().mutate(root, info, **data)
        response.requires_confirmation = settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL
        response.success = True
        return response

    @classmethod
    def clean_input(cls, info, instance, data, input_cls=None):
        password = data["password"]
        try:
            password_validation.validate_password(password, instance)
        except ValidationError as error:
            raise InvalidPassword(error_field="password", errors=error)

            
        if not settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            return super().clean_input(info, instance, data, input_cls=None)
        elif not data.get("redirect_url"):
            raise GraphQLAuthError(error_field="redirect_url", message="This field is required.")

        try:
            validate_safesens_url(data["redirect_url"])
        except ValidationError as error:
            raise InvalidRedirectUrl(error_field="redirect_url", message="This field is invalid.", errors=error)

        return super().clean_input(info, instance, data, input_cls=None)

    @classmethod
    def _check_current_user_permissions(cls, info, user, role):
        current_user = info.context.user
        if current_user.is_contractor() and role!=UserRole.CONTRACTOR_CUSTOMER:
            return cls(success=False, account_errors=[AccountError(message="Contractor is only authorized to create its customer.", code=AccountErrorCode.CONTRACTOR_UNAUTHORISED)]) 

        if current_user.is_contractor_customer() and role!=UserRole.TECHNICIAN:
            return cls(success=False, account_errors=[AccountError(message="A customer is only authorized to create its teachnician.", code=AccountErrorCode.CUSTOMER_UNAUTHORISED)])

        if (current_user.is_staff() or current_user.is_superuser) and role!=UserRole.CONTRACTOR and role!=UserRole.KOVCO_STAFF:
            return cls(success=False, account_errors=[AccountError(message="Staff is only authorized to create contractors.", code=AccountErrorCode.STAFF_UNAUTHORISED)])

        return cls(success=True, account_errors=None)

        
    @classmethod
    def save(cls, info, user, cleaned_input):
        password = cleaned_input["password"]
        user.set_password(password)

        results = cls._check_current_user_permissions(info, user, user.role)

        if results.success == False:
            return results

        if settings.ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL:
            user.is_active = False
            user.save()
            send_account_confirmation_email(user, cleaned_input["redirect_url"])
        else:
            user.save()

        permissions = get_user_permissions(user.role)
        for permission in permissions:
            user.user_permissions.add(permission)
        

    @classmethod
    def populate_required_fields(cls, info, instance, data):
        instance.manager = info.context.user
        super().populate_required_fields(info, instance, data)


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
            raise GraphQLAuthError(message="This field is required.", errors=e)
            