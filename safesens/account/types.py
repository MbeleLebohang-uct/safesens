import graphene
from graphene import relay
from graphene_django.utils import camelize
from graphene_federation import key

from django.contrib.auth import get_user_model

from .exceptions import WrongUsage

from ..core.types import Image, PermissionDisplay, ObjectWithMetadata
from ..core.connection import CountableDjangoObjectType

from . import models

class ExpectedErrorType(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.
    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise WrongUsage("`errors` must be list or dict!")


@key("id")
@key("email")
class User(CountableDjangoObjectType):
    permissions = graphene.List(
        PermissionDisplay, description="List of user's permissions."
    )
    avatar = graphene.Field(Image, size=graphene.Int(description="Size of the avatar."))
    is_staff = graphene.Boolean(description="Is the user a staff member or not.")

    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = get_user_model()
        only_fields = [
            "date_joined",
            "email",
            "first_name",
            "id",
            "is_active",
            "is_staff",
            "last_login",
            "last_name",
        ]


    @staticmethod
    def resolve_permissions(root: models.User, _info, **_kwargs):
        if root.is_superuser:
            permissions = get_permissions()
        else:
            permissions = root.user_permissions.prefetch_related(
                "content_type"
            ).order_by("codename")
        return format_permissions_for_display(permissions)


    @staticmethod
    def resolve_avatar(root: models.User, info, size=None, **_kwargs):
        if root.avatar:
            return Image.get_adjusted(
                image=root.avatar,
                alt=None,
                size=size,
                rendition_key_set="user_avatars",
                info=info,
            )

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        if root.id is not None:
            return graphene.Node.get_node_from_global_id(_info, root.id)
        return get_user_model().objects.get(email=root.email)
