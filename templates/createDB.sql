CREATE TABLE public.devicelist (
	"namespace" varchar(16) NOT NULL,
	deviceid varchar(32) NOT NULL,
	alias varchar(32) NULL,
	devicetype varchar(32) NULL,
	active bool NULL,
	"comment" varchar(128) NULL,
	readtemperature bool NULL DEFAULT false,
	readpower bool NULL DEFAULT false,
	readhumidity bool NULL DEFAULT false,
	readrainfall bool NULL DEFAULT false,
	CONSTRAINT devicelist_pk PRIMARY KEY (namespace, deviceid)
);

CREATE TABLE public.devicevalues (
	"timestamp" timestamp NOT NULL,
	"namespace" varchar(16) NOT NULL,
	deviceid varchar(32) NOT NULL,
	parametername varchar(16) NOT NULL,
	value float8 NOT NULL,
	valueoffset float8 NULL DEFAULT 0.0,
	CONSTRAINT devicevalues_pk PRIMARY KEY ("timestamp", namespace, deviceid)
);