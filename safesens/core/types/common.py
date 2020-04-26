import graphene

from ..enums import (
    AccountErrorCode,
    PermissionEnum,
)

from ..models import ModelWithMetadata

 
class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class AccountError(Error):
    code = AccountErrorCode(description="The error code.", required=True)


class PermissionDisplay(graphene.ObjectType):
    code = PermissionEnum(description="Internal code for permission.", required=True)
    name = graphene.String(
        description="Describe action(s) allowed to do by permission.", required=True
    )

    class Meta:
        description = "Represents a permission object in a friendly form."


class Image(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the image.")
    alt = graphene.String(description="Alt text for an image.")

    class Meta:
        description = "Represents an image."


class MetadataItem(graphene.ObjectType):
    key = graphene.String(required=True, description="Key of a metadata item.")
    value = graphene.String(required=True, description="Value of a metadata item.")


class ObjectWithMetadata(graphene.Interface):
    private_metadata = graphene.List(
        MetadataItem,
        required=True,
        description=(
            "List of private metadata items."
            "Requires proper staff permissions to access."
        ),
    )
    metadata = graphene.List(
        MetadataItem,
        required=True,
        description=(
            "List of public metadata items. Can be accessed without permissions."
        ),
    )


    @staticmethod
    def resolve_metadata(root: ModelWithMetadata, _info):
        return resolve_metadata(root.metadata)

    @staticmethod
    def resolve_private_metadata(root: ModelWithMetadata, info):
        return resolve_private_metadata(root, info)
