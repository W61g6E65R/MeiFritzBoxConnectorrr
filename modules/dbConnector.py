# Imports: global
import logging
from typing import List

# Imports: project specific
import psycopg2

# Imports: local
import modules.globalConstants

g_dbConnection = ''
g_dbCurser = ''

logging.basicConfig(modules.globalConstants.LOGGING_CONFIG_STRING)

def connect(dbName:str, dbUser:str, dbPassword:str, dbHost:str, dbPort:str) -> None:
    """ Connects to the database and store the connection in a global variable

    Args:
        dbName (str): Name of the database
        dbUser (str): User with read/write privileges
        dbPassword (str): Password for dbUser
        dbHost (str): Address of the database
        dbPort (str): Port of the database on dbHost
    """

    global g_dbConnection
    global g_dbConnectionStatus
    global g_dbCurser

    try:
        g_dbConnection = psycopg2.connect(
            database = dbName,
            user = dbUser,
            password = dbPassword,
            host = dbHost,
            port = dbPort
        )
    except:
        logging.error(f"Module dbConnector: Connecting to database FAILED: {dbUser}@{dbHost}:{dbPort}/{dbName}")

    logging.info(f"Module dbConnector: Connected to database: {dbUser}@{dbHost}:{dbPort}/{dbName}")
    g_dbCurser = g_dbConnection.cursor()
    
def checkConnectionStatus() -> None:
    """ Checking if connection is ok

    Returns:
        bool: returns false when not connected
    """
    m_connectionStatus = g_dbConnection.status()

    if(m_connectionStatus == 0):
        try:
            raise RuntimeError('DB-Connection Status')
        except:
            logging.error(f'Module dbConnector: Database connection not established! (Status: {m_connectionStatus})')

def getDeviceList(fritzBoxId:str) -> List:
    """ Read the device list from the database and store it in a list

    Returns:
        List: List with all devices in format identifier, parameterlist
    """
    global g_dbCurser
    m_deviceList = []
    m_sqlStatement = "SELECT identifier, fritzBoxId, readTemperature, readPowerConsumption, readHumidity FROM devicelist"
    checkConnectionStatus()

    g_dbCurser.execute(m_sqlStatement)
    m_rows = g_dbCurser.fetchall()
    for row in m_rows:
        if row[1] == fritzBoxId: # Only add to deviceList when on the same fritzBox
            m_deviceList.append([row[0],row[2], row[3], row[4]])
    
    return m_deviceList

def addValue(timestamp:str, fritzBoxId:str, identifier:str, parametername:str, parametervalue:float) -> None:
    global g_dbCurser
    checkConnectionStatus()

    m_sqlStatement = f"INSERT INTO values (timestamp, sourceFritzBox, identifier,parametername,parametervalue) \
                        VALUES ('{timestamp}', '{fritzBoxId}','{identifier}', '{parametername}', {parametervalue});"
    try:
        g_dbCurser.execute(m_sqlStatement)
        g_dbConnection.commit()
    except:
        logging.error('Module dbConnector: AddValue')


def getLastValue(fritzBoxId:str, identifier:str, parametername:str):
    global g_dbCurser
    m_lastValue = 0.0
    m_sqlStatement = f"SELECT timestamp, parameterValue FROM values \
                        WHERE sourcefritzbox   = '{fritzBoxId}' AND \
                              identifier = '{identifier}' AND \
                              parametername = '{parametername}' \
                        ORDER BY timestamp desc limit 1"
    g_dbCurser.execute(m_sqlStatement)
    m_rows = g_dbCurser.fetchone()
    if m_rows != None:
        m_lastValue = m_rows[1]
    return m_lastValue

def closeConnection():
    global g_dbConnection
    g_dbConnection.close()
    logging.info('Module dbConnector: Closing connection')