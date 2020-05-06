import graphene

from ..core.types import SortInputObjectType


class UserSortField(graphene.Enum):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"

    @property
    def description(self):
        if self in [
            UserSortField.FIRST_NAME,
            UserSortField.LAST_NAME,
            UserSortField.EMAIL,
        ]:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort users by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class UserSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = UserSortField
        type_name = "users" 