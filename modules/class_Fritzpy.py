# import.global
import logging

# import.project
import json
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzstatus import FritzStatus
from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.core.exceptions import *

# import.local
from modules.class_ConnectionObject import ConnectionObject
from modules.class_DBConnector import DBConnector

class FritzPy:
    """ Class for interacting with FritzBox
    """

    def __init__(self, fritzbox:ConnectionObject, database:ConnectionObject) -> None:
        """ Constructor for class FritzPy

        Args:
            fritzbox (ConnectionObject): Connection string for FritzBox
            database (ConnectionObject): Connection string for database

        Raises:
            RuntimeError: _description_
        """
        self.log = logging.getLogger(__name__)
        self.deviceConfig = []
        self.identifier = fritzbox.identifier
        self.log.info(f'Try to connect to Fritzbox[{self.identifier}] {fritzbox.userName}@{fritzbox.address}')
        try:
            self.fritzbox_homeAutomation = FritzHomeAutomation(
                address = fritzbox.address,
                user    = fritzbox.userName,
                password= fritzbox.password
            )
            self.fritzbox_status = FritzStatus(
                address = fritzbox.address,
                user    = fritzbox.address,
                password= fritzbox.password
            )
            self.dbObject = DBConnector(database)

        except Exception as e:
            self.log.error(e)
            raise RuntimeError
        self.log.info('Success')
        self.updateInternalDeviceList()


    def updateInternalDeviceList(self) -> None:
        """ Get device list from database and write it to internal object
        """
        deviceList = self.dbObject.getDeviceList(self.identifier)
        self.log.info(f'Updating internal deviceList for {self.identifier}')
        for device in deviceList:
            deviceConfig = {'id':device[1], 'name':device[2], 'active':device[3],
                            'readTemperature':device[4],
                            'readPower':device[5],
                            'readHumidity': device[6],
                            'readRainfall': device[7],
                            'cycleTime': device[8] }
            self.log.info(deviceConfig)
            self.deviceConfig.append(deviceConfig)
        

    def exportDeviceList(self, file:str) -> None:
        """ Export device list to file

        Args:
            file (str): File and path name
        """
        self.log.info(f'Export device list to {file}')
        device_info = self.fritzbox_homeAutomation.device_information()
        
        try:
            fileObject = open(file, "w")
            for line in device_info:
                fileObject.writelines(json.dumps(line)+'\n')
        except IOError as e:
            self.log.error(e)
        
        fileObject.close()

    def updateDeviceValues(self, deviceId:str) -> None:
        """ Update all values from given device

        Args:
            deviceId (str): Device Id to read parameters from
        """
        self.log.info(f'Updating device values {self.identifier}.{deviceId}')
        for device in self.deviceConfig:
            if (device['id'] == deviceId) and (device['active'] == True):
                try:
                    deviceValues = self.fritzbox_homeAutomation.get_device_information_by_identifier(device['id'])
                except Exception as e:
                    self.log.error(f"Error getting data from device:{device['id']}")
                    self.log.error(e)
                    break

                if (deviceValues['NewPresent']=='CONNECTED') and (deviceValues['NewDeviceName'] == device['name']):
                    if device['readTemperature'] and deviceValues['NewTemperatureIsValid'] == 'VALID':
                        temperature = float(deviceValues['NewTemperatureCelsius'])/10.0
                        self.dbObject.addValue(self.identifier,device['id'],'temperature',temperature, deviceValues['NewTemperatureOffset'])
                    
                    if (device['readPower']) and (deviceValues['NewMultimeterIsValid']=='VALID'):
                        power = float(deviceValues['NewMultimeterPower'])/100.0
                        self.dbObject.addValue(self.identifier,device['id'],'power',power, 0.0)

                elif deviceValues['NewPresent']!='CONNECTED':
                    self.log(f"Device {device['id']} not connected")
                elif deviceValues['NewDeviceName'] == device['name']:
                    self.log(f"Device {device['id']} name does not match id")
                        
