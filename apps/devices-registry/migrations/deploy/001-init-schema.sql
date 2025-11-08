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
    tags character varying[],
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    modified_at TIMESTAMP DEFAULT now() NOT NULL
);
ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (address, provider, protocol);
ALTER TABLE public.devices OWNER TO iot;

CREATE OR REPLACE FUNCTION device_update_modified_at()
RETURNS trigger
AS $$
BEGIN
    NEW.modified_at := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER devices_update_trigger
    BEFORE UPDATE ON public.devices
    FOR EACH ROW
    EXECUTE FUNCTION device_update_modified_at();

COMMIT;
