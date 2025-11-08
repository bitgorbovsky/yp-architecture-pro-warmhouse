-- Revert devices-registry:001-init-schema from pg

BEGIN;

DROP TABLE public.devices;
DROP SEQUENCE public.warmhouse_id;

COMMIT;
