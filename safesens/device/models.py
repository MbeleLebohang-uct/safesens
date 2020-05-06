import datetime
from django.db import models
from safesens.account.models import User

from django.utils.translation import gettext_lazy as _, pgettext_lazy

from ..core.permissions import DevicePermissions
from ..core.models import Address


class Device(models.Model):
    imei                        = models.CharField("IMEI", max_length=50, default="")
    contract_end_date           = models.DateField(("contract end date"), default=datetime.date.today)
    sim_phone_number            = models.CharField(("sim card phone number"), max_length=15, default="")
    unit_name                   = models.CharField(("unit name"), max_length=100, default="")
    unit_location               = models.OneToOneField(Address, related_name="unit_location", on_delete=models.CASCADE, blank=True, null=True)
    unit_admin_name             = models.CharField("unit admin name", max_length=50, default="")
    unit_admin_phone_number     = models.CharField("unit admin phone number", max_length=50, default="")
    
    ch1_on                      = models.BooleanField(("channel1 on"), default=False)
    ch2_on                      = models.BooleanField(("channel2 on"), default=False)
    ch3_on                      = models.BooleanField(("channel3 on"), default=False)
    ch4_on                      = models.BooleanField(("channel4 on"), default=False)
    ch5_on                      = models.BooleanField(("channel5 on"), default=False)

    ch1_name                    = models.CharField(("channel1 name"), max_length=100, default="")
    ch2_name                    = models.CharField(("channel2 name"), max_length=100, default="")
    ch3_name                    = models.CharField(("channel3 name"), max_length=100, default="")
    ch4_name                    = models.CharField(("channel4 name"), max_length=100, default="")
    ch5_name                    = models.CharField(("channel5 name"), max_length=100, default="")

    ch1_sensor_type             = models.CharField(("channel1 sensor type"), max_length=100, default="")
    ch2_sensor_type             = models.CharField(("channel2 sensor type"), max_length=100, default="")
    ch3_sensor_type             = models.CharField(("channel3 sensor type"), max_length=100, default="")
    ch4_sensor_type             = models.CharField(("channel4 sensor type"), max_length=100, default="")
    ch5_sensor_type             = models.CharField(("channel5 sensor type"), max_length=100, default="")

    scale_factor_ch1            = models.FloatField(("channel1 scale factor"), default=0.0)
    scale_factor_ch2            = models.FloatField(("channel2 scale factor"), default=0.0)
    scale_factor_ch3            = models.FloatField(("channel3 scale factor"), default=0.0)
    scale_factor_ch4            = models.FloatField(("channel4 scale factor"), default=0.0)
    scale_factor_ch5            = models.FloatField(("channel5 scale factor"), default=0.0)

    zero_offset_ch1             = models.FloatField(("channel1 zero offset"), default=0.0)
    zero_offset_ch2             = models.FloatField(("channel2 zero offset"), default=0.0)
    zero_offset_ch3             = models.FloatField(("channel3 zero offset"), default=0.0)
    zero_offset_ch4             = models.FloatField(("channel4 zero offset"), default=0.0)
    zero_offset_ch5             = models.FloatField(("channel5 zero offset"), default=0.0)

    units_ch1                   = models.CharField(("channel1 units"), max_length=50, default="")
    units_ch2                   = models.CharField(("channel2 units"), max_length=50, default="")
    units_ch3                   = models.CharField(("channel3 units"), max_length=50, default="")
    units_ch4                   = models.CharField(("channel4 units"), max_length=50, default="")
    units_ch5                   = models.CharField(("channel5 units"), max_length=50, default="")

    upper_threshold_ch1         = models.FloatField(("channel1 upper threshold"), default=0.0)
    upper_threshold_ch2         = models.FloatField(("channel2 upper threshold"), default=0.0)
    upper_threshold_ch3         = models.FloatField(("channel3 upper threshold"), default=0.0)
    upper_threshold_ch4         = models.FloatField(("channel4 upper threshold"), default=0.0)
    upper_threshold_ch5         = models.FloatField(("channel5 upper threshold"), default=0.0)

    lower_threshold_ch1         = models.FloatField(("channel1 lower threshold"), default=0.0)
    lower_threshold_ch2         = models.FloatField(("channel2 lower threshold"), default=0.0)
    lower_threshold_ch3         = models.FloatField(("channel3 lower threshold"), default=0.0)
    lower_threshold_ch4         = models.FloatField(("channel4 lower threshold"), default=0.0)
    lower_threshold_ch5         = models.FloatField(("channel5 lower threshold"), default=0.0)

    monitoring_active_ch1       = models.BooleanField(("monitoring active channel1"), default=False)
    monitoring_active_ch2       = models.BooleanField(("monitoring active channel2"), default=False)
    monitoring_active_ch3       = models.BooleanField(("monitoring active channel3"), default=False)
    monitoring_active_ch4       = models.BooleanField(("monitoring active channel4"), default=False)
    monitoring_active_ch5       = models.BooleanField(("monitoring active channel5"), default=False)

    alert_email                 = models.EmailField(("alert email"), max_length=100, default="")

    alert_state_ch1             = models.BooleanField(("channel1 alert state"), default=False)
    alert_state_ch2             = models.BooleanField(("channel2 alert state"), default=False)
    alert_state_ch3             = models.BooleanField(("channel3 alert state"), default=False)
    alert_state_ch4             = models.BooleanField(("channel4 alert state"), default=False)
    alert_state_ch5             = models.BooleanField(("channel5 alert state"), default=False)

    ch1_masks_alerts             = models.BooleanField(("channel1 masks alerts"), default=False)
    ch2_masks_alerts             = models.BooleanField(("channel2 masks alerts"), default=False)
    ch3_masks_alerts             = models.BooleanField(("channel3 masks alerts"), default=False)
    ch4_masks_alerts             = models.BooleanField(("channel4 masks alerts"), default=False)
    ch5_masks_alerts             = models.BooleanField(("channel5 masks alerts"), default=False)

    heartbeat_monitoring_active  = models.BooleanField(("heartbeat monitor state"), default=False)
    heartbeat_monitor_state      = models.BooleanField(("heartbeat monitor state"), default=False)
    allowable_offline_minutes    = models.IntegerField(("allowable offline minutes"), default=0)

    users                        = models.ManyToManyField(User, related_name="devices")

    def __str__(self):
        return self.imei

    class Meta:
        app_label = "device"
        ordering = ("unit_name",)
        permissions = (
            (
                DevicePermissions.MANAGE_DEVICES.codename,
                pgettext_lazy("Permission description", "Manage devices."),
            ),
        )