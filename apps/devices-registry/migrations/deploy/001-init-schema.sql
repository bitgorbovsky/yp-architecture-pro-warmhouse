-- Deploy devices-registry:001-init-schema to pg

BEGIN;

--
-- Sequence for warmhouse old device records for
-- compatibility with old monolite app
--
CREATE SEQUENCE public.warmhouse_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.warmhouse_id OWNER TO iot;


--
-- Table with devices.
--
CREATE TABLE public.devices (
    address character varying DEFAULT nextval('public.warmhouse_id'::regclass) NOT NULL,
    provider character varying NOT NULL,
    protocol character varying NOT NULL,
    kind character varying NOT NULL,
    model character varying NOT NULL,
    serialnum character varying NOT NULL,
    name character varying,
    description text,
    tags character varying[]
);
ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (address, provider, protocol);
ALTER TABLE public.devices OWNER TO iot;

COMMIT;
