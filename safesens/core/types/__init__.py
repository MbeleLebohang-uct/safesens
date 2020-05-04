import graphene

from .common import (
    Error,
    PermissionDisplay,
    Image,
)

from .upload import Upload

class Output(graphene.ObjectType):
    """
    A class to all public classes extend to
    padronize the output
    """

    success = graphene.Boolean(default_value=True)
