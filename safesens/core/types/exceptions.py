from django.utils.translation import gettext as _
from graphene_django.utils import camelize

class GraphQLAuthError(Exception):
    errors = None
    default_message = None
    field = None

    def __init__(self, error_field=None, message=None, errors=None):
        field = error_field
        if message is None:
            message = self.default_message

        if errors is not None:
            if isinstance(errors, dict):
                if errors.get("__all__", False):
                    errors["non_field_errors"] = errors.pop("__all__")
                return camelize(errors)
            elif isinstance(errors, list):
                return {"nonFieldErrors": errors}
        
        super().__init__(message)


class UserAlreadyVerified(GraphQLAuthError):
    default_message = _("User already verified.")


class InvalidPassword(GraphQLAuthError):
    default_message = _("Invalid password.")


class InvalidRedirectUrl(GraphQLAuthError):
    default_message = _("Invalid redirect url.")


class InvalidCredentials(GraphQLAuthError):
    default_message = _("Invalid credentials.")


class UserNotVerified(GraphQLAuthError):
    default_message = _("User is not verified.")


class EmailAlreadyInUse(GraphQLAuthError):
    default_message = _("This email is already in use.")


class TokenScopeError(GraphQLAuthError):
    default_message = _("This token if for something else.")


class WrongUsage(GraphQLAuthError):
    """
    internal exception
    """

    default_message = _("Wrong usage, check your code!.")
