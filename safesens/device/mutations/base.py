import graphene

class DeviceInput(graphene.InputObjectType):
    sim_phone_number = graphene.String(description="Device sim card phone number.")
    unit_name = graphene.String(description="Device name")
    unit_admin_name = graphene.String(description="The name of the admin user for this device.")
    unit_admin_phone_number = graphene.String(description="The phone number of the admin user for this device.")

    ch1_on = graphene.Boolean(description="Determine if channel 1 is on.")
    ch2_on = graphene.Boolean(description="Determine if channel 2 is on.")
    ch3_on = graphene.Boolean(description="Determine if channel 3 is on.")
    ch4_on = graphene.Boolean(description="Determine if channel 4 is on.")
    ch5_on = graphene.Boolean(description="Determine if channel 5 is on.")

    ch1_name = graphene.String(description="The name of channel 1.")
    ch2_name = graphene.String(description="The name of channel 2.")
    ch3_name = graphene.String(description="The name of channel 3.")
    ch4_name = graphene.String(description="The name of channel 4.")
    ch5_name = graphene.String(description="The name of channel 5.")

    ch1_sensor_type = graphene.String(description="The type of a sensor on channel 1.")
    ch2_sensor_type = graphene.String(description="The type of a sensor on channel 2.")
    ch3_sensor_type = graphene.String(description="The type of a sensor on channel 3.")
    ch4_sensor_type = graphene.String(description="The type of a sensor on channel 4.")
    ch5_sensor_type = graphene.String(description="The type of a sensor on channel 5.")

    scale_factor_ch1 = graphene.Float(description="Scale factor for channel 1")
    scale_factor_ch2 = graphene.Float(description="Scale factor for channel 2")
    scale_factor_ch3 = graphene.Float(description="Scale factor for channel 3")
    scale_factor_ch4 = graphene.Float(description="Scale factor for channel 4")
    scale_factor_ch5 = graphene.Float(description="Scale factor for channel 5")

    zero_offset_ch1 = graphene.Float(description="Zero offset value for channel 1")
    zero_offset_ch2 = graphene.Float(description="Zero offset value for channel 2")
    zero_offset_ch3 = graphene.Float(description="Zero offset value for channel 3")
    zero_offset_ch4 = graphene.Float(description="Zero offset value for channel 4")
    zero_offset_ch5 = graphene.Float(description="Zero offset value for channel 5")

    units_ch1 = graphene.String(description="The unit name for channel 1. Volts(V), Amps(A), etc")
    units_ch2 = graphene.String(description="The unit name for channel 2. Volts(V), Amps(A), etc")
    units_ch3 = graphene.String(description="The unit name for channel 3. Volts(V), Amps(A), etc")
    units_ch4 = graphene.String(description="The unit name for channel 4. Volts(V), Amps(A), etc")
    units_ch5 = graphene.String(description="The unit name for channel 5. Volts(V), Amps(A), etc")

    upper_threshold_ch1 = graphene.Float(description="The upper threshold for channel 1.")
    upper_threshold_ch2 = graphene.Float(description="The upper threshold for channel 2.")
    upper_threshold_ch3 = graphene.Float(description="The upper threshold for channel 3.")
    upper_threshold_ch4 = graphene.Float(description="The upper threshold for channel 4.")
    upper_threshold_ch5 = graphene.Float(description="The upper threshold for channel 5.")

    lower_threshold_ch1 = graphene.Float(description="The lower threshold for channel 1.")
    lower_threshold_ch2 = graphene.Float(description="The lower threshold for channel 2.")
    lower_threshold_ch3 = graphene.Float(description="The lower threshold for channel 3.")
    lower_threshold_ch4 = graphene.Float(description="The lower threshold for channel 4.")
    lower_threshold_ch5 = graphene.Float(description="The lower threshold for channel 5.")

    monitoring_active_ch1 = graphene.Boolean(description="Determine if channel 1 is actively being monitored.")
    monitoring_active_ch2 = graphene.Boolean(description="Determine if channel 2 is actively being monitored.")
    monitoring_active_ch3 = graphene.Boolean(description="Determine if channel 3 is actively being monitored.")
    monitoring_active_ch4 = graphene.Boolean(description="Determine if channel 4 is actively being monitored.")
    monitoring_active_ch5 = graphene.Boolean(description="Determine if channel 5 is actively being monitored.")

    alert_email = graphene.String(description="The emails address to send all the alerts of this devices to.")

    alert_state_ch1 = graphene.Boolean(description="Determine if channel 1 is is in alert state.")
    alert_state_ch2 = graphene.Boolean(description="Determine if channel 2 is is in alert state.")
    alert_state_ch3 = graphene.Boolean(description="Determine if channel 3 is is in alert state.")
    alert_state_ch4 = graphene.Boolean(description="Determine if channel 4 is is in alert state.")
    alert_state_ch5 = graphene.Boolean(description="Determine if channel 5 is is in alert state.")

    ch1_masks_alerts = graphene.Boolean(description="Determine if channel 1 alerts should be ignored.")
    ch2_masks_alerts = graphene.Boolean(description="Determine if channel 2 alerts should be ignored.")
    ch3_masks_alerts = graphene.Boolean(description="Determine if channel 3 alerts should be ignored.")
    ch4_masks_alerts = graphene.Boolean(description="Determine if channel 4 alerts should be ignored.")
    ch5_masks_alerts = graphene.Boolean(description="Determine if channel 5 alerts should be ignored.")

    heartbeat_monitoring_active = graphene.Boolean(description="Determine if the device heartbeat monitoring is active.")
    heartbeat_monitor_state = graphene.Boolean(description="Determine if the device heartbeat monitoring state.")
    
    allowable_offline_minutes = graphene.Int(description="The number of minutes the devices is allowed to be offline.")
