__version__ = 0.9
__author___ = 'Wagner Matthias'

LOGGING_CONFIG_FORMAT   = "%(asctime)s - %(message)s"

FRITZBOX_TIMESTAMP_DELTA_MAX = 60 # Max age of old value, after x minutes the value will be written again, also if DELTA_MIN is not exceeded

FRITZBOX_TEMPERATURE_PARAMETER_NAME     = 'NewTemperatureCelsius'
FRITZBOX_TEMPERATURE_PARAMETER_VALID    = 'NewTemperatureIsValid'
FRITZBOX_TEMPERATURE_PARAMETER_ENABLED  = 'NewTemperatureIsEnabled'
FRITZBOX_TEMPERATURE_PARAMETER_OFFSET   = 'NewTemperatureOffset'
FRITZBOX_TEMPERATURE_DELTA_MIN          = 0.49 # Only write values if delta is reached
FRITZBOX_TEMPERATURE_FACTOR             = 0.1 # Factor for multiplication 

FRITZBOX_HKR_VALVE_STAT_PARAMETER_NAME    = 'NewHkrSetVentilStatus'
FRITZBOX_HKR_TEMP_REDUCED_PARAMETER_NAME = 'NewHkrReduceTemperature'
FRITZBOX_HKR_TEMP_COMFORT_PARAMETER_NAME = 'NewHkrComfortTemperature'
FRITZBOX_HKR_VALID_PARAMETER_NAME        = 'NewHkrIsValid'
FRITZBOX_HKR_ENABLED_PARAMETER_NAME      = 'NewHkrIsEnabled'
FRITZBOX_HKR_TEMP_REDUCED_FACTOR         = 0.1
FRITZBOX_HKR_TEMP_COMFORT_FACTOR         = 0.1

FRITZBOX_POWER_PARAMETER_NAME       = 'NewMultimeterPower'
FRITZBOX_POWER_PARAMETER_VALID      = 'NewMultimeterIsValid'
FRITZBOX_POWER_PARAMETER_ENABLED    = 'NewMultimeterIsEnabled'
FRITZBOX_POWER_DELTA_MIN            = 1 # Only write values if delta is reached
FRITZBOX_POWER_FACTOR               = 0.01 # Factor for multiplication 

