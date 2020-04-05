import datetime
from django.db import models
from safesens.device.models import Device

class Event(models.Model):
    imei                        = models.CharField("IMEI", max_length=50, default="")
    ch1                         = models.FloatField(("Channel 1 reading"), default=0.0)
    ch2                         = models.FloatField(("Channel 2 reading"), default=0.0)
    ch3                         = models.FloatField(("Channel 3 reading"), default=0.0)
    ch4                         = models.FloatField(("Channel 4 reading"), default=0.0)
    ch5                         = models.FloatField(("Channel 5 reading"), default=0.0)
    battery_voltage             = models.FloatField(("Battery voltage reading"), default=0.0)
    gsm_signal                  = models.IntegerField(("GSM signal"), default=0)
    device_time_date            = models.DateTimeField(("contract end date"), auto_now_add=True)
    server_time                 = models.IntegerField(("GSM signal"), default=0)
    device                      = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        app_label = "event"
        ordering = ("imei","device_time_date",)