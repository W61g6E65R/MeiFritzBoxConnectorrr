# MeiFritzBoxConnectorrr
Get Data from FritzBox (FritzConnection) and write it in a database

## Limitations ##

All given information are only tested with Ubuntu 22.04!

## Preparation

  - **VirtualEnv**
    - <code>python3 -m venv .venv </code>
  - **Docker-Compose**
    - Rename /templates/template.env to /.env
    - Insert credentials in .env file. This file is used in docker-compose

## MessageStructure

{'NewAIN': '13979 0041302', 'NewDeviceId': 19, 'NewFunctionBitMask': 1048864, 'NewFirmwareVersion': '05.25', 'NewManufacturer': 'AVM', 'NewProductName': 'FRITZ!DECT 400', 'NewDeviceName': 'MeiSchalterUnten', 'NewPresent': 'CONNECTED', 'NewMultimeterIsEnabled': 'DISABLED', 'NewMultimeterIsValid': 'INVALID', 'NewMultimeterPower': 0, 'NewMultimeterEnergy': 0, 
'NewTemperatureIsEnabled': 'ENABLED', 'NewTemperatureIsValid': 'VALID', 'NewTemperatureCelsius': 225, 'NewTemperatureOffset': 0, 
'NewSwitchIsEnabled': 'DISABLED', 'NewSwitchIsValid': 'INVALID', 'NewSwitchState': 'OFF', 'NewSwitchMode': 'AUTO', 'NewSwitchLock': False, 
'NewHkrIsEnabled': 'DISABLED', 'NewHkrIsValid': 'INVALID', 'NewHkrIsTemperature': 0, 'NewHkrSetVentilStatus': 'CLOSED', 'NewHkrSetTemperature': 0, 
'NewHkrReduceVentilStatus': 'CLOSED', 'NewHkrReduceTemperature': 0, 'NewHkrComfortVentilStatus': 'CLOSED', 'NewHkrComfortTemperature': 0}