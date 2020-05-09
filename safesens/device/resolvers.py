from django.db.models import QuerySet
import graphene_django_optimizer as gql_optimizer

from .sorters import (
    DeviceOrder,
    DeviceOrderField
)

from ..core.utils import (
    sort_queryset
) 

def sort_devices(qs: QuerySet, sort_by: DeviceOrder) -> "QuerySet":
    if sort_by is None:
        return qs
    
    if sort_by.field:
        return sort_queryset(qs, sort_by, DeviceOrderField)

    return qs


def resolve_devices(info, sort_by=None, **_kwargs):
    qs = info.context.user.devices.all()

    qs = sort_devices(qs, sort_by)
    qs = qs.distinct()
    return gql_optimizer.query(qs, info)