# Generated by Django 3.0.5 on 2020-04-04 13:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('device', '0002_auto_20200404_1341'),
        ('event', '0002_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(default='', max_length=50, verbose_name='IMEI')),
                ('ch1', models.FloatField(default=0.0, verbose_name='Channel 1 reading')),
                ('ch2', models.FloatField(default=0.0, verbose_name='Channel 2 reading')),
                ('ch3', models.FloatField(default=0.0, verbose_name='Channel 3 reading')),
                ('ch4', models.FloatField(default=0.0, verbose_name='Channel 4 reading')),
                ('ch5', models.FloatField(default=0.0, verbose_name='Channel 5 reading')),
                ('battery_voltage', models.FloatField(default=0.0, verbose_name='Battery voltage reading')),
                ('gsm_signal', models.IntegerField(default=0, verbose_name='GSM signal')),
                ('device_time_date', models.DateTimeField(default=datetime.date.today, verbose_name='contract end date')),
                ('server_time', models.IntegerField(default=0, verbose_name='GSM signal')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.Device')),
            ],
        ),
    ]
