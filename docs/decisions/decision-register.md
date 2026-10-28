# Decision register

<!-- reading-sequence:start -->
[Previous: Existing-system schema research](../research/existing-system-schemas.md) | [Next: Database decision records](adr/README.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Product goal](../product-goal.md) | [Database ADRs](adr/README.md)

Recorded 2026-10-28 from the project conversation. User decisions and proposed implementation choices are deliberately distinguished. This register is not a legal ownership agreement.

## Confirmed direction

| ID | Decision | Basis and implications |
| --- | --- | --- |
| P001 | Build an open-source IMS intended for GitHub | User direction. Publication, repository destination, and license have not yet been selected. |
| P002 | Serve small and midsize companies across sectors | User explicitly includes manufacturing, pharma, and other businesses. Use a shared inventory core with optional sector capabilities. Do not assume pharma compliance from a generic schema. |
| P003 | Stock entry must natively support items without original bills | Explicit user requirement. One stock-entry form; optional documents and supplier. No fake bill, special undocumented-stock module, or mandatory accounting workaround. |
| P004 | Use local PostgreSQL | User choice. PostgreSQL 17 client is installed; server availability and credentials were not established. No database was changed. |
| P005 | Research existing tables and columns before implementation | User request. Record exact source commits and field declarations; do not describe framework model fields as a complete physical database dump. |
| P006 | Document product decisions, engineering decisions, and code provenance | User direction. Decisions should include alternatives, rationale, consequences, and evidence. |
| P008 | Include audit/compliance and overlapping-sector import/export scenarios | User request. Initial jurisdiction confirmed as India-based businesses importing/exporting internationally; destination and goods remain unspecified. |
| P009 | Use scrape.do for subsequent scraping; stop Firecrawl use | User instruction after Firecrawl credits were exhausted. Successful CDSCO PDF retrieval verified; credential used transiently, not committed. |

## Proposed technical decisions — reviewable, not yet accepted implementation

Schema-evolution tooling was initialized at the user's request: [ADR 0001](adr/0001-schema-evolution.md) selects dbmate v2.37.0 plus Git-tracked ADRs. The CLI generated the namespace baseline; no migration has been applied to a database. [ADR 0002](adr/0002-physical-entry-and-financial-evidence.md) captures the confirmed bill-independent entry requirement. Table-specific review begins in the [discussion queue](../design/table-discussions.md).

The user requested an auditable table/column inventory. The generated [schema audit](../design/schema-audit.md) consolidates the proposals and records unresolved issues; it does not constitute approval or an applied schema. Mutable audit columns and partially specified trade fields need table-level review.

| ID | Proposal | Alternatives and rationale | Consequence / revisit condition |
| --- | --- | --- | --- |
| E001 | Separate item definitions, physical transactions, ledger entries, balance projections, and financial documents | A single products.quantity column cannot explain changes or safely represent lots, sites, reservations, and integrations. Upstream systems also separate these concerns. | More tables, but inspectable history and rebuildable balances. |
| E002 | Every physical entry uses the same transaction header and line model | Alternatives: bill-driven stock creation or separate no-bill stock. Both conflict with P003. Optional receipt/bill/order links attach evidence without controlling eligibility to enter stock. | Require item, quantity, unit, location and actor; document, supplier and cost can be absent. |
| E003 | Preserve unknown costs as NULL with a valuation status | Zero cost and unknown cost have different meanings. A zero-default would create false inventory values. | Quantity posting may succeed without cost; reports expose unvalued quantity and incomplete valuation. |
| E004 | Use normalized shared core and typed sector tables | Alternatives: a separate database per industry, hundreds of nullable item columns, or JSON-only inventory. | Optional batch, serial, quality and manufacturing tables; JSON reserved for integration payloads and noncritical metadata. |
| E005 | Immutable posted quantity ledger, corrections by reversal | Editing balances or deleting history prevents reliable reconciliation. | Controlled posting routine, permissions and immutability enforcement are required, not just a UI convention. |
| E006 | Balance rows are transactionally maintained projections | Alternative: compute every stock check from the entire ledger. | Deliberate denormalization for locking and performance; reconciliation must detect drift. |
| E007 | Enforce organization consistency with composite foreign keys | UUIDs alone do not prevent cross-company links. | Every organization-owned parent has UNIQUE(org_id,id); child references include org_id. Authentication and authorization remain separate work. |
| E008 | ERP integration uses external mappings, inbox deduplication and a transactional outbox | Alternatives: external IDs as primary keys or writing core tables directly from connectors. | Independent internal identities, retries, reconciliation and explicit ownership of fields. |
| E009 | Restrict initial valuation posting order; retain original occurrence time | Unrestricted backdated cost postings can require replaying downstream valuation. | Record occurred_at and recorded_at separately. Historical quantity reports and accounting valuation dates must state their basis. Valuation replay is deferred. |

## Proposed product goal and scope

2026-10-28 consolidated framing: user requested a clear problem statement after stakeholder research. The [product goal](../product-goal.md) now centers on unreliable stock decisions and costly handoffs across people/tools, with explainable eligible quantities and reconstructable history as intended outcomes. Initial adoption is problem-based across sectors; initial delivery remains the shared stock-control loop. Open source, local PostgreSQL and broad sector coverage support the approach but are not themselves business problems. This is a documented proposal; impact and differentiation are not yet validated in pilots.

2026-10-28 stakeholder extension: the user requested actual operational roles and existing-software challenges. [Stakeholder research](../research/stakeholders-and-operational-workflows.md) records role-attributed reports, documented tasks, responsibility/access boundaries and observation tasks. Proposed role-specific workspaces remain hypotheses; no direct interviews or software usability tests have been performed.

2026-10-28 compliance extension: [Design addendum](../design/compliance-and-trade.md) proposes independent action gates, provenance segmentation, versioned evidence and approval snapshots. Existing vendor capabilities are documented in [research](../research/india-compliance-and-trade.md); no claim of universal market absence is supported. These additions are not applied migrations or certification claims. Regime-, entity- and destination-specific applicability remains subject to review.

2026-10-28: [Product goal](../product-goal.md) proposes reliable stock decisions and reduced reconciliation effort as the organizing outcome. Initial release scope is a complete shared stock-control loop, with sector-specific workflows added against explicit acceptance criteria. This is a proposal in response to the user's request to define the business goal, not an assertion that numerical success targets or sector priorities have been approved. Measure sustained physical-count agreement and operator effort; establish baseline and targets with pilot users.

## Candidate product features, not committed scope

- Supplier-specific codes and purchasing units on one internal SKU.
- Reservations separate from physical stock, with optional expiration.
- Traceable stock adjustments and safe imports.
- Saved operational reports with ledger drill-down.
- Observable, retryable integrations rather than an unqualified real-time guarantee.
- Manufacturing BOMs and consumption/output genealogy.
- Lot/serial/expiry and quarantine/release capabilities where enabled.

Prior research signals: [supplier aliases](https://help.zoho.com/portal/en/community/topic/zoho-inventory-tracking-stock-from-various-vendors), [inFlow operational reviews](https://www.capterra.com/p/78431/inFlow-Inventory/reviews/), [Cin7 integration and usability reviews](https://www.g2.com/products/cin7-core/reviews?qs=pros-and-cons). Reviews are contextual and sometimes historical, not proof of present universal deficiencies.

## Open decisions

- License, repository owner/name, contribution policy and supported deployment model.
- Single organization initially versus multi-organization UI; draft schema preserves isolation either way.
- Valuation method, landed-cost distribution, currency conversion and accounting ownership.
- Supported first ERP connector and direction of authority per object/field.
- Quantity precision by unit, retention, timezone display and numbering conventions.
- Sector-specific requirements and applicable pharma jurisdictions; compliance needs separate verification.
- Contribution, review and authorship practices for future changes.

## Decision template

ID / date / status / decision maker / problem / evidence / alternatives / choice / tradeoffs / verification / revisit trigger / related code or PR.

<!-- reading-sequence:start -->
[Previous: Existing-system schema research](../research/existing-system-schemas.md) | [Next: Database decision records](adr/README.md)
<!-- reading-sequence:end -->
