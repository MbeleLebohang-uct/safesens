from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_address_1",
        "street_address_2",
        "city",
        "suburb",
        "postal_code",
        "country",
    )