__version__ = 0.9
__author___ = 'Wagner Matthias'

LOGGING_CONFIG_FORMAT   = "%(asctime)s - %(message)s"

FRITZBOX_TIMESTAMP_DELTA_MAX = 60 # Max age of old value, after x minutes the value will be written again, also if DELTA_MIN is not exceeded

FRITZBOX_TEMPERATURE_PARAMETER_NAME     = 'NewTemperatureCelsius'
FRITZBOX_TEMPERATURE_PARAMETER_VALID    = 'NewTemperatureIsValid'
FRITZBOX_TEMPERATURE_PARAMETER_ENABLED  = 'NewTemperatureIsEnabled'
FRITZBOX_TEMPERATURE_PARAMETER_OFFSET   = 'NewTemperatureOffset'
FRITZBOX_TEMPERATURE_DELTA_MIN          = 0.1 # Only write values if delta is reached
FRITZBOX_TEMPERATURE_FACTOR             = 1 # Factor for multiplication 

FRITZBOX_POWER_PARAMETER_NAME       = 'NewMultimeterPower'
FRITZBOX_POWER_PARAMETER_VALID      = 'NewMultimeterIsValid'
FRITZBOX_POWER_PARAMETER_ENABLED    = 'NewMultimeterIsEnabled'
FRITZBOX_POWER_DELTA_MIN            = 1 # Only write values if delta is reached
FRITZBOX_POWER_FACTOR               = 0.01 # Factor for multiplication 

