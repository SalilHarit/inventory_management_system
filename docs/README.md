# Documentation index

<!-- reading-sequence:start -->
[Previous: Project home](../README.md) | [Next: Product goal](product-goal.md)
<!-- reading-sequence:end -->

[Project home](../README.md)

This index connects the project's product research, proposed database design, decision records, and migration workflow. The database designs remain proposals until implemented and validated.

Follow the **Previous** and **Next** links at the top or bottom of each page to read the documentation in sequence. Start with the [product goal](product-goal.md), then continue through user research, decisions, database design, and the migration workflow.

## Product and user research

- [Product goal and business outcomes](product-goal.md) — the business problem, users, initial scope, and success measures.
- [Stakeholders and operational workflows](research/stakeholders-and-operational-workflows.md) — roles, observed software challenges, and field-research questions.
- [India compliance and trade research](research/india-compliance-and-trade.md) — source-backed findings and jurisdictional limitations.

## Database design and review

- [Table and column audit](design/schema-audit.md) — consolidated proposed names and open audit findings.
- [Table discussion queue](design/table-discussions.md) — suggested order and questions for reviewing tables.
- [PostgreSQL schema proposal](design/database-schema.md) — the core table dictionary and constraints.
- [Compliance and trade design](design/compliance-and-trade.md) — independent holds, shipment evidence, and cross-border provenance.
- [Posting and ERP integration](design/posting-and-integration.md) — concurrency, corrections, integration contracts, and acceptance scenarios.
- [Existing-system schema research](research/existing-system-schemas.md) — upstream field declarations and source references.

## Decisions and change history

- [Decision register](decisions/decision-register.md) — confirmed direction, proposed choices, and open questions.
- [Database decision records](decisions/adr/README.md) — ADR index and template.
  - [ADR 0001: schema evolution](decisions/adr/0001-schema-evolution.md)
  - [ADR 0002: physical entry and financial evidence](decisions/adr/0002-physical-entry-and-financial-evidence.md)
- [Migration workflow](../db/README.md) — dbmate setup and schema-change process.
- [Contribution provenance](contribution-provenance.md) — project work, sources, validation, and review status.

<!-- reading-sequence:start -->
[Previous: Project home](../README.md) | [Next: Product goal](product-goal.md)
<!-- reading-sequence:end -->
