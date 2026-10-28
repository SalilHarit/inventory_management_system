# Compliance and trade design addendum

<!-- reading-sequence:start -->
[Previous: Posting and ERP integration](posting-and-integration.md) | [Next: Migration workflow](../../db/README.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Compliance research](../research/india-compliance-and-trade.md) | [Schema proposal](database-schema.md)

Status: proposal, no migration applied. Read with [schema](database-schema.md), [posting contract](posting-and-integration.md) and [India evidence](../research/india-compliance-and-trade.md).

## Product rule

Record physical reality accurately; independently determine permitted actions using explicit, sourced, versioned requirements. A missing bill never requires a separate stock-entry workflow. Recording goods without documents does not authorize tax claims, customs clearance, regulated use or dispatch.

One SKU can simultaneously be manufactured, pharma-related, imported and intended for export. Model these as composable capabilities and shipment context, not a mutually exclusive industry dropdown.

## Separate state dimensions

- Physical position: site, bin, transit and owner.
- Quality: inspection pending, released, rejected or excursion hold.
- Customs: applicable regime and evidenced clearance for the scoped quantity/action.
- Documentation: missing, under review, accepted, superseded.
- Commercial allocation: free, reserved, consumed.
- Financial valuation: unknown, estimated or finalized.

Do not encode every combination into stock_status or use one global compliant boolean. Keep the existing stock status for physical/quality allocation categorization, with independent holds and action gates. Passing one gate never clears another. Unknown applicability or missing mandatory evidence blocks the affected regulated action pending review, while ordinary physical recording remains possible.

## Proposed schema additions

Conventions from the base schema apply: organization-scoped IDs, composite organization FKs, exact quantities, actor/time metadata. These are planned modules, not instructions to implement every table in the initial release.

| Table | Principal columns | Integrity / purpose |
| --- | --- | --- |
| establishment | code, location_id, legal_name, address, jurisdiction_code | History/versioning for the actual operating premises; hierarchy and registration applicability reviewed |
| business_registration | establishment_id?, party_id?, registration_type, identifier, jurisdiction_code, valid_from, valid_to?, status, evidence_document_id? | Exactly one registration subject; retain historical validity, do not treat any number as proof of current validity |
| item_classification | item_id, jurisdiction_code, scheme, code, effective_from, effective_to?, reviewed_by, evidence_document_id? | Different national tariff/controlled-product classifications can coexist; classification requires qualified review |
| trade_shipment | number, direction, origin_country, destination_country, importer_party_id, exporter_party_id, consignee_party_id?, customs_regime, incoterm_code?, incoterm_version?, named_place?, currency_code, version | Internal shipment is not a filing. Incoterm is commercial allocation information, not automatic proof of origin, ownership or clearance |
| trade_shipment_line | shipment_id, line_no, item_id, quantity, item_uom_id, base_qty, origin_country?, classification_id | Snapshot approved classification/version; origin is not necessarily supplier country or ship-from country |
| shipment_stock_allocation | shipment_line_id, inventory_line_id, provenance_segment_id, base_qty | Supports partial and split shipments; locked cumulative allocations cannot exceed stock/line quantities |
| provenance_segment | item_id, lot_id?, owner_party_id?, originating_receipt_line_id, customs_regime, origin_evidence_document_id?, predecessor_segment_id? | Stable provenance identity; same lot from different import treatments is not merged implicitly |
| customs_declaration | shipment_id, declaration_type, reference, port_code, declaration_date, version, external_mapping_id?, evidence_document_id? | Bill of Entry/shipping bill scoped by authority/port/date as needed; exact unique identifier contract defined per integration |
| customs_declaration_line | declaration_id, line_no, shipment_line_id, declared_base_qty, assessed_value?, currency_code | Matching must support multiple line allocations before implementation if declaration and commercial lines differ |
| customs_release_event | declaration_line_id, released_base_qty, action_scope, occurred_at, source_authority, evidence_document_id, supersedes_id? | Append-only release/revocation history. Partial quantities retained; effective balance cannot exceed declared quantity |
| shipment_document | shipment_id, shipment_line_id?, document_version_id, document_role | Transport document, commercial invoice, packing list, certificate or permit are distinct roles |
| permit | registration_id?, permit_type, reference, jurisdiction_code, valid_from, valid_to?, evidence_document_id, status | Scope through normalized permit_scope rows; different licences have different quantitative limits |
| permit_scope | permit_id, item_id?, origin_country?, destination_country?, permitted_base_qty?, uom_id? | Explicit scope; quantity has a defined item/unit basis; no meaningless total across incompatible goods |
| permit_usage | permit_scope_id, shipment_line_id, base_qty, usage_type, reversal_of_id? | Append-only consumption/release, locked cumulative limits; no double spending across concurrent shipments |
| requirement_version | code, revision, jurisdiction_code, authority_url, effective_from, effective_to?, applicability_schema_version, definition jsonb, status, approved_by | Immutable published rules, validated schema, human-reviewed applicability; no autonomous legal rule generation |
| compliance_case | shipment_id?, inventory_transaction_id?, case_type, status, assigned_actor_id, subject_version, subject_hash | Explicitly constrained target; scope is company-consistent and relevant to action |
| compliance_check | case_id, requirement_version_id, action_scope, outcome (pass/fail/unknown/not_applicable), evaluated_at, valid_until?, evaluated_subject_hash, evidence_document_version_id? | Append-only evaluation snapshots; not_applicable requires rationale; changed scope/data invalidates reuse |
| inventory_hold | provenance_segment_id?, lot_id?, shipment_line_id?, hold_type, reason, effective_at, imposed_by, source_check_id? | Explicit target and propagation rules; hold event history for impose/release; scoped quantity allocation table if hold is partial |
| approval_event | case_id, decision, actor_id, role_at_decision, reason, decided_at, subject_hash, evidence_document_version_id? | Maker/checker where required; approval bound to exact facts, cannot approve a changed shipment accidentally |
| document_version | document_id, version_no, storage_key, content_hash, recorded_at, supersedes_id?, source, verification_status | Immutable original files and versions; deleting/replacing an attachment must not rewrite evidence |
| audit_review | scope, period_from, period_to, reviewer_id, reviewed_at, finding_count, report_document_version_id | Shows actual audit review rather than merely having logs; full finding linkage before implementation |
| evidence_export | case_id?, requested_by, created_at, snapshot_hash, manifest_storage_key, format_version | Reproducible case pack with scoped movements, documents, decisions and external acknowledgements |

Required base changes: add provenance_segment_id to stock_bucket and its natural unique key so legally/operationally distinct stock is not coalesced. Segment is mandatory for tracked trade stock; existing domestic stock can use an explicit ordinary provenance segment. Manufacturing may need multiple parent segments through genealogy; predecessor_segment_id alone is not enough for many-input transformations. Add trace links across input segments and outputs, preserving quantities without assuming all origin/restriction rules propagate identically.

Support many-to-many customs-line mappings via declaration_line_allocation if external line layouts differ. Do not enforce a one-to-one line assumption in production DDL. Full tax, duty, FX, recoverable-credit and landed-cost calculations remain a separate reviewed accounting module; store source amounts and bases instead of one undifferentiated cost.

## Atomic action gates and concurrency

Allocation, production issue and dispatch recheck applicable holds and approvals inside the posting transaction. Lock affected lot/provenance/hold-scope guard rows before balance locks using one globally consistent order. The hold-creation path acquires the same guards, preventing a check-then-dispatch race. Lock shipment/version and permit-scope rows before validating remaining clearance/permit quantities. Re-evaluate stale checks after destination, party, item, quantity, evidence or classification changes.

Checks identify the action: recording presence, relocation under authorized procedure, manufacturing consumption, ordinary sale and export dispatch are not interchangeable. Do not forbid required quarantine handling merely because commercial use is blocked. Exact permitted actions come from reviewed regime policy.

No business-user override may silently bypass a statutory prohibition. Any permitted exception has an explicit basis, authorized reviewer, evidence, scope and expiry. Escalation is not a legal exemption. Government API failure leaves status pending/unknown rather than passing it; preserve external request/response IDs through existing inbox/outbox machinery.

## Audit controls beyond stock history

Audit master-data changes, classification/permit edits, approvals, policy changes, role changes, imports, integrations, document versions and privileged operations—not just stock movements. Capture original and revised values, actor, authenticated source, server recorded time, stated occurrence time and correlation ID. Preserve successive changes, not only the latest value.

Local PostgreSQL owners/superusers can defeat ordinary triggers and change stored data. Do not call an in-database append-only table tamper-proof. Separate application/admin duties, database audit logging, restricted credentials, independently retained exports/checkpoints, monitoring of disabled controls, tested backup/restore and deployment change records are required design work. Hashes stored in the same administrator-controlled database are not independent tamper evidence. Digital signatures/e-signature regimes require separately validated identity, signing and key controls; an approval button is not automatically a legally recognized signature.

Retention is a sourced rule by record category/entity/regime plus legal hold. Deletion routines must respect preservation duties and hold status. Determine applicable Indian accounting backup/access requirements with the entity's auditor; a generic daily backup promise does not certify compliance. Operational audit documentation includes software/configuration versions and evidence that controls operated over the period.

## Acceptance scenarios

1. QC pass leaves customs hold intact; customs release leaves quality hold intact.
2. Identical SKU/lot from two regimes remains separately traceable through transfers and production.
3. Partial release permits only released eligible quantity; concurrent dispatches cannot consume clearance/permit capacity twice.
4. Route or document changes invalidate previous approvals; old evidence remains retrievable.
5. No-bill receipt succeeds in the ordinary form; required-document gaps remain explicit and action-scoped.
6. A new recall/hold racing with dispatch has a serializable outcome through shared guards.
7. ERP replay cannot remove a hold, duplicate an external declaration or overwrite reviewed classifications without review.
8. Auditor can reconstruct one shipment's receipt, lot genealogy, usage, approvals, declarations and changes from a versioned evidence export.
9. Direct database changes, restore tests and logging gaps are detected/documented under the deployment's audit design.

## Delivery sequence

Foundation now: actor/reason history, document versions, independent holds, provenance segmentation, role boundaries and evidence export design. Then India trade-document/registration workflows and reviewed action gates. Later destination/product rule packs, controlled-goods screening, bonded/special procedures and validated pharma deployment packs. Each advertised capability needs its own source review, acceptance tests and operator validation.

<!-- reading-sequence:start -->
[Previous: Posting and ERP integration](posting-and-integration.md) | [Next: Migration workflow](../../db/README.md)
<!-- reading-sequence:end -->
