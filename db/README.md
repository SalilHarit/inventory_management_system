# Schema evolution

<!-- reading-sequence:start -->
[Previous: Compliance and trade design](../docs/design/compliance-and-trade.md) | [Next: Contribution provenance](../docs/contribution-provenance.md)
<!-- reading-sequence:end -->

[Documentation index](../docs/README.md) | [Project home](../README.md) | [Database ADRs](../docs/decisions/adr/README.md) | [Table discussions](../docs/design/table-discussions.md)

Use dbmate v2.37.0 for ordered SQL migrations and Git-tracked ADRs for their rationale. [Official documentation](https://github.com/amacneil/dbmate/tree/v2.37.0).

## Current state

The initial migration creates the ims PostgreSQL namespace only. It does not implement the proposed tables. No migration has been applied to the user's database. db/schema.sql will be generated from an actual development database after the first application; it is deliberately absent until then.

Windows executable: `.tools/dbmate.exe` (local, ignored). The initial download is version-pinned; obtain the Windows amd64 asset from the official v2.37.0 release and verify its GitHub-provided SHA-256 digest when reinstalling. Other platforms can use the same pinned release. Binary files are not source artifacts.

## Workflow

1. Discuss the problem and table contract in [table discussions](../docs/design/table-discussions.md).
2. Record material decisions in [ADRs](../docs/decisions/adr/README.md). Distinguish proposed, accepted, implemented and superseded.
3. Generate a migration with `./.tools/dbmate.exe new descriptive_change_name`. Link its ADR in a SQL comment. Keep migration filenames/version order intact.
4. Review SQL, preservation/backfill requirements, constraints, lock impact and deployment compatibility. Use expand/backfill/contract for breaking changes. Do not automatically apply the entire draft schema.
5. Configure `.env` locally using `.env.example`. Use `./.tools/dbmate.exe status` to inspect database history. Use `migrate` to apply to an explicitly configured existing database; `up` may create a database and is not our routine command.
6. Test empty-database application, upgrade from the prior version, and relevant business/concurrency invariants on disposable databases. Inspect generated `db/schema.sql`, then commit migration, snapshot and ADR together after successful validation.

Examples (PowerShell, from repository root):

```powershell
./.tools/dbmate.exe --version
./.tools/dbmate.exe new add_item_catalog
./.tools/dbmate.exe status
# Mutates only the database selected by DATABASE_URL; inspect target first.
./.tools/dbmate.exe migrate
./.tools/dbmate.exe dump
```

PostgreSQL pg_dump must be available and compatible with the server for schema snapshots. Do not hand-edit a generated snapshot or mistake a successful SQL migration for validation of inventory behavior.

## History and recovery

Applied migrations are immutable project history: correct them with a new migration. dbmate stores version numbers, not migration content checksums; Git review protects source history, not the deployed database. Built-in deployed checksum validation would require another tool or a separately designed manifest/control. Do not claim dbmate detects edits to applied SQL.

SQL migrations run transactionally by default. A future nontransactional operation needs an explicit reviewed migration strategy. Migration locking serializes migration runners; ordinary dispatch/reservation safety is handled by the posting contract.

Down sections are required by dbmate, but destructive downgrades are not automatically safe. The initial baseline deliberately rejects rollback to protect future objects. Prefer forward fixes; define backup/restore and verify restoration before destructive data changes. Renaming/deleting columns is not an acceptable rollback strategy for preserving customer data.

## Schema history versus inventory audit

Migrations record structural changes. ADRs record decisions. Inventory/audit ledgers record business and administrative events. All three are needed; none substitutes for another.

<!-- reading-sequence:start -->
[Previous: Compliance and trade design](../docs/design/compliance-and-trade.md) | [Next: Contribution provenance](../docs/contribution-provenance.md)
<!-- reading-sequence:end -->
