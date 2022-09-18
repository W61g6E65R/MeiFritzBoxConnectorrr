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

# Connect with database
modules.dbConnector.connect(m_dbName, m_dbUser, m_dbPassword, m_dbHost, m_dbPort)

# Connect with fritzBox
modules.fritzpy.connect(m_fritzIp, m_fritzUser, m_fritzPass, m_fritzIdent)

schedule.every(15).seconds.do(modules.fritzpy.updateHomeAutomationDeviceValues, m_fritzIdent)
schedule.every(60).minutes.do(modules.fritzpy.updateDeviceList, m_fritzIdent)
schedule.every(5).minutes.do(modules.fritzpy.updateConnectionStatus, m_fritzIdent)

while True:
    schedule.run_pending()
    time.sleep(1)


