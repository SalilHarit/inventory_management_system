# ADR 0001 — Versioned SQL migrations and database decisions

<!-- reading-sequence:start -->
[Previous: Database decision records](README.md) | [Next: ADR 0002: bill-independent entry](0002-physical-entry-and-financial-evidence.md)
<!-- reading-sequence:end -->

[Documentation index](../../README.md) | [Project home](../../../README.md) | [Database ADRs](README.md) | [Migration workflow](../../../db/README.md)

Date: 2026-10-28.

Status: accepted for initial tooling under the user's instruction to start tracking schema evolution. No business table decisions or live database application are implied.

Contribution details and review status are recorded in Git history and the project provenance document.

## Context and options

The project has a broad proposed column dictionary but no applied schema or application framework. We need executable structural history and a record of rationale without committing to an ORM.

- dbmate: simple SQL migrations and generated schema snapshots; no applied-content checksum validation.
- Atlas: offers versioned migration workflows and integrity mechanisms; a larger workflow to evaluate if needed.
- Framework migrations: defer until a framework is selected; does not meet the immediate need.

## Decision

Use pinned dbmate v2.37.0 and PostgreSQL SQL, with ADRs committed beside changes. Start with an ims namespace baseline only. No table creation from an unreviewed dictionary, no automatic connection using guessed credentials. Track the generated schema snapshot only after actual successful application/dump.

## Consequences

Readable, portable history independent of application framework. dbmate records versions rather than checksums; applied-file immutability relies on source review and process. If deployment attestation, built-in drift/checksum enforcement or richer migration review becomes necessary, revisit the tool explicitly and preserve history.

Migrations are infrastructure history, not business audit evidence. No feature can claim compliance because it has a migration or ADR.

## Validation

Local CLI installation/version and migration generation are checked as part of setup. No live-database migration, downgrade, dump or concurrency test has been performed. See db/README.md for commands and requirements.

Related migration: the generated `initialize_ims_schema` baseline in db/migrations. Exact filename is recorded in that directory.

<!-- reading-sequence:start -->
[Previous: Database decision records](README.md) | [Next: ADR 0002: bill-independent entry](0002-physical-entry-and-financial-evidence.md)
<!-- reading-sequence:end -->
