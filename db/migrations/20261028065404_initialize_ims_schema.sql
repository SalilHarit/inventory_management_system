-- migrate:up
-- ADR: docs/decisions/adr/0001-schema-evolution.md
-- Namespace only; business tables remain under discussion.
CREATE SCHEMA ims;


-- migrate:down
-- Protect objects which subsequent migrations may add.
DO $$ BEGIN
  RAISE EXCEPTION 'Baseline rollback disabled. Use a reviewed forward migration or restore procedure.';
END $$;
