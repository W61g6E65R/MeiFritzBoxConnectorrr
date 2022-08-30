
# Imports: global
import logging
from tkinter.messagebox import NO
from tokenize import Double
import datetime

# Imports: 3rd party
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

# Imports: local
import modules.globalConstants
import modules.dbConnector

# Global var
g_fritzBoxConnection = ''
g_fritzBoxIdentifier = ''

logging.basicConfig(modules.globalConstants.LOGGING_CONFIG_STRING)

def connect(fritzBoxIPAddress, fritzBoxUserName, fritzBoxUserPassword, fritzBoxIdentifier:str='FritzBox') -> None:
        
    global g_fritzBoxConnection
    global g_fritzBoxIdentifier
    g_fritzBoxIdentifier = fritzBoxIdentifier
    g_fritzBoxConnection = FritzHomeAutomation(  
        address=fritzBoxIPAddress, 
                user=fritzBoxUserName, 
                password=fritzBoxUserPassword)

    logging.info(f"Module fritzpy: Connection to {fritzBoxUserName}@{fritzBoxIPAddress} established")

def printDeviceList() -> None:
    """ Read and print the full device list from the FritzBox
    """
    global g_fritzBoxConnection
    info = g_fritzBoxConnection.device_informations()
    logging.info(f"Module fritzpy: Get Device list")
    for key in info:
        print (key)
        print ('/n')

def updateDeviceValues(identifier:str) -> None:

    global g_fritzBoxConnection
    # First read in all configured devices from database
    m_deviceList = modules.dbConnector.getDeviceList()
    m_temperature = None
    m_temperature_old = None
    m_Read_Temperature = False
    m_Read_Power = False
    m_Read_Humidity = False

    # Get all values from the given device from the fritzBox
    for device in m_deviceList:
        m_currentDeviceValues = g_fritzBoxConnection.get_device_information_by_identifier(identifier)
        
        # Read Config from deviceList
        m_Read_Temperature = device[2]
        m_Read_Power = device[3]
        m_Read_Humidity = device[4]

        # Temperature
        if (m_Read_Temperature):
            m_temperature = m_currentDeviceValues[modules.globalConstants.FRITZBOX_PARAMETER_NAME_TEMPERATURE]
            # Check if temperature has changed considerable and then add new value if neccessary
            m_temperature_old = modules.dbConnector.getLastValue(identifier, 
                                                                modules.globalConstants.FRITZBOX_PARAMETER_NAME_TEMPERATURE)
            
            if (abs(m_temperature - m_temperature_old ) > modules.globalConstants.FRITZBOX_TEMPERATURE_DELTA_MIN):
                modules.dbConnector.addValue(datetime.now(), g_fritzBoxIdentifier, identifier,
                                            modules.globalConstants.FRITZBOX_PARAMETER_NAME_TEMPERATURE,
                                            m_temperature)