import graphene

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.tokens import default_token_generator

from ...core.mutations import BaseMutation
from ...core.types import Output
from ...core.types.common import AccountError

from ..models import User
from ..types import UserType

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
