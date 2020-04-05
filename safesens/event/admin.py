from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "imei",
        "ch1",
        "ch2",
        "ch3",
        "ch4",
        "ch5",
        "battery_voltage",
        "gsm_signal",
        "device_time_date",
        "server_time",
        "device",
    )
