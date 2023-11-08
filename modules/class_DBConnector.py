# import.Global
import logging

# import.Project
import psycopg
import datetime

# import.Local
from modules.class_ConnectionObject import ConnectionObject

class DBConnector:
    """ DB Connection
    """

    def __init__(self, ConnectionObj:ConnectionObject) -> None:
        """ Constructor for DBConnector class

        Args:
            ConnectionObj (ConnectionObject): Connection object with credentials

        Raises:
            RuntimeError: Connection to database fails
        """
        self.log = logging.getLogger(__name__)
        try:
            self.dbConnection = psycopg.connect(
                dbname      = ConnectionObj.identifier,
                user        = ConnectionObj.userName,
                password    = ConnectionObj.password,
                hostaddr    = ConnectionObj.address,
                port        = ConnectionObj.port
            )
            self.dbCursor = self.dbConnection.cursor()

        except Exception as e:
            self.log.error(e)
            self.log.error(f"Connecting to database FAILED: {ConnectionObj.userName}@{ConnectionObj.address}:{ConnectionObj.port}/{ConnectionObj.identifier}")
            raise RuntimeError(f'Runtime Error!')
            return

        self.log.info(f"Connected to database:{ConnectionObj.userName}@{ConnectionObj.address}:{ConnectionObj.port}/{ConnectionObj.identifier}")
    
    def addValue(self, namespace:str, deviceId:str, parameterName:str, value:float, valueoffset:float=0.0)-> None:
        """ Add value to database

        Args:
            namespace (str): Identification of source main device (e.g. FritzBox)
            deviceId (str): Identifiaction of source device (e.g. AVM DECT! Device)
            parameterName (str): Parameter identification
            value (float): Parameter value
            valueoffset (float, optional): Offset to parameter value. Defaults to 0.0.
        """
        timestamp = datetime.datetime.now()
        sqlStatement = f"INSERT INTO devicevalues (timestamp, namespace, deviceid, parametername, value, valueoffset) \
                            VALUES ('{timestamp}', '{namespace}', '{deviceId}', '{parameterName}', {value}, {valueoffset})"
        try:
            self.log.debug(sqlStatement)
            self.dbCursor.execute(sqlStatement)
            self.dbConnection.commit()
        except Exception as e:
            self.log.error(e)

    def getDeviceList(self, namespace:str)-> []:
        """ Get a list of all device of given namespace (e.g. Fritzbox)

        Args:
            namespace (str):  Identification of source main device (e.g. FritzBox)

        Returns:
            []: deviceList
        """
        sqlStatement = f"SELECT namespace, deviceid, alias, active, readtemperature, readpower, readhumidity, readrainfall, cycletime FROM deviceList \
                            WHERE namespace = '{namespace}'"
        deviceList =[]
        try:
            self.dbCursor.execute(sqlStatement)
            deviceList = self.dbCursor.fetchall()
        except Exception as e:
            self.log.error(e)
        return deviceList
    
    def closeConnetion(self) -> None:
        """ Close connection
        """
        self.log.info('Closing db Connection')
        self.dbConnection.close()