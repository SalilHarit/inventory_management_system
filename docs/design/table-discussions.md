# Table discussion queue

<!-- reading-sequence:start -->
[Previous: ADR 0002: bill-independent entry](../decisions/adr/0002-physical-entry-and-financial-evidence.md) | [Next: Database schema proposal](database-schema.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Table audit](schema-audit.md) | [Database ADRs](../decisions/adr/README.md)

Status: proposals for discussion, not executable table definitions. Use the [schema dictionary](database-schema.md) and [trade addendum](compliance-and-trade.md) as references; commit accepted contracts through ADRs and migrations.

The [consolidated audit inventory](schema-audit.md) lists all proposed table/column names, including common identity fields and known inconsistencies. Review the audit findings alongside each table discussion.

Use the [relationship diagrams](table-relationships.md) alongside the column inventory to trace how a proposed table connects to other domains.

## Discussion 1: organization, actor and organization_actor

Why first: stock, permissions, audit attribution and ERP mappings must agree about which business owns the record and who performed the action.

| Table | What one row means | Proposed key columns | Important boundary |
| --- | --- | --- | --- |
| organization | A business/legal stock-accounting boundary | id UUID, code, name, base_currency_code, display_timezone, created_at, created_by | A warehouse is not automatically an organization. Foreign branches/legal entities need explicit modeling. |
| actor | A person or service identity responsible for actions | id UUID, display_name, kind, external_subject, active, created_at, created_by | API imports have service identities. Deactivation preserves historical attribution. Authentication credentials are separate. |
| organization_actor | An actor's role assignment within a business | id UUID, org_id, actor_id, role_code, active, created_at, created_by | One actor may have multiple roles; permissions can later include site/action scope. Admin does not automatically mean QC/trade approver. |

Proposed constraints: organization code unique; non-null external_subject unique; role assignments unique by organization/actor/role. Organization-owned references use company-consistent FKs. Do not cascade-delete referenced identities. Bootstrap actor is an explicit setup exception for created_by.

Open design points: start UI with one business while preserving multiple-business isolation; whether legal entity versus operating unit needs separate tables; authentication provider and immutable subject identity; role definitions and site scopes; how display-name changes appear in historical audit evidence.

## Discussion 2: item, uom, item_uom and supplier_item

One internal SKU identifies the stocked variant. No bill or stock balance belongs in item. Purchasing cases and issuing pieces use item-specific conversions; supplier codes map to the same SKU. Agree base-unit change policy, packaging identity, decimal precision and serial/lot policy before migration.

## Discussion 3: location, provenance and holds

Agree which locations hold stock, legal owner versus custodian, and when identical item/lot stock must stay separate by receipt/customs regime. Quality and customs holds remain independent; a single available boolean is insufficient.

## Discussion 4: physical transactions, ledger and balances

Agree posting/correction contract, idempotency, lock order, serial position uniqueness and reservation interaction. A table definition alone cannot establish safe concurrent stock changes.

## Discussion 5: documents, purchasing and finance links

Agree immutable evidence versions, optional associations, partial receipts and bill matching. Continue native no-bill entry and explicit unknown valuation.

## Acceptance checklist for each table discussion

What does one row represent? Who creates/reads/changes it? Which facts are required or may be unknown? Which keys prevent duplication? Which relationships must match business/item scope? What changes are forbidden after posting? What concurrent operations contend? What evidence survives correction/deactivation? Which ERP owns each fact? What migration/backfill and tests demonstrate the contract?

<!-- reading-sequence:start -->
[Previous: ADR 0002: bill-independent entry](../decisions/adr/0002-physical-entry-and-financial-evidence.md) | [Next: Database schema proposal](database-schema.md)
<!-- reading-sequence:end -->
