
# Imports: global
import logging
import datetime

# Imports: 3rd party
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzstatus import FritzStatus
from fritzconnection.lib.fritzwlan import FritzWLAN

# Imports: local
import modules.globalConstants
import modules.dbConnector

# Global var
g_fritzBoxHomeAutomation = ''
g_fritzBoxStatus = ''
g_fritzBoxIdentifier = ''
g_dbDeviceList = []

logging.basicConfig(format=modules.globalConstants.LOGGING_CONFIG_FORMAT, level=logging.INFO)

def connect(fritzBoxIPAddress:str, fritzBoxUserName:str, fritzBoxUserPassword:str, fritzBoxIdentifier:str='FritzBox') -> None:
    """ Connect to the fritzBox and store connecction in global var

    Args:
        fritzBoxIPAddress (str): _description_
        fritzBoxUserName (str): _description_
        fritzBoxUserPassword (str): _description_
        fritzBoxIdentifier (str, optional): _description_. Defaults to 'FritzBox'.
    """
    global g_fritzBoxHomeAutomation
    global g_fritzBoxIdentifier    
    global g_fritzBoxStatus

    g_fritzBoxIdentifier = fritzBoxIdentifier
    g_fritzBoxHomeAutomation = FritzHomeAutomation(  
                address=fritzBoxIPAddress, 
                user=fritzBoxUserName, 
                password=fritzBoxUserPassword)

    g_fritzBoxStatus = FritzStatus(
                address=fritzBoxIPAddress, 
                user=fritzBoxUserName, 
                password=fritzBoxUserPassword)

    logging.info(f"Module fritzpy: Connection to {fritzBoxUserName}@{fritzBoxIPAddress} established")

    # First read in all configured devices from database
    updateDeviceList(fritzBoxIdentifier)

def updateDeviceList(fritzBoxIdentifier:str) -> None:
    """_summary_
        Read in the deviceList from the choosen FritzBox from the database
    Args:
        fritzBoxIdentifier (str): _description_
    """
    global g_dbDeviceList
    g_dbDeviceList = modules.dbConnector.getDeviceList(fritzBoxIdentifier)

def printDeviceList() -> None:
    """ Read and print the full device list from the FritzBox
    """
    global g_fritzBoxHomeAutomation
    info = g_fritzBoxHomeAutomation.device_informations()
    logging.info(f"Module fritzpy: Get Device list")
    for key in info:
        print (key)
        print ('/n')

def updateHomeAutomationDeviceValues(fritzboxId:str) -> None:
    """ Read values for all devices in database from FritzBox and update if neccessary

    Args:
        identifier (str): Identifier of the fritzBox
    """
    global g_fritzBoxHomeAutomation
    global g_dbDeviceList

    # Get all values from the given device from the fritzBox
    for device in g_dbDeviceList:
        # Read Config from deviceList
        m_DeviceIdentifier = device[0]
        m_DeviceActive     = device[5]
        m_Read_Temperature = device[1]
        m_Read_Power = device[2]
        #m_Read_Humidity = device[4]

        if (m_Read_Temperature == True and m_DeviceActive == True):
            updateValue(fritzboxId, m_DeviceIdentifier, 
                        modules.globalConstants.FRITZBOX_TEMPERATURE_PARAMETER_NAME, modules.globalConstants.FRITZBOX_TEMPERATURE_DELTA_MIN, 
                        modules.globalConstants.FRITZBOX_TEMPERATURE_PARAMETER_ENABLED, modules.globalConstants.FRITZBOX_TEMPERATURE_PARAMETER_VALID, 
                        modules.globalConstants.FRITZBOX_TEMPERATURE_FACTOR, modules.globalConstants.FRITZBOX_TEMPERATURE_PARAMETER_OFFSET)

        if (m_Read_Power == True and m_DeviceActive == True):
            updateValue(fritzboxId, m_DeviceIdentifier, 
                        modules.globalConstants.FRITZBOX_POWER_PARAMETER_NAME, modules.globalConstants.FRITZBOX_POWER_DELTA_MIN, 
                        modules.globalConstants.FRITZBOX_POWER_PARAMETER_ENABLED, modules.globalConstants.FRITZBOX_POWER_PARAMETER_VALID, 
                        modules.globalConstants.FRITZBOX_POWER_FACTOR)
        

def updateValue(fritzBoxId:str, deviceIdentifier:str, paraName:str, paraMinDelta:float, paraEnableTag:str, paraValidTag:str, paraFactor:float = 1.0, paraOffsetTag:str = '') -> None:                  
    
    # Read parameter from fritzBox
    try:
        m_currentDeviceValues = g_fritzBoxHomeAutomation.get_device_information_by_identifier(deviceIdentifier)
    except Exception as e:
        logging.error(f'ERROR: Module fritzpy: {deviceIdentifier}@{fritzBoxId}')
        logging.error(e)

    m_currValue = m_currentDeviceValues[paraName] * paraFactor
    m_valid = m_currentDeviceValues[paraValidTag]
    m_enabled = m_currentDeviceValues[paraEnableTag]

    if (paraOffsetTag != ''):
        paraOffset = m_currentDeviceValues[paraOffsetTag]
    else:
        paraOffset = 0.0
    
    writeValue(fritzBoxId, deviceIdentifier, paraName, m_currValue, paraMinDelta, paraOffset, m_valid, m_enabled)

def updateConnectionStatus(fritzBoxId:str):
    global g_fritzBoxStatus
    m_transmissionRate = g_fritzBoxStatus.transmission_rate
    m_maxRate = g_fritzBoxStatus.max_linked_bit_rate
    m_isConnected = 0.0
    m_isLinked = 0.0
    m_FactorBitMbit = 0.000001
    if g_fritzBoxStatus.is_connected:
        m_isConnected = 1.0
    if g_fritzBoxStatus.is_linked:
        m_isLinked = 1.0

    writeValue(fritzBoxId, '1', 'transmission_rate_upload', m_transmissionRate[0] * m_FactorBitMbit )
    writeValue(fritzBoxId, '1', 'transmission_rate_download', m_transmissionRate[1] * m_FactorBitMbit )
    writeValue(fritzBoxId, '1', 'max_rate_upload', m_maxRate[0]  * m_FactorBitMbit)
    writeValue(fritzBoxId, '1', 'max_rate_download', m_maxRate[1] * m_FactorBitMbit)
    writeValue(fritzBoxId, '1', 'isConnected', m_isConnected)
    writeValue(fritzBoxId, '1', 'isLinked', m_isLinked)

def writeValue(fritzBoxId:str, deviceIdentifier:str, paraName:str, currValue:float, 
                paraMinDelta:float = 0.0, paraOffset:float = 0.0, 
                valid:str = 'VALID', enabled:str = 'ENABLED'):

    m_timestamp = datetime.datetime.now()
    # Check if parameter has changed considerable and then add new value if neccessary
    m_oldEntry = modules.dbConnector.getLastValue(fritzBoxId, deviceIdentifier , paraName)
    m_oldTimestamp = m_oldEntry[0]
    m_oldValue = m_oldEntry[1]
    m_timeDiff = (m_timestamp.microsecond - m_oldTimestamp.microsecond) / 60000 # Convert to seconds
    
    if valid == 'VALID' and enabled == 'ENABLED':
        if ((abs(currValue - m_oldValue ) > paraMinDelta) or (m_timeDiff > modules.globalConstants.FRITZBOX_TIMESTAMP_DELTA_MAX)): 
            modules.dbConnector.addValue(
                                        str(m_timestamp), g_fritzBoxIdentifier, deviceIdentifier,
                                        paraName, currValue, paraOffset
                                        )
            logging.info(f'Module fritzPy: Updating Parameter {paraName}. [{deviceIdentifier}: {m_oldValue} -> {currValue} +- {paraOffset}] / Time since last update [min]: {m_timeDiff}')
        else:
            logging.info(f'Module fritzPy: Parameter {paraName} not changed. [{deviceIdentifier}: {m_oldValue} = {currValue}]')
    else:
        logging.info(f'Module fritzPy Parameter {paraName} on device {deviceIdentifier} not accessible: [Enabled: {enabled} / Valid {valid}]')