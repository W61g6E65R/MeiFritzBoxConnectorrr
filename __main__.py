# Imports
import os
import schedule
import time
import logging
import dotenv

# Local imports
import modules.globalConstants
import modules.dbConnector
import modules.fritzpy

logging.basicConfig(format=modules.globalConstants.LOGGING_CONFIG_FORMAT, level=logging.INFO)

# DEBUGGING
# dotenv.load_dotenv()

m_dbName = os.environ['DATABASE_NAME']
m_dbUser = os.environ['DATABASE_USER']
m_dbPassword = os.environ['DATABASE_PASSWORD']
m_dbHost = os.environ['DATABASE_HOST']
m_dbPort = os.environ['DATABASE_PORT']
m_fritzIp = os.environ['FRITZBOX_IP_ADDRESS']
m_fritzUser = os.environ['FRITZBOX_USER_NAME']
m_fritzPass = os.environ['FRITZBOX_USER_PASSWORD']
m_fritzIdent = os.environ['FRITZBOX_IDENTIFIER']
m_refreshRate_Automation  = os.environ['REFRESH_RATE_SMARTHOME_SECONDS']
m_refreshRate_DeviceList  = os.environ['REFRESH_RATE_DEVICELIST_MINUTES']
m_refreshRate_Connection  = os.environ['REFRESH_RATE_CONNECTION_MINUTES']

# Connect with database
modules.dbConnector.connect(m_dbName, m_dbUser, m_dbPassword, m_dbHost, m_dbPort)

# Connect with fritzBox
modules.fritzpy.connect(m_fritzIp, m_fritzUser, m_fritzPass, m_fritzIdent)

# First read in all configured devices from database
modules.fritzpy.updateDeviceList(m_fritzIdent)

schedule.every(m_refreshRate_Automation).seconds.do(modules.fritzpy.updateHomeAutomationDeviceValues, m_fritzIdent)
schedule.every(m_refreshRate_DeviceList).minutes.do(modules.fritzpy.updateDeviceList, m_fritzIdent)
schedule.every(m_refreshRate_Connection).minutes.do(modules.fritzpy.updateConnectionStatus, m_fritzIdent)

while True:
    schedule.run_pending()
    time.sleep(1)


