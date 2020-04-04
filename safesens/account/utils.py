from enum import IntEnum

class CustomerTypes(IntEnum):
    TECHNICIAN = 1
    CONTRACTOR_CUSTOMER = 2
    CONTRACTOR = 3
    STAFF = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]