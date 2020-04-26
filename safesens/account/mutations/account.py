import graphene

from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError, PermissionDenied

from django.core.exceptions import (
    ValidationError,
)

from ..error_codes import AccountErrorCode

from ...core.mutations import validation_error_to_error_type
from ...core.types.common import AccountError

from ..models import User
from ..types import UserType

class CreateToken(ObtainJSONWebToken):
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

