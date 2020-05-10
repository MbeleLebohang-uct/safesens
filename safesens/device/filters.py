import django_filters

from ..core.types import FilterInputObjectType

from ..core.utils import filter_by_query_param, filter_range_field
from ..core.types.common import DateRangeInput
from ..core.filters import ObjectTypeFilter

from .models import Device


def filter_contract_end_date(qs, _, value):
    return filter_range_field(qs, "contract_end_date__date", value)


def filter_fields_containing_value(*search_fields: str):
    """Create a icontains filters through given fields on a given query set object."""

    def _filter_qs(qs, _, value):
        if value:
            qs = filter_by_query_param(qs, value, search_fields)
        return qs

    return _filter_qs


class DeviceFilter(django_filters.FilterSet):
    contract_end_date = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_contract_end_date
    )
    imei = django_filters.CharFilter(
        method=filter_fields_containing_value("imei")
    )
    
    class Meta:
        model = Device
        fields = [
            "contract_end_date",
            "imei"
        ]

class DeviceFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = DeviceFilter

