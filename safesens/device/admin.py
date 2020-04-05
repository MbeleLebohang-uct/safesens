from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("imei",
                    "contract_end_date",
                    "sim_phone_number",
                    "unit_name",
                    "unit_location",
                    "unit_admin_name",
                    "unit_admin_phone_number",
                    "ch1_on",
                    "ch2_on",
                    "ch3_on",
                    "ch4_on",
                    "ch5_on",)
    