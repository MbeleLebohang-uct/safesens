from enum import IntEnum
from graphql_jwt.utils import jwt_payload

class CustomerTypes(IntEnum):
    TECHNICIAN = 1
    CONTRACTOR_CUSTOMER = 2
    CONTRACTOR = 3
    STAFF = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

def create_jwt_payload(user, context=None):
    payload = jwt_payload(user, context)
    payload["user_type"] = user.user_type
    payload["is_superuser"] = user.is_superuser
    return payload