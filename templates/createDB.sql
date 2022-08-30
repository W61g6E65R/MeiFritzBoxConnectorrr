CREATE TABLE values(
    id          SERIAL, PRIMARY KEY,
    timestamp   timestamp,
    fritzBoxId  varchar(24),
    identifier  varchar(24),
    value       double
)

CREATE TABLE deviceList(
    id          SERIAL, PRIMARY KEY,
    identifier  varchar(24),
    fritzBoxId  varchar(24),
    readTemperature boolean,
    readPowerConsumption boolean,
    readHumidity boolean,
    comment     varchar(128)
)