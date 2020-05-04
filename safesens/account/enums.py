import graphene

from . import UserRole

class UserRoleEnum(graphene.Enum):
    TECHNICIAN = UserRole.TECHNICIAN
    CONTRACTOR_CUSTOMER = UserRole.CONTRACTOR_CUSTOMER
    CONTRACTOR = UserRole.CONTRACTOR
    KOVCO_STAFF = UserRole.KOVCO_STAFF