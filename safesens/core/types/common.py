import graphene

from graphene import relay
from graphene_federation import key
from graphene_django.utils import camelize

from ..enums import (
    AccountErrorCode,
    DeviceErrorCode,
    PermissionEnum,
)

from ..templatetags.images import get_thumbnail
from ..connection import CountableDjangoObjectType
from ..models import Address
from .exceptions import WrongUsage


class CountryDisplay(graphene.ObjectType):
    code = graphene.String(description="Country code.", required=True)
    country = graphene.String(description="Country name.", required=True)

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

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise WrongUsage("`errors` must be list or dict!")


class AccountError(Error):
    code = AccountErrorCode(description="The error code.", required=True)


class DeviceError(Error):
    code = DeviceErrorCode(description="The error code.", required=True)


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

    @staticmethod
    def get_adjusted(image, alt, size, rendition_key_set, info):
        """Return Image adjusted with given size."""
        if size:
            url = get_thumbnail(
                image_file=image,
                size=size,
                method="thumbnail",
                rendition_key_set=rendition_key_set,
            )
        else:
            url = image.url
        url = info.context.build_absolute_uri(url)
        return Image(url, alt)

class DateRangeInput(graphene.InputObjectType):
    gte = graphene.Date(description="Start date.", required=False)
    lte = graphene.Date(description="End date.", required=False)

@key(fields="id")
class Address(CountableDjangoObjectType):
    country = graphene.Field(
        CountryDisplay, required=True, description="Country name."
    )

    class Meta:
        description = "Represents address data."
        interfaces = [relay.Node]
        model = Address
        exclude = ("address", "unit_location", )
       
    @staticmethod
    def resolve_country(root: Address, _info):
        return CountryDisplay(code=root.country.code, country=root.country.name)