# ADR 0002 — Physical inventory entry does not require a bill

<!-- reading-sequence:start -->
[Previous: ADR 0001: schema evolution](0001-schema-evolution.md) | [Next: Table discussions](../../design/table-discussions.md)
<!-- reading-sequence:end -->

[Documentation index](../../README.md) | [Project home](../../../README.md) | [Database ADRs](README.md) | [Schema proposal](../../design/database-schema.md)

Date: 2026-10-28.

Status: user-confirmed product requirement; table implementation proposed, not applied.

Contribution details and review status are recorded in Git history and the project provenance document.

## Context

Goods may exist before paperwork is available, have been produced internally, be returned, or be opening stock. A financial document may also disagree with the quantity received. Using a mandatory bill foreign key as the stock-entry root misrepresents those situations.

## Decision

Separate item, physical transaction header/lines, posted stock ledger, optional document links and supplier bill/matching records. The same entry form and posting path accepts receipts with or without bills. Unknown costs remain unknown; lot/serial and action-eligibility requirements apply independently.

Alternatives rejected: mandatory supplier invoice for every receipt; fabricated invoice for opening stock; separate no-bill stock module.

## Consequences and invariants

- inventory_transaction and inventory_line must not require supplier_bill_id.
- One receipt can have zero or many documents; later matching does not post quantity again.
- Document capture does not establish tax eligibility or regulatory permission.
- Stock and valuation updates remain separate and traceable.
- Physical movements preserve actor, unit conversion, location and reason.

Affected proposed tables: item, inventory_transaction, inventory_line, stock_ledger_entry, transaction_document, supplier_bill, bill_receipt_allocation, line_cost_estimate.

Migration: none yet. Validation remaining: native no-bill and bill-attached entry equivalence; late matching without duplicate quantity; unknown versus zero cost.

<!-- reading-sequence:start -->
[Previous: ADR 0001: schema evolution](0001-schema-evolution.md) | [Next: Table discussions](../../design/table-discussions.md)
<!-- reading-sequence:end -->
