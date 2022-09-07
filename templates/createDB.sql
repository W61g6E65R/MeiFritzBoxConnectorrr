CREATE TABLE values_double(
    id              SERIAL PRIMARY KEY,
    timestamp       timestamp,
    fritzBoxId      varchar(24),
    identifier      varchar(24),
    parameterName   varchar(24),
    value           float
)
CREATE TABLE values_bool(
    id              SERIAL, PRIMARY KEY,
    timestamp       timestamp,
    fritzBoxId      varchar(24),
    identifier      varchar(24),
    parameterName   varchar(24),
    value           boolean
)

CREATE TABLE deviceList(
    id                      SERIAL PRIMARY KEY,
    identifier              varchar(24),
    name                    varchar(24),
    fritzBoxId              varchar(24),
    readTemperature         boolean,
    readPowerConsumption    boolean,
    readHumidity            boolean,
    comment                 varchar(128)
)