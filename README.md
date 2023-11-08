# MeiFritzBoxConnectorrr

Get Data from FritzBox (FritzConnection) and write it in a database

## Description

With this project it is possible to periodicaly read data from DECT devices which are connected to a fritzBox
and write them to a postgresql database.
It is also possible to connect more than one FritzBox, but all need the same user and password.

## Preparation

  - **VirtualEnv**
    - <code>python3 -m venv .venv </code>
  - **Docker-Compose**
    - Rename /templates/template.env to ./.env
    - Insert credentials in .env file. This file is used in docker-compose
  - **Postgresql**
    - Create tables with sql from ./templates/createDB.sql