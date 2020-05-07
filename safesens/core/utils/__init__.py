import graphene

from graphene import ObjectType

from typing import Optional, Union 
from urllib.parse import urljoin

from django.db.models import Q, QuerySet

from django.utils.encoding import iri_to_uri
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.conf import settings

from ..types import SortInputObjectType


def build_absolute_uri(location: str) -> Optional[str]:
    host = Site.objects.get_current().domain
    protocol = "https" if settings.ENABLE_SSL else "http"
    current_uri = "%s://%s" % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)


def from_global_id_strict_type (
    global_id: str, only_type: Union[ObjectType, str], field: str = "id"
) -> str:
    """Resolve a node global id with a strict given type required."""
    try:
        _type, _id = graphene.Node.from_global_id(global_id)
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValidationError(
            {
                field: ValidationError(
                    "Couldn't resolve to a node: %s" % global_id, code="not_found"
                )
            }
        ) from exc

    if str(_type) != str(only_type):
        raise ValidationError(
            {field: ValidationError(f"Must receive a {only_type} id", code="invalid")}
        )
    return _id

def snake_to_camel_case(name):
    """Convert snake_case variable name to camelCase."""
    if isinstance(name, str):
        split_name = name.split("_")
        return split_name[0] + "".join(map(str.capitalize, split_name[1:]))
    return name 


def filter_range_field(qs, field, value):
    gte, lte = value.get("gte"), value.get("lte")
    if gte:
        lookup = {f"{field}__gte": gte}
        qs = qs.filter(**lookup)
    if lte:
        lookup = {f"{field}__lte": lte}
        qs = qs.filter(**lookup)
    return qs


def filter_by_query_param(queryset, query, search_fields):
    """Filter queryset according to given parameters.

    Keyword Arguments:
        queryset - queryset to be filtered
        query - search string
        search_fields - fields considered in filtering

    """
    if query:
        query_by = {
            "{0}__{1}".format(field, "icontains"): query for field in search_fields
        }
        query_objects = Q()
        for q in query_by:
            query_objects |= Q(**{q: query_by[q]})
        return queryset.filter(query_objects).distinct()
    return queryset

def filter_by_manager_param(queryset, manager):
    """Filter queryset according to given parameters.

    Keyword Arguments:
        queryset - queryset to be filtered
        manager - manager user

    """
    query_objects = Q(manager=manager)
    return queryset.filter(query_objects)

def sort_queryset(
    queryset: QuerySet, sort_by: SortInputObjectType, sort_enum: graphene.Enum
) -> QuerySet:
    """Sort queryset according to given parameters.

    Keyword Arguments:
        queryset - queryset to be filtered
        sort_by - dictionary with sorting field and direction

    """
    if sort_by is None or not sort_by.field:
        return queryset

    direction = sort_by.direction
    sorting_field = sort_by.field

    custom_sort_by = getattr(sort_enum, f"sort_by_{sorting_field}", None)
    if custom_sort_by:
        return custom_sort_by(queryset, sort_by)
    return queryset.order_by(f"{direction}{sorting_field}")