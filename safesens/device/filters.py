import django_filters

from ..core.types import FilterInputObjectType

from ..core.utils import filter_range_field
from ..core.types.common import DateRangeInput
from ..core.filters import ObjectTypeFilter

from .models import Device


def filter_contract_end_date(qs, _, value):
    return filter_range_field(qs, "contract_end_date__date", value)


class DeviceFilter(django_filters.FilterSet):
    contract_end_date = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_contract_end_date
    )
    
    class Meta:
        model = Device
        fields = [
            "contract_end_date",
        ]

class DeviceFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = DeviceFilter

