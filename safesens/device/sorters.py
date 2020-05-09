import graphene

from ..core.types import SortInputObjectType


class DeviceOrderField(graphene.Enum):
    IMEI = "imei"
    CONTRACT_END_DATE = "contract_end_date"

    @property
    def description(self):
        descriptions = {
            DeviceOrderField.IMEI.name: "imei",
            DeviceOrderField.CONTRACT_END_DATE.name: "contract end date",
        }
        if self.name in descriptions:
            return f"Sort devices by {descriptions[self.name]}."
        raise ValueError("Unsupported enum value: %s" % self.value)

class DeviceOrder(SortInputObjectType):
    attribute_id = graphene.Argument(
        graphene.ID,
        description=(
            "Sort devices by the selected attribute's values."
        ),
    )
    field = graphene.Argument(
        DeviceOrderField, description=f"Sort devices by the selected field."
    )