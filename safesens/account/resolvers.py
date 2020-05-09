from django.db.models import QuerySet
import graphene_django_optimizer as gql_optimizer

from .models import User

from .sorters import (
    UserSortField,
    UserSortingInput,
)

from ..core.utils import (
    filter_by_query_param,
    filter_by_role_param,
    sort_queryset
)

from . import UserRole

USER_SEARCH_FIELDS = (
    "email",
    "first_name",
    "last_name",
    "manager",
)


def sort_users(qs: QuerySet, sort_by: UserSortingInput) -> QuerySet:
    if sort_by:
        return sort_queryset(qs, sort_by, UserSortField)
    return qs.order_by("email")


def resolve_own_technicians(info, query, sort_by=None, **_kwargs):
    qs = User.objects.technicians()
    
    current_user = info.context.user

    qs = filter_by_manager_param(queryset=qs, manager=current_user)

    qs = sort_users(qs, sort_by)
    qs = qs.distinct()
    return gql_optimizer.query(qs, info)


def resolve_own_users(info, query, sort_by=None, **_kwargs):
    current_user = info.context.user
    
    if current_user.role != UserRole.TECHNICIAN:
        qs = info.context.user.user_set.all()

        qs = filter_by_role_param(queryset=qs, role=current_user)

        qs = sort_users(qs, sort_by)
        qs = qs.distinct()
        return gql_optimizer.query(qs, info)
    return None
    
