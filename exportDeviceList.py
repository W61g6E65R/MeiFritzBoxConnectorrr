# Imports
import os
import schedule
import time
import logging
import dotenv
import pandas

# Local imports
import modules.fritzpy

logging.basicConfig(format=modules.globalConstants.LOGGING_CONFIG_FORMAT, level=logging.INFO)

dotenv.load_dotenv()

m_fritzIp = os.environ['FRITZBOX_IP_ADDRESS']
m_fritzUser = os.environ['FRITZBOX_USER_NAME']
m_fritzPass = os.environ['FRITZBOX_USER_PASSWORD']
m_fritzIdent = os.environ['FRITZBOX_IDENTIFIER']
m_exportFile_reduced = os.environ['EXPORT_FILE_REDUCED']
m_exportFile_full = os.environ['EXPORT_FILE_FULL']


# Connect with fritzBox
modules.fritzpy.connect(m_fritzIp, m_fritzUser, m_fritzPass, m_fritzIdent)

m_deviceList = pandas.DataFrame.from_dict(modules.fritzpy.getDeviceList())
m_deviceList_sorted = m_deviceList[['NewAIN', 'NewDeviceName', 'NewPresent',
                                    'NewMultimeterIsEnabled','NewMultimeterIsValid', 'NewMultimeterPower', 'NewMultimeterEnergy',
                                    'NewTemperatureIsEnabled', 'NewTemperatureIsValid', 'NewTemperatureCelsius','NewTemperatureOffset',
                                    'NewSwitchIsEnabled', 'NewSwitchIsValid', 'NewSwitchState', 'NewSwitchMode', 'NewSwitchLock',
                                    'NewHkrIsEnabled', 'NewHkrIsValid', 'NewHkrIsTemperature', 'NewHkrSetVentilStatus', 'NewHkrSetTemperature', 'NewHkrReduceVentilStatus', 'NewHkrReduceTemperature', 'NewHkrComfortVentilStatus', 'NewHkrComfortTemperature']]
m_deviceList.to_json(m_exportFile_full, orient='records', lines=True)
m_deviceList_sorted.to_json(m_exportFile_reduced, orient='records', lines=True)
