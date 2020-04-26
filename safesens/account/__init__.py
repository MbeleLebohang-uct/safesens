class UserRole:
    TECHNICIAN = "technician"  
    CONTRACTOR_CUSTOMER = "contractor_customer"
    CONTRACTOR = "contractor"
    KOVCO_STAFF = "kovco_staff"
    
    CHOICES = [
        (TECHNICIAN, "technician"),
        (CONTRACTOR_CUSTOMER, "contractor customer"),
        (CONTRACTOR, "contractor"),
        (KOVCO_STAFF, "kovco staff"),
    ]
