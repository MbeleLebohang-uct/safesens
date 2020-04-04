# Generated by Django 3.0.5 on 2020-04-04 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(default='', max_length=50, verbose_name='IMEI')),
                ('contract_end_date', models.DateField(default=datetime.date.today, verbose_name='contract end date')),
                ('sim_phone_number', models.CharField(default='', max_length=15, verbose_name='sim card phone number')),
                ('unit_name', models.CharField(default='', max_length=100, verbose_name='unit name')),
                ('unit_location', models.TextField(default='', verbose_name='unit location')),
                ('unit_admin_name', models.CharField(default='', max_length=50, verbose_name='unit admin name')),
                ('unit_admin_phone_number', models.CharField(default='', max_length=50, verbose_name='unit admin phone number')),
                ('ch1_on', models.BooleanField(default=False, verbose_name='channel1 on')),
                ('ch2_on', models.BooleanField(default=False, verbose_name='channel2 on')),
                ('ch3_on', models.BooleanField(default=False, verbose_name='channel3 on')),
                ('ch4_on', models.BooleanField(default=False, verbose_name='channel4 on')),
                ('ch5_on', models.BooleanField(default=False, verbose_name='channel5 on')),
                ('ch1_name', models.CharField(default='', max_length=100, verbose_name='channel1 name')),
                ('ch2_name', models.CharField(default='', max_length=100, verbose_name='channel2 name')),
                ('ch3_name', models.CharField(default='', max_length=100, verbose_name='channel3 name')),
                ('ch4_name', models.CharField(default='', max_length=100, verbose_name='channel4 name')),
                ('ch5_name', models.CharField(default='', max_length=100, verbose_name='channel5 name')),
                ('ch1_sensor_type', models.CharField(default='', max_length=100, verbose_name='channel1 sensor type')),
                ('ch2_sensor_type', models.CharField(default='', max_length=100, verbose_name='channel2 sensor type')),
                ('ch3_sensor_type', models.CharField(default='', max_length=100, verbose_name='channel3 sensor type')),
                ('ch4_sensor_type', models.CharField(default='', max_length=100, verbose_name='channel4 sensor type')),
                ('ch5_sensor_type', models.CharField(default='', max_length=100, verbose_name='channel5 sensor type')),
                ('scale_factor_ch1', models.FloatField(default=0.0, verbose_name='channel1 scale factor')),
                ('scale_factor_ch2', models.FloatField(default=0.0, verbose_name='channel2 scale factor')),
                ('scale_factor_ch3', models.FloatField(default=0.0, verbose_name='channel3 scale factor')),
                ('scale_factor_ch4', models.FloatField(default=0.0, verbose_name='channel4 scale factor')),
                ('scale_factor_ch5', models.FloatField(default=0.0, verbose_name='channel5 scale factor')),
                ('zero_offset_ch1', models.FloatField(default=0.0, verbose_name='channel1 zero offset')),
                ('zero_offset_ch2', models.FloatField(default=0.0, verbose_name='channel2 zero offset')),
                ('zero_offset_ch3', models.FloatField(default=0.0, verbose_name='channel3 zero offset')),
                ('zero_offset_ch4', models.FloatField(default=0.0, verbose_name='channel4 zero offset')),
                ('zero_offset_ch5', models.FloatField(default=0.0, verbose_name='channel5 zero offset')),
                ('units_ch1', models.CharField(default='', max_length=50, verbose_name='channel1 units')),
                ('units_ch2', models.CharField(default='', max_length=50, verbose_name='channel2 units')),
                ('units_ch3', models.CharField(default='', max_length=50, verbose_name='channel3 units')),
                ('units_ch4', models.CharField(default='', max_length=50, verbose_name='channel4 units')),
                ('units_ch5', models.CharField(default='', max_length=50, verbose_name='channel5 units')),
                ('upper_threshold_ch1', models.FloatField(default=0.0, verbose_name='channel1 upper threshold')),
                ('upper_threshold_ch2', models.FloatField(default=0.0, verbose_name='channel2 upper threshold')),
                ('upper_threshold_ch3', models.FloatField(default=0.0, verbose_name='channel3 upper threshold')),
                ('upper_threshold_ch4', models.FloatField(default=0.0, verbose_name='channel4 upper threshold')),
                ('upper_threshold_ch5', models.FloatField(default=0.0, verbose_name='channel5 upper threshold')),
                ('lower_threshold_ch1', models.FloatField(default=0.0, verbose_name='channel1 lower threshold')),
                ('lower_threshold_ch2', models.FloatField(default=0.0, verbose_name='channel2 lower threshold')),
                ('lower_threshold_ch3', models.FloatField(default=0.0, verbose_name='channel3 lower threshold')),
                ('lower_threshold_ch4', models.FloatField(default=0.0, verbose_name='channel4 lower threshold')),
                ('lower_threshold_ch5', models.FloatField(default=0.0, verbose_name='channel5 lower threshold')),
                ('monitoring_active_ch1', models.BooleanField(default=False, verbose_name='monitoring active channel1')),
                ('monitoring_active_ch2', models.BooleanField(default=False, verbose_name='monitoring active channel2')),
                ('monitoring_active_ch3', models.BooleanField(default=False, verbose_name='monitoring active channel3')),
                ('monitoring_active_ch4', models.BooleanField(default=False, verbose_name='monitoring active channel4')),
                ('monitoring_active_ch5', models.BooleanField(default=False, verbose_name='monitoring active channel5')),
                ('alert_email', models.EmailField(default='', max_length=100, verbose_name='alert email')),
                ('alert_state_ch1', models.BooleanField(default=False, verbose_name='channel1 alert state')),
                ('alert_state_ch2', models.BooleanField(default=False, verbose_name='channel2 alert state')),
                ('alert_state_ch3', models.BooleanField(default=False, verbose_name='channel3 alert state')),
                ('alert_state_ch4', models.BooleanField(default=False, verbose_name='channel4 alert state')),
                ('alert_state_ch5', models.BooleanField(default=False, verbose_name='channel5 alert state')),
                ('ch1_masks_alerts', models.BooleanField(default=False, verbose_name='channel1 masks alerts')),
                ('ch2_masks_alerts', models.BooleanField(default=False, verbose_name='channel2 masks alerts')),
                ('ch3_masks_alerts', models.BooleanField(default=False, verbose_name='channel3 masks alerts')),
                ('ch4_masks_alerts', models.BooleanField(default=False, verbose_name='channel4 masks alerts')),
                ('ch5_masks_alerts', models.BooleanField(default=False, verbose_name='channel5 masks alerts')),
                ('heartbeat_monitoring_active', models.BooleanField(default=False, verbose_name='heartbeat monitor state')),
                ('heartbeat_monitor_state', models.BooleanField(default=False, verbose_name='heartbeat monitor state')),
                ('allowable_offline_minutes', models.IntegerField(default=0, verbose_name='allowable offline minutes')),
            ],
            options={
                'ordering': ('imei', 'unit_name'),
                'permissions': (('manage_devices', 'Manage devices.'),),
            },
        ),
    ]
