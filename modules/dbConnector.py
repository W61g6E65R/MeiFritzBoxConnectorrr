# Imports: global
import errno
import logging
import datetime
from xmlrpc.client import boolean

# Imports: project specific
import psycopg

# Imports: local
import modules.globalConstants

g_dbConnection = ''

logging.basicConfig(format=modules.globalConstants.LOGGING_CONFIG_FORMAT, level=logging.INFO)

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

    try:
        g_dbConnection = psycopg.connect(
            dbname = dbName,
            user = dbUser,
            password = dbPassword,
            hostaddr = dbHost,
            port = dbPort
        )
    except Exception as e:
        logging.error(e)
        logging.error(f"Module dbConnector: Connecting to database FAILED: {dbUser}@{dbHost}:{dbPort}/{dbName}")
        return

    logging.info(f"Module dbConnector: Connected to database: {dbUser}@{dbHost}:{dbPort}/{dbName}")
    
    
def checkConnectionStatus() -> None:
    """ Checking if connection is ok

    Returns:
        bool: returns false when not connected
    """
    m_connectionStatus = 1 #g_dbConnection.status TODO Upgrade to psycopg 3

    if(m_connectionStatus == 0):
        try:
            raise RuntimeError('DB-Connection Status')
        except:
            logging.error(f'Module dbConnector: Database connection not established! (Status: {m_connectionStatus})')

def getDeviceList(fritzBoxId:str) -> list:
    """ Read the device list from the database and store it in a list

    Returns:
        List: List with all devices in format identifier, parameterlist
    """
    global g_dbConnection
    m_deviceList = []
    m_sqlStatement = "SELECT identifier, fritzboxid, readtemperature, readpowerconsumption, readhumidity, active FROM devicelist"
    checkConnectionStatus()
    m_dbCursor = g_dbConnection.cursor()

    logging.info('Module dbConnector: Reading in deviceList from DB')
    m_dbCursor.execute(m_sqlStatement)
    m_rows = m_dbCursor.fetchall()
    for row in m_rows:
        if row[1] == fritzBoxId: # Only add to deviceList when on the same fritzBox
            m_deviceList.append([row[0],row[2], row[3], row[4], row[4], row[5]])
    if(len(m_deviceList) == 0):
        try:
            raise RuntimeError(f'DB-Plausibility Check')
        except:
            logging.error(f'Module dbConnector: No device in deviceList for fritzBoxId {fritzBoxId}')
            return
    g_dbConnection.commit()
    return m_deviceList

def addValue(timestamp:str, fritzBoxId:str, identifier:str, 
                parametername:str, parametervalue:float, 
                offset:float = 0.0, isautocomplete:bool = False ) -> None:
    global g_dbConnection
    checkConnectionStatus()
    m_dbCursor = g_dbConnection.cursor()
    m_sqlStatement = f"INSERT INTO values_float (timestamp, fritzboxid, identifier, parametername, value, valueoffset, isautocomplete) \
                        VALUES ('{timestamp}', '{fritzBoxId}','{identifier}', '{parametername}', {parametervalue}, {float(offset)}, {isautocomplete});"
    try:
        m_dbCursor.execute(m_sqlStatement)
        g_dbConnection.commit()
    except Exception as e:
        logging.error(e)
        logging.error(m_sqlStatement)


def getLastValue(fritzBoxId:str, identifier:str, parametername:str):
    global g_dbConnection

    m_dbCursor = g_dbConnection.cursor()
    m_lastValue = (datetime.datetime.now(), 0.0) # Init with valid timestamp
    m_sqlStatement = f"SELECT timestamp, value FROM values_float \
                        WHERE fritzboxid   = '{fritzBoxId}' AND \
                              identifier = '{identifier}' AND \
                              parametername = '{parametername}' \
                        ORDER BY timestamp desc limit 1"
    try:
        m_dbCursor.execute(m_sqlStatement)
        g_dbConnection.commit()
        m_rows = m_dbCursor.fetchone()
        if m_rows != None:
            m_lastValue = (m_rows[0], m_rows[1])
    except:
        g_dbConnection.rollback()
    

    return m_lastValue

def closeConnection():
    global g_dbConnection
    g_dbConnection.close()
    logging.info('Module dbConnector: Closing connection')