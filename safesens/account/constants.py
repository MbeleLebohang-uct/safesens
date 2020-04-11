from django.utils.translation import gettext as _

class Messages:
    NOT_AUTHENICATED = [{"message": _("User not authenticated."), "code": "permission_denied"}]
    TECHNICIAN_UNAUTHORISED = [{"message": _("Technician not authorized to perform this operation."), "code": "permission_denied"}]
    CONTRACTOR_UNAUTHORISED = [{"message": _("Contractor not authorized to perform this operation."), "code": "permission_denied"}]
    CUSTOMER_UNAUTHORISED = [{"message": _("Customer not authorized to perform this operation."), "code": "permission_denied"}]
    STAFF_UNAUTHORISED = [{"message": _("Staff not authorized to perform this operation."), "code": "permission_denied"}]
    