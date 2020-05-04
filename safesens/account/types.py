import graphene
from graphene import relay
from django.contrib.auth import get_user_model
from graphene_federation import key

from ..core.types import PermissionDisplay, Image
from ..core.connection import CountableDjangoObjectType
 
from . import models


@key("id")
@key("email")
class UserType(CountableDjangoObjectType):
    permissions = graphene.List(
        PermissionDisplay, description="List of user's permissions."
    )
    is_staff = graphene.Boolean(description="Is the user a staff member or not.")
    avatar = graphene.Field(Image, size=graphene.Int(description="Size of the avatar."))

    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ]
        model = get_user_model()


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