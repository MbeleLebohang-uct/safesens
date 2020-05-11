import graphene

from .common import (
    Error,
    PermissionDisplay,
    CountryDisplay,
    Address,
    Image,
)

from .upload import Upload
from .filter_input import FilterInputObjectType
from .sort_input import SortInputObjectType

class Output(graphene.ObjectType):
    """
    A class to all public classes extend to
    padronize the output
    """

    success = graphene.Boolean(default_value=True)
