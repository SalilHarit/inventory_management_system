# Open IMS

<!-- reading-sequence:start -->
[Next: Documentation index](docs/README.md)
<!-- reading-sequence:end -->

Open-source inventory management for small and midsize organizations across sectors.

Teams lose time and make purchasing, production and delivery mistakes when they cannot agree on what stock exists, where it is, what can be used, or why it changed. Open IMS aims to give operators, supervisors and reviewers one traceable operational record—from physical entry to use or dispatch—with clear quantities, restrictions, responsibilities and supporting evidence.

The first proposed release focuses on the shared receiving, movement, reservation, issue and count workflow. Manufacturing, pharma and international-trade capabilities extend that core as their requirements are validated.

Status: research and database design. No application or production schema has been implemented.

Start with the [documentation index](docs/README.md) to browse related product, research, database, and decision documents.

- [Product goal and business outcomes](docs/product-goal.md)
- [Stakeholders, existing workflows and operator challenges](docs/research/stakeholders-and-operational-workflows.md)
- [India compliance and trade research](docs/research/india-compliance-and-trade.md)
- [Compliance, auditability and cross-border design](docs/design/compliance-and-trade.md)
- [Project decisions](docs/decisions/decision-register.md)
- [Schema evolution workflow](db/README.md)
- [Database decision records](docs/decisions/adr/README.md)
- [Table discussion queue](docs/design/table-discussions.md)
- [Upstream table and column research](docs/research/existing-system-schemas.md)
- [Proposed PostgreSQL schema and column dictionary](docs/design/database-schema.md)
- [Consolidated proposed table and column audit](docs/design/schema-audit.md)
- [Concurrency and ERP integration contracts](docs/design/posting-and-integration.md)
- [Contribution provenance](docs/contribution-provenance.md)

Inventory entry accepts stock with or without an original bill through the same form and posting path. Bills document financial obligations; they are not prerequisites for physical inventory.

The project is released under the [MIT License](LICENSE).

<!-- reading-sequence:start -->
[Next: Documentation index](docs/README.md)
<!-- reading-sequence:end -->
