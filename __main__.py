# Imports.general
import os
import schedule
import time
import logging
import dotenv

# Imports.local
from modules.class_ConnectionObject import ConnectionObject
from modules.class_Fritzpy import FritzPy
import config

logging.basicConfig(format = '%(asctime)s - %(message)s', 
                    level  = logging.INFO)

# Load environmental var from .env file
dotenv.load_dotenv()

# Init database
db_connectionObject = ConnectionObject(address      = config.database['address'],
                                       userName     = os.environ['DATABASE_USER_NAME'],
                                       password     = os.environ['DATABASE_USER_PASSWORD'],
                                       identifier   = config.database['name'],
                                       port         = config.database['port'])

# All fritzBoxes need the same user/password!
fritzBox_list = []
for fritzBoxItem in config.fritzBox_list:
    connection_object= ConnectionObject(address     = fritzBoxItem['address'],
                                         identifier = fritzBoxItem['identifier'],
                                         userName   = os.environ['FRITZBOX_USER_NAME'],
                                         password   = os.environ['FRITZBOX_USER_PASSWORD'])
    fritzBox_list.append(FritzPy(connection_object, db_connectionObject))


for fritzBox in fritzBox_list:
    # Update local device list files /data...
    fritzBox.exportDeviceList(f'./data/deviceList_{fritzBox.identifier}')
    
    # Read device config from database
    schedule.every(1).hour.do(fritzBox.updateInternalDeviceList)

    # Read values from every configured device
    for device in fritzBox.deviceConfig:
        schedule.every(device['cycleTime']).seconds.do(fritzBox.updateDeviceValues, deviceId=device['id'])

while True:
    schedule.run_pending()
    time.sleep(1)
