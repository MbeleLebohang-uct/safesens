import graphene
from graphene import ObjectType
from graphene.types.mutation import MutationOptions
from graphene_django.registry import get_global_registry

from django.core.exceptions import (
    NON_FIELD_ERRORS,
    ImproperlyConfigured,
    ValidationError,
)
from typing import Tuple, Union
from itertools import chain

from graphql.error import GraphQLError

from .types import Error
from .utils import from_global_id_strict_type, snake_to_camel_case
from .utils.error_codes import get_error_code_from_error
 

registry = get_global_registry()
 
def get_model_name(model):
    """Return name of the model with first letter lowercase."""
    model_name = model.__name__
    return model_name[:1].lower() + model_name[1:]

def get_output_fields(model, return_field_name):
    """Return mutation output field for model instance."""
    model_type = registry.get_type_for_model(model)
    if not model_type:
        raise ImproperlyConfigured(
            "Unable to find type for model %s in graphene registry" % model.__name__
        )
    fields = {return_field_name: graphene.Field(model_type)}
    return fields

def get_error_fields(error_type_class, error_type_field):
    return {
        error_type_field: graphene.Field(
            graphene.List(
                graphene.NonNull(error_type_class),
                description="List of errors that occurred executing the mutation.",
            ),
            default_value=[],
            required=True,
        )
    }

def validation_error_to_error_type(validation_error: ValidationError) -> list:
    """Convert a ValidationError into a list of Error types."""
    err_list = []
    if hasattr(validation_error, "error_dict"):
        # convert field errors
        for field, field_errors in validation_error.error_dict.items():
            field = None if field == NON_FIELD_ERRORS else snake_to_camel_case(field)
            for err in field_errors:
                err_list.append(
                    (
                        Error(field=field, message=err.messages[0]),
                        get_error_code_from_error(err),
                        err.params,
                    )
                )
    else:
        # convert non-field errors
        for err in validation_error.error_list:
            err_list.append(
                (
                    Error(message=err.messages[0]),
                    get_error_code_from_error(err),
                    err.params,
                )
            )
    return err_list