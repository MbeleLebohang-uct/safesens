import django_filters

from ..core.utils import filter_range_field
from ..core.types.common import DateRangeInput
from ..core.filters import ObjectTypeFilter

from .models import User


def filter_date_joined(qs, _, value):
    return filter_range_field(qs, "date_joined__date", value)


class TechnicianFilter(django_filters.FilterSet):
    date_joined = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_joined
    )
    
    class Meta:
        model = User
        fields = [
            "date_joined",
        ]

        
class UserFilter(django_filters.FilterSet):
    date_joined = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_joined
    )
    
    class Meta:
        model = User
        fields = [
            "date_joined",
        ]