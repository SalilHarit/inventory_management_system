# Contribution provenance

<!-- reading-sequence:start -->
[Previous: Migration workflow](../db/README.md)
<!-- reading-sequence:end -->

[Documentation index](README.md) | [Decision register](decisions/decision-register.md) | [Database ADRs](decisions/adr/README.md)

Document meaningful changes with the relevant decisions, sources, validations, and review status. Git history records the author of each committed change. Do not claim review or validation that has not occurred.

## Research and schema draft — 2026-10-28

The project direction covers cross-sector inventory, local PostgreSQL, physical stock entry without mandatory bills, concurrency, traceability, and ERP integration.

Research records identify public sources and exact upstream commits. The schema dictionary, table inventory, compliance addendum, and posting contracts are proposals for discussion. A namespace-only migration has been generated; no live database migration or concurrency test has been performed.

The source-field extraction recorded 506 direct declarations across 12 source files. Inherited and dynamically contributed fields may be absent. Public operator reviews and documentation inform stakeholder hypotheses; no operator interviews or pilot validation have been performed.

## Future changes

Link each substantial change to its product or engineering decision, sources, test evidence, and unresolved limitations. A reviewer should be able to reconstruct both the change and the reason for it.

<!-- reading-sequence:start -->
[Previous: Migration workflow](../db/README.md)
<!-- reading-sequence:end -->
