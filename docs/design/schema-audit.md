# Proposed table and column audit

<!-- reading-sequence:start -->
[Previous: Database schema proposal](database-schema.md) | [Next: Posting and ERP integration](posting-and-integration.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Table discussions](table-discussions.md)

Generated 2026-10-28 from the base schema and trade addendum. This consolidates names for discussion; it is not SQL, an approved final schema or a deployed database inventory.

**75 proposed tables; 730 explicitly listed column positions including expanded identity/audit columns.** Mutable metadata is listed separately below and not included in that count.

[Machine-readable inventory](schema-audit.json) · [Base dictionary](database-schema.md) · [Trade addendum](compliance-and-trade.md) · [Table discussion queue](table-discussions.md)

## Read this before auditing

- Every table below expands id, created_at, created_by and org_id where the draft requires them. Global currency uses code as its primary key and has no organization/audit columns under the current convention.
- Mutable master/draft records also need updated_at, updated_by and version. Their exact per-table assignment is NOT settled; audit this before DDL. Existing explicitly declared version columns are included.
- A question mark in a source declaration means optional. The trade addendum has incomplete type/nullability declarations; missing detail is labeled rather than silently invented.
- Common created_by versus event-specific actor_id/reviewer_id/posted_by fields can overlap. Review their distinct recording/action/approval meaning; do not remove attribution blindly.
- Sources remain proposals. Future migrations and the generated live schema snapshot will establish the implemented truth.

## Table index

| # | Table | Group | Listed columns |
| --- | --- | --- | --- |
| 1 | [organization](#organization) | Identity and shared catalog | 7 |
| 2 | [actor](#actor) | Identity and shared catalog | 7 |
| 3 | [organization_actor](#organization_actor) | Identity and shared catalog | 7 |
| 4 | [currency](#currency) | Identity and shared catalog | 3 |
| 5 | [uom](#uom) | Identity and shared catalog | 8 |
| 6 | [item](#item) | Identity and shared catalog | 11 |
| 7 | [item_uom](#item_uom) | Identity and shared catalog | 9 |
| 8 | [item_identifier](#item_identifier) | Identity and shared catalog | 8 |
| 9 | [party](#party) | Identity and shared catalog | 7 |
| 10 | [party_role](#party_role) | Identity and shared catalog | 6 |
| 11 | [supplier_item](#supplier_item) | Identity and shared catalog | 11 |
| 12 | [supplier_price](#supplier_price) | Identity and shared catalog | 10 |
| 13 | [location](#location) | Locations, tracking and physical stock | 9 |
| 14 | [stock_status](#stock_status) | Locations, tracking and physical stock | 7 |
| 15 | [lot](#lot) | Locations, tracking and physical stock | 10 |
| 16 | [serial](#serial) | Locations, tracking and physical stock | 7 |
| 17 | [stock_bucket](#stock_bucket) | Locations, tracking and physical stock | 11 |
| 18 | [stock_balance](#stock_balance) | Locations, tracking and physical stock | 8 |
| 19 | [inventory_transaction](#inventory_transaction) | Locations, tracking and physical stock | 16 |
| 20 | [inventory_line](#inventory_line) | Locations, tracking and physical stock | 13 |
| 21 | [stock_ledger_entry](#stock_ledger_entry) | Locations, tracking and physical stock | 9 |
| 22 | [reservation](#reservation) | Locations, tracking and physical stock | 11 |
| 23 | [reservation_allocation](#reservation_allocation) | Locations, tracking and physical stock | 9 |
| 24 | [reservation_event](#reservation_event) | Locations, tracking and physical stock | 10 |
| 25 | [document](#document) | Optional documents, purchasing and sales | 10 |
| 26 | [transaction_document](#transaction_document) | Optional documents, purchasing and sales | 6 |
| 27 | [purchase_order](#purchase_order) | Optional documents, purchasing and sales | 10 |
| 28 | [purchase_order_line](#purchase_order_line) | Optional documents, purchasing and sales | 13 |
| 29 | [receipt_order_allocation](#receipt_order_allocation) | Optional documents, purchasing and sales | 7 |
| 30 | [supplier_bill](#supplier_bill) | Optional documents, purchasing and sales | 11 |
| 31 | [supplier_bill_line](#supplier_bill_line) | Optional documents, purchasing and sales | 12 |
| 32 | [bill_receipt_allocation](#bill_receipt_allocation) | Optional documents, purchasing and sales | 8 |
| 33 | [sales_order](#sales_order) | Optional documents, purchasing and sales | 8 |
| 34 | [sales_order_line](#sales_order_line) | Optional documents, purchasing and sales | 10 |
| 35 | [dispatch_order_allocation](#dispatch_order_allocation) | Optional documents, purchasing and sales | 7 |
| 36 | [line_cost_estimate](#line_cost_estimate) | Valuation, counts and sector extensions | 9 |
| 37 | [valuation_event](#valuation_event) | Valuation, counts and sector extensions | 12 |
| 38 | [stock_count](#stock_count) | Valuation, counts and sector extensions | 9 |
| 39 | [stock_count_line](#stock_count_line) | Valuation, counts and sector extensions | 10 |
| 40 | [quality_inspection](#quality_inspection) | Valuation, counts and sector extensions | 10 |
| 41 | [quality_result](#quality_result) | Valuation, counts and sector extensions | 9 |
| 42 | [bom](#bom) | Valuation, counts and sector extensions | 8 |
| 43 | [bom_component](#bom_component) | Valuation, counts and sector extensions | 9 |
| 44 | [production_order](#production_order) | Valuation, counts and sector extensions | 8 |
| 45 | [production_posting](#production_posting) | Valuation, counts and sector extensions | 6 |
| 46 | [production_genealogy](#production_genealogy) | Valuation, counts and sector extensions | 7 |
| 47 | [entity_registry](#entity_registry) | Integration and audit | 6 |
| 48 | [integration_connection](#integration_connection) | Integration and audit | 10 |
| 49 | [external_mapping](#external_mapping) | Integration and audit | 10 |
| 50 | [integration_inbox](#integration_inbox) | Integration and audit | 13 |
| 51 | [integration_outbox](#integration_outbox) | Integration and audit | 9 |
| 52 | [integration_delivery](#integration_delivery) | Integration and audit | 12 |
| 53 | [audit_event](#audit_event) | Integration and audit | 10 |
| 54 | [establishment](#establishment) | Trade / compliance | 9 |
| 55 | [business_registration](#business_registration) | Trade / compliance | 13 |
| 56 | [item_classification](#item_classification) | Trade / compliance | 12 |
| 57 | [trade_shipment](#trade_shipment) | Trade / compliance | 17 |
| 58 | [trade_shipment_line](#trade_shipment_line) | Trade / compliance | 12 |
| 59 | [shipment_stock_allocation](#shipment_stock_allocation) | Trade / compliance | 8 |
| 60 | [provenance_segment](#provenance_segment) | Trade / compliance | 11 |
| 61 | [customs_declaration](#customs_declaration) | Trade / compliance | 12 |
| 62 | [customs_declaration_line](#customs_declaration_line) | Trade / compliance | 10 |
| 63 | [customs_release_event](#customs_release_event) | Trade / compliance | 11 |
| 64 | [shipment_document](#shipment_document) | Trade / compliance | 8 |
| 65 | [permit](#permit) | Trade / compliance | 12 |
| 66 | [permit_scope](#permit_scope) | Trade / compliance | 10 |
| 67 | [permit_usage](#permit_usage) | Trade / compliance | 9 |
| 68 | [requirement_version](#requirement_version) | Trade / compliance | 14 |
| 69 | [compliance_case](#compliance_case) | Trade / compliance | 11 |
| 70 | [compliance_check](#compliance_check) | Trade / compliance | 12 |
| 71 | [inventory_hold](#inventory_hold) | Trade / compliance | 12 |
| 72 | [approval_event](#approval_event) | Trade / compliance | 12 |
| 73 | [document_version](#document_version) | Trade / compliance | 12 |
| 74 | [audit_review](#audit_review) | Trade / compliance | 11 |
| 75 | [evidence_export](#evidence_export) | Trade / compliance | 9 |

## Open audit findings

1. Stock identity must include provenance_segment_id; the base table alone is superseded on that point by the trade addendum.
2. document.storage_key/sha256/original_name overlap immutable document_version content. Decide which fields identify a logical document versus a file version; file metadata should not drift independently.
3. organization_actor roles do not yet define permissions/site scopes. Do not call the current identity tables a complete authorization system.
4. establishment.address and audit_review.scope are underspecified; decide normalized address fields and relational review scope before implementation.
5. customs_declaration_line currently lists shipment_line_id, but the addendum requires many-to-many allocation support. declaration_line_allocation is not yet column-specified.
6. inventory_hold lacks an explicit event/allocation schema for release and partial quantities. The current row list alone cannot implement the stated hold behavior.
7. Item-classification approvals and permit versions must preserve historic facts; mutable row references alone are insufficient.
8. purchase_order_line requires supplier-code/description snapshots in prose but their final names/types are not specified. Add them during table review.
9. Provenance receipt-to-segment-to-bucket references form a creation dependency cycle. Resolve deferral/draft construction and constraints before DDL.
10. A global actor external_subject needs issuer/provider scoping if multiple identity providers are supported.
11. Core stock quantities, reservations, business permissions and compliance constraints require reviewed posting functions and tests in addition to column definitions.
12. Suppliers/customers need contact/address and relevant registration facts for document workflows. The current party table is intentionally incomplete.

## Detailed inventory

### organization

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `code` | text | required by draft convention |
| `name` | text | required by draft convention |
| `base_currency_code` | FK currency | required by draft convention |
| `display_timezone` | text | required by draft convention |

Rules to review: UQ code; timezone validated against PostgreSQL timezone names. Organization is a legal stock/accounting boundary.

### actor

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | bootstrap actor exception only |
| `display_name` | text | required by draft convention |
| `kind` | text (human/service) | required by draft convention |
| `external_subject` | text? | nullable in draft |
| `active` | boolean | required by draft convention |

Rules to review: UQ external_subject where present; service imports still have an actor. No password/secret storage in inventory tables.

### organization_actor

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `actor_id` | FK actor | required by draft convention |
| `role_code` | text | required by draft convention |
| `active` | boolean | required by draft convention |

Rules to review: UQ(org_id,actor_id,role_code); role permission details deferred.

### currency

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `code` | text PK | required by draft convention |
| `name` | text | required by draft convention |
| `minor_units` | smallint | required by draft convention |

Rules to review: Global reference table; minor_units >= 0. All currency_code fields reference code directly.

### uom

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | text | required by draft convention |
| `name` | text | required by draft convention |
| `dimension` | text | required by draft convention |
| `fractional_allowed` | boolean | required by draft convention |

Rules to review: UQ(org_id,code); examples each, mass, length.

### item

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `sku` | text | required by draft convention |
| `name` | text | required by draft convention |
| `description` | text? | nullable in draft |
| `base_uom_id` | FK uom | required by draft convention |
| `tracking_mode` | text (none/lot/serial) | required by draft convention |
| `expiry_required` | boolean | required by draft convention |
| `active` | boolean | required by draft convention |

Rules to review: UQ(org_id,sku). No quantity or invoice FK. Base unit and tracking mode cannot change after stock exists without a migration.

### item_uom

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `uom_id` | FK uom | required by draft convention |
| `factor_to_base` | numeric(24,10) | required by draft convention |
| `is_purchase_default` | boolean | required by draft convention |
| `is_sales_default` | boolean | required by draft convention |

Rules to review: UQ(org_id,item_id,uom_id); factor > 0, same dimension or explicit packaging conversion. Partial UQ for each default. Base item unit factor = 1.

### item_identifier

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `item_uom_id` | FK item_uom? | nullable in draft |
| `scheme` | text | required by draft convention |
| `value` | text | required by draft convention |

Rules to review: UQ(org_id,scheme,value); optional unit identifies a case barcode. Validate unit belongs to item.

### party

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | text | required by draft convention |
| `name` | text | required by draft convention |
| `active` | boolean | required by draft convention |

Rules to review: UQ(org_id,code); supplier/customer/manufacturer are roles, not duplicate party records.

### party_role

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `party_id` | FK party | required by draft convention |
| `role_code` | text (supplier/customer/manufacturer) | required by draft convention |

Rules to review: UQ(org_id,party_id,role_code).

### supplier_item

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `supplier_id` | FK party | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `supplier_sku` | text | required by draft convention |
| `purchase_item_uom_id` | FK item_uom | required by draft convention |
| `minimum_qty` | quantity? | nullable in draft |
| `order_multiple` | quantity? | nullable in draft |
| `lead_time_days` | integer? | nullable in draft |

Rules to review: UQ(org_id,supplier_id,supplier_sku); purchase unit belongs to item; positive quantities, nonnegative lead time. Multiple supplier codes may map to one item.

### supplier_price

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `supplier_item_id` | FK supplier_item | required by draft convention |
| `currency_code` | FK currency | required by draft convention |
| `minimum_qty` | quantity | required by draft convention |
| `unit_price` | money | required by draft convention |
| `valid_from` | date | required by draft convention |
| `valid_to` | date? | nullable in draft |

Rules to review: minimum_qty > 0, price >= 0, valid_to >= valid_from; reject overlapping effective periods for same supplier item/currency/quantity tier. Historical lines retain price snapshots.

### location

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | text | required by draft convention |
| `name` | text | required by draft convention |
| `parent_id` | FK location? | nullable in draft |
| `kind` | text (warehouse/bin/transit/external) | required by draft convention |
| `active` | boolean | required by draft convention |

Rules to review: UQ(org_id,code); no hierarchy cycles; only leaf locations hold stock. Transit is physically owned stock outside source/destination bins.

### stock_status

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | text | required by draft convention |
| `name` | text | required by draft convention |
| `allocatable` | boolean | required by draft convention |

Rules to review: UQ(org_id,code); available, quarantine, damaged, rejected. Allocation policy uses this flag.

### lot

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `internal_code` | text | required by draft convention |
| `manufacturer_id` | FK party? | nullable in draft |
| `manufacturer_lot` | text? | nullable in draft |
| `manufactured_on` | date? | nullable in draft |
| `expires_on` | date? | nullable in draft |

Rules to review: UQ(org_id,item_id,internal_code); expiry >= manufacture date when both known. Supplier is receipt provenance, not unique identity of the batch.

### serial

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `serial_number` | text | required by draft convention |
| `lot_id` | FK lot? | nullable in draft |

Rules to review: UQ(org_id,item_id,serial_number); lot must belong to item.

### stock_bucket

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `location_id` | FK location | required by draft convention |
| `status_id` | FK stock_status | required by draft convention |
| `owner_party_id` | FK party? | nullable in draft |
| `lot_id` | FK lot? | nullable in draft |
| `serial_id` | FK serial? | nullable in draft |
| `provenance_segment_id` | uuid FK provenance_segment | required for tracked trade; general policy under review |

Rules to review: UNIQUE NULLS NOT DISTINCT(org_id,item_id,location_id,status_id,owner_party_id,lot_id,serial_id). NULL owner means organization-owned; lots/serials must match item and serial lot. This is the stable lockable identity of a stock position. Trade addendum extends bucket identity with provenance_segment_id.

### stock_balance

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `bucket_id` | FK stock_bucket | required by draft convention |
| `on_hand_qty` | quantity | required by draft convention |
| `reserved_qty` | quantity | required by draft convention |
| `version` | bigint | required by draft convention |

Rules to review: UQ(org_id,bucket_id); 0 <= reserved <= on_hand; quantity nonnegative initially. Deliberate projection maintained atomically with ledger. Not a master-data field.

### inventory_transaction

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `kind` | text (receipt/issue/transfer/adjustment/production/return/status_change) | required by draft convention |
| `status` | text (draft/posted) | required by draft convention |
| `reason_code` | text | required by draft convention |
| `notes` | text? | nullable in draft |
| `occurred_at` | timestamptz | required by draft convention |
| `recorded_at` | timestamptz? | nullable in draft |
| `posted_by` | FK actor? | nullable in draft |
| `counterparty_id` | FK party? | nullable in draft |
| `reversal_of_id` | FK inventory_transaction? | nullable in draft |
| `request_key` | text | required by draft convention |
| `request_hash` | text | required by draft convention |

Rules to review: UQ(org_id,number), UQ(org_id,request_key), partial UQ(org_id,reversal_of_id) for full reversals. Bill is NOT required. Posted metadata required when posted; posted records immutable.

### inventory_line

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `transaction_id` | FK inventory_transaction | required by draft convention |
| `line_no` | integer | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `item_uom_id` | FK item_uom | required by draft convention |
| `entered_qty` | quantity | required by draft convention |
| `factor_to_base` | numeric(24,10) | required by draft convention |
| `base_qty` | quantity | required by draft convention |
| `source_bucket_id` | FK stock_bucket? | nullable in draft |
| `destination_bucket_id` | FK stock_bucket? | nullable in draft |

Rules to review: UQ(org_id,transaction_id,line_no), quantities > 0, factor > 0, base_qty = entered_qty * factor rounded under unit rules. At least one bucket; both must differ; item matches buckets and unit. This snapshots conversion used at posting.

### stock_ledger_entry

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `transaction_line_id` | FK inventory_line | required by draft convention |
| `bucket_id` | FK stock_bucket | required by draft convention |
| `side` | text (source/destination) | required by draft convention |
| `qty_delta` | quantity | required by draft convention |
| `posted_at` | timestamptz | required by draft convention |

Rules to review: UQ(org_id,transaction_line_id,side); source negative, destination positive; never zero. Append-only. Index(org_id,bucket_id,posted_at,id). Ledger contains posted lines only.

### reservation

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `requested_base_qty` | quantity | required by draft convention |
| `expires_at` | timestamptz? | nullable in draft |
| `status` | text (active/fulfilled/released/expired) | required by draft convention |
| `sales_order_line_id` | FK sales_order_line? | nullable in draft |
| `purpose` | text | required by draft convention |

Rules to review: UQ(org_id,number); requested quantity > 0. This is a demand header; does not change physical stock.

### reservation_allocation

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `reservation_id` | FK reservation | required by draft convention |
| `bucket_id` | FK stock_bucket | required by draft convention |
| `allocated_qty` | quantity | required by draft convention |
| `consumed_qty` | quantity | required by draft convention |
| `released_qty` | quantity | required by draft convention |

Rules to review: UQ(org_id,reservation_id,bucket_id); quantities >= 0, consumed + released <= allocated; outstanding = allocated - consumed - released. Balance reserved equals sum outstanding allocations.

### reservation_event

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `allocation_id` | FK reservation_allocation | required by draft convention |
| `event_type` | text | required by draft convention |
| `qty` | quantity | required by draft convention |
| `actor_id` | FK actor | required by draft convention |
| `occurred_at` | timestamptz | required by draft convention |
| `transaction_line_id` | FK inventory_line? | nullable in draft |

Rules to review: Append-only explanation of allocate/consume/release/expire. Consumption links to actual dispatch.

### document

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `kind` | text (bill/delivery_note/photo/count_sheet/other) | required by draft convention |
| `original_name` | text? | nullable in draft |
| `storage_key` | text? | nullable in draft |
| `sha256` | text? | nullable in draft |
| `document_date` | date? | nullable in draft |
| `reference` | text? | nullable in draft |

Rules to review: Document registry, not a bill-specific requirement. Attachment storage and access policy separate.

### transaction_document

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `transaction_id` | FK inventory_transaction | required by draft convention |
| `document_id` | FK document | required by draft convention |

Rules to review: UQ(org_id,transaction_id,document_id). A transaction can have zero documents.

### purchase_order

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `supplier_id` | FK party | required by draft convention |
| `status` | text | required by draft convention |
| `currency_code` | FK currency | required by draft convention |
| `ordered_on` | date | required by draft convention |
| `expected_on` | date? | nullable in draft |

Rules to review: UQ(org_id,number); order creates expectation, not stock.

### purchase_order_line

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `order_id` | FK purchase_order | required by draft convention |
| `line_no` | integer | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `supplier_item_id` | FK supplier_item? | nullable in draft |
| `item_uom_id` | FK item_uom | required by draft convention |
| `ordered_qty` | quantity | required by draft convention |
| `cancelled_qty` | quantity | required by draft convention |
| `factor_to_base` | numeric(24,10) | required by draft convention |
| `unit_price` | money? | nullable in draft |

Rules to review: UQ(org_id,order_id,line_no); quantity > 0, 0 <= cancelled <= ordered; snapshot supplier code and description in text columns for historical printing.

### receipt_order_allocation

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `inventory_line_id` | FK inventory_line | required by draft convention |
| `purchase_order_line_id` | FK purchase_order_line | required by draft convention |
| `base_qty` | quantity | required by draft convention |

Rules to review: UQ(org_id,inventory_line_id,purchase_order_line_id); quantity > 0. Supports partial/split receipts; lock order line when validating cumulative received quantity.

### supplier_bill

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `supplier_id` | FK party | required by draft convention |
| `supplier_invoice_number` | text? | nullable in draft |
| `invoice_date` | date? | nullable in draft |
| `currency_code` | FK currency | required by draft convention |
| `status` | text | required by draft convention |
| `total_amount` | money? | nullable in draft |
| `document_id` | FK document? | nullable in draft |

Rules to review: Partial UQ(org_id,supplier_id,supplier_invoice_number) when present, with explicit credit-note/duplicate exception policy deferred. Capturing an attachment is optional. No automatic quantity posting.

### supplier_bill_line

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `bill_id` | FK supplier_bill | required by draft convention |
| `line_no` | integer | required by draft convention |
| `item_id` | FK item? | nullable in draft |
| `description` | text | required by draft convention |
| `billed_qty` | quantity? | nullable in draft |
| `item_uom_id` | FK item_uom? | nullable in draft |
| `unit_price` | money? | nullable in draft |
| `line_amount` | money | required by draft convention |

Rules to review: UQ(org_id,bill_id,line_no); non-stock charges allowed. Item/UOM pairing consistency required when present.

### bill_receipt_allocation

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `bill_line_id` | FK supplier_bill_line | required by draft convention |
| `inventory_line_id` | FK inventory_line | required by draft convention |
| `base_qty` | quantity | required by draft convention |
| `allocated_amount` | money | required by draft convention |

Rules to review: UQ(org_id,bill_line_id,inventory_line_id); supports one bill to many receipts and vice versa. Matching compares bills and deliveries without changing received quantities.

### sales_order

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `customer_id` | FK party? | nullable in draft |
| `status` | text | required by draft convention |
| `ordered_at` | timestamptz | required by draft convention |

Rules to review: UQ(org_id,number); cash/direct dispatch may omit an order.

### sales_order_line

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `order_id` | FK sales_order | required by draft convention |
| `line_no` | integer | required by draft convention |
| `item_id` | FK item | required by draft convention |
| `item_uom_id` | FK item_uom | required by draft convention |
| `ordered_qty` | quantity | required by draft convention |
| `factor_to_base` | numeric(24,10) | required by draft convention |

Rules to review: UQ(org_id,order_id,line_no); positive quantity and factor.

### dispatch_order_allocation

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `inventory_line_id` | FK inventory_line | required by draft convention |
| `sales_order_line_id` | FK sales_order_line | required by draft convention |
| `base_qty` | quantity | required by draft convention |

Rules to review: UQ(org_id,inventory_line_id,sales_order_line_id); cumulative dispatch bounded under row lock.

### line_cost_estimate

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `inventory_line_id` | FK inventory_line | required by draft convention |
| `unit_cost` | money? | nullable in draft |
| `currency_code` | FK currency? | nullable in draft |
| `basis` | text (unknown/estimated/documented/zero_cost) | required by draft convention |
| `source_document_id` | FK document? | nullable in draft |

Rules to review: UQ(org_id,inventory_line_id); unknown => NULL cost/currency; other bases require cost >= 0 and currency; zero_cost => cost=0. Freeze on posting. Not the final accounting valuation ledger.

### valuation_event

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `inventory_line_id` | FK inventory_line | required by draft convention |
| `amount_base_currency` | money? | nullable in draft |
| `base_qty` | quantity | required by draft convention |
| `status` | text (pending/estimated/final) | required by draft convention |
| `method` | text? | nullable in draft |
| `effective_at` | timestamptz | required by draft convention |
| `reverses_id` | FK valuation_event? | nullable in draft |
| `bill_allocation_id` | FK bill_receipt_allocation? | nullable in draft |

Rules to review: Append-only; pending amount NULL; final amount not NULL. Revaluation adds events, not quantity. Full FIFO layers, consumption allocations, FX snapshots and landed-cost rules need a separate accounting design before authoritative valuation.

### stock_count

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `location_id` | FK location | required by draft convention |
| `status` | text | required by draft convention |
| `snapshot_at` | timestamptz? | nullable in draft |
| `completed_at` | timestamptz? | nullable in draft |

Rules to review: UQ(org_id,number); blind counting can hide expected quantities in UI.

### stock_count_line

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `count_id` | FK stock_count | required by draft convention |
| `bucket_id` | FK stock_bucket | required by draft convention |
| `expected_qty` | quantity | required by draft convention |
| `counted_qty` | quantity? | nullable in draft |
| `expected_balance_version` | bigint | required by draft convention |
| `adjustment_line_id` | FK inventory_line? | nullable in draft |

Rules to review: UQ(org_id,count_id,bucket_id); reject stale approval if balance version changed, or recount. Do not overwrite quantity with stale counted totals.

### quality_inspection

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `lot_id` | FK lot? | nullable in draft |
| `receipt_line_id` | FK inventory_line? | nullable in draft |
| `status` | text (pending/pass/fail) | required by draft convention |
| `inspected_by` | FK actor? | nullable in draft |
| `inspected_at` | timestamptz? | nullable in draft |
| `notes` | text? | nullable in draft |

Rules to review: At least one target; release via stock status-change transaction. Policy and evidence requirements are sector-specific.

### quality_result

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `inspection_id` | FK quality_inspection | required by draft convention |
| `test_code` | text | required by draft convention |
| `measured_value` | text? | nullable in draft |
| `result` | text | required by draft convention |
| `document_id` | FK document? | nullable in draft |

Rules to review: UQ(org_id,inspection_id,test_code); typed measurement limits deferred to sector module.

### bom

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `output_item_id` | FK item | required by draft convention |
| `revision` | text | required by draft convention |
| `output_base_qty` | quantity | required by draft convention |
| `status` | text | required by draft convention |

Rules to review: UQ(org_id,output_item_id,revision); output > 0; released revision immutable.

### bom_component

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `bom_id` | FK bom | required by draft convention |
| `line_no` | integer | required by draft convention |
| `component_item_id` | FK item | required by draft convention |
| `base_qty` | quantity | required by draft convention |
| `scrap_allowance` | numeric(10,6) | required by draft convention |

Rules to review: UQ(org_id,bom_id,line_no); quantity > 0, allowance >= 0; detect recursive BOM cycles.

### production_order

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | text | required by draft convention |
| `bom_id` | FK bom | required by draft convention |
| `planned_output_base_qty` | quantity | required by draft convention |
| `status` | text | required by draft convention |

Rules to review: UQ(org_id,number); positive output; exact released BOM revision preserved.

### production_posting

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `production_order_id` | FK production_order | required by draft convention |
| `transaction_id` | FK inventory_transaction | required by draft convention |

Rules to review: UQ(org_id,transaction_id); transaction lines distinguish consumption and outputs through their source/destination.

### production_genealogy

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `consumed_line_id` | FK inventory_line | required by draft convention |
| `output_line_id` | FK inventory_line | required by draft convention |
| `attributed_input_base_qty` | quantity | required by draft convention |

Rules to review: UQ(org_id,consumed_line_id,output_line_id); positive input, both in compatible production context. Links ingredient lots to outputs for traceability, not a compliance certification.

### entity_registry

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `entity_type` | text | required by draft convention |
| `retired_at` | timestamptz? | nullable in draft |

Rules to review: Shared integration identity. Integratable core rows use their id as FK to registry; deferred validation verifies registry type matches real row. Avoid unvalidated object_type/object_id pointers.

### integration_connection

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | text | required by draft convention |
| `provider` | text | required by draft convention |
| `external_company_id` | text? | nullable in draft |
| `authority_policy` | jsonb | required by draft convention |
| `enabled` | boolean | required by draft convention |
| `secret_reference` | text? | nullable in draft |

Rules to review: UQ(org_id,code); secrets outside tables; authority policy validated against a versioned schema.

### external_mapping

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `connection_id` | FK integration_connection | required by draft convention |
| `entity_id` | FK entity_registry | required by draft convention |
| `external_type` | text | required by draft convention |
| `external_id` | text | required by draft convention |
| `external_version` | text? | nullable in draft |
| `last_seen_at` | timestamptz? | nullable in draft |

Rules to review: UQ(org_id,connection_id,external_type,external_id), UQ(org_id,connection_id,entity_id,external_type). Merges/aliases need explicit policy, not accidental overwrites.

### integration_inbox

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `connection_id` | FK integration_connection | required by draft convention |
| `event_key` | text | required by draft convention |
| `payload_hash` | text | required by draft convention |
| `payload` | jsonb | required by draft convention |
| `status` | text | required by draft convention |
| `received_at` | timestamptz | required by draft convention |
| `processed_at` | timestamptz? | nullable in draft |
| `attempts` | integer | required by draft convention |
| `error_code` | text? | nullable in draft |

Rules to review: UQ(org_id,connection_id,event_key); same key/different hash is conflict; payload retention/redaction policy required.

### integration_outbox

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `entity_id` | FK entity_registry | required by draft convention |
| `event_type` | text | required by draft convention |
| `entity_version` | bigint | required by draft convention |
| `payload` | jsonb | required by draft convention |
| `occurred_at` | timestamptz | required by draft convention |

Rules to review: UQ(org_id,entity_id,entity_version,event_type); inserted with local business transaction.

### integration_delivery

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `outbox_id` | FK integration_outbox | required by draft convention |
| `connection_id` | FK integration_connection | required by draft convention |
| `status` | text | required by draft convention |
| `attempts` | integer | required by draft convention |
| `available_at` | timestamptz | required by draft convention |
| `lease_until` | timestamptz? | nullable in draft |
| `last_error` | text? | nullable in draft |
| `delivered_at` | timestamptz? | nullable in draft |

Rules to review: UQ(org_id,outbox_id,connection_id); independent delivery state per destination.

### audit_event

Source: [database-schema.md](database-schema.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `actor_id` | FK actor | required by draft convention |
| `entity_id` | FK entity_registry? | nullable in draft |
| `action` | text | required by draft convention |
| `request_id` | text | required by draft convention |
| `occurred_at` | timestamptz | required by draft convention |
| `changes` | jsonb | required by draft convention |

Rules to review: Append-only, restrict access; redact credentials/PII; not a substitute for quantity ledger.

### establishment

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | type not specified in source draft | not specified; review required |
| `location_id` | type not specified in source draft | not specified; review required |
| `legal_name` | type not specified in source draft | not specified; review required |
| `address` | type not specified in source draft | not specified; review required |
| `jurisdiction_code` | type not specified in source draft | not specified; review required |

Rules to review: History/versioning for the actual operating premises; hierarchy and registration applicability reviewed

### business_registration

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `establishment_id` | type not specified in source draft | nullable in draft |
| `party_id` | type not specified in source draft | nullable in draft |
| `registration_type` | type not specified in source draft | not specified; review required |
| `identifier` | type not specified in source draft | not specified; review required |
| `jurisdiction_code` | type not specified in source draft | not specified; review required |
| `valid_from` | type not specified in source draft | not specified; review required |
| `valid_to` | type not specified in source draft | nullable in draft |
| `status` | type not specified in source draft | not specified; review required |
| `evidence_document_id` | type not specified in source draft | nullable in draft |

Rules to review: Exactly one registration subject; retain historical validity, do not treat any number as proof of current validity

### item_classification

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | type not specified in source draft | not specified; review required |
| `jurisdiction_code` | type not specified in source draft | not specified; review required |
| `scheme` | type not specified in source draft | not specified; review required |
| `code` | type not specified in source draft | not specified; review required |
| `effective_from` | type not specified in source draft | not specified; review required |
| `effective_to` | type not specified in source draft | nullable in draft |
| `reviewed_by` | type not specified in source draft | not specified; review required |
| `evidence_document_id` | type not specified in source draft | nullable in draft |

Rules to review: Different national tariff/controlled-product classifications can coexist; classification requires qualified review

### trade_shipment

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `number` | type not specified in source draft | not specified; review required |
| `direction` | type not specified in source draft | not specified; review required |
| `origin_country` | type not specified in source draft | not specified; review required |
| `destination_country` | type not specified in source draft | not specified; review required |
| `importer_party_id` | type not specified in source draft | not specified; review required |
| `exporter_party_id` | type not specified in source draft | not specified; review required |
| `consignee_party_id` | type not specified in source draft | nullable in draft |
| `customs_regime` | type not specified in source draft | not specified; review required |
| `incoterm_code` | type not specified in source draft | nullable in draft |
| `incoterm_version` | type not specified in source draft | nullable in draft |
| `named_place` | type not specified in source draft | nullable in draft |
| `currency_code` | type not specified in source draft | not specified; review required |
| `version` | type not specified in source draft | not specified; review required |

Rules to review: Internal shipment is not a filing. Incoterm is commercial allocation information, not automatic proof of origin, ownership or clearance

### trade_shipment_line

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `shipment_id` | type not specified in source draft | not specified; review required |
| `line_no` | type not specified in source draft | not specified; review required |
| `item_id` | type not specified in source draft | not specified; review required |
| `quantity` | type not specified in source draft | not specified; review required |
| `item_uom_id` | type not specified in source draft | not specified; review required |
| `base_qty` | type not specified in source draft | not specified; review required |
| `origin_country` | type not specified in source draft | nullable in draft |
| `classification_id` | type not specified in source draft | not specified; review required |

Rules to review: Snapshot approved classification/version; origin is not necessarily supplier country or ship-from country

### shipment_stock_allocation

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `shipment_line_id` | type not specified in source draft | not specified; review required |
| `inventory_line_id` | type not specified in source draft | not specified; review required |
| `provenance_segment_id` | type not specified in source draft | not specified; review required |
| `base_qty` | type not specified in source draft | not specified; review required |

Rules to review: Supports partial and split shipments; locked cumulative allocations cannot exceed stock/line quantities

### provenance_segment

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `item_id` | type not specified in source draft | not specified; review required |
| `lot_id` | type not specified in source draft | nullable in draft |
| `owner_party_id` | type not specified in source draft | nullable in draft |
| `originating_receipt_line_id` | type not specified in source draft | not specified; review required |
| `customs_regime` | type not specified in source draft | not specified; review required |
| `origin_evidence_document_id` | type not specified in source draft | nullable in draft |
| `predecessor_segment_id` | type not specified in source draft | nullable in draft |

Rules to review: Stable provenance identity; same lot from different import treatments is not merged implicitly

### customs_declaration

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `shipment_id` | type not specified in source draft | not specified; review required |
| `declaration_type` | type not specified in source draft | not specified; review required |
| `reference` | type not specified in source draft | not specified; review required |
| `port_code` | type not specified in source draft | not specified; review required |
| `declaration_date` | type not specified in source draft | not specified; review required |
| `version` | type not specified in source draft | not specified; review required |
| `external_mapping_id` | type not specified in source draft | nullable in draft |
| `evidence_document_id` | type not specified in source draft | nullable in draft |

Rules to review: Bill of Entry/shipping bill scoped by authority/port/date as needed; exact unique identifier contract defined per integration

### customs_declaration_line

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `declaration_id` | type not specified in source draft | not specified; review required |
| `line_no` | type not specified in source draft | not specified; review required |
| `shipment_line_id` | type not specified in source draft | not specified; review required |
| `declared_base_qty` | type not specified in source draft | not specified; review required |
| `assessed_value` | type not specified in source draft | nullable in draft |
| `currency_code` | type not specified in source draft | not specified; review required |

Rules to review: Matching must support multiple line allocations before implementation if declaration and commercial lines differ

### customs_release_event

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `declaration_line_id` | type not specified in source draft | not specified; review required |
| `released_base_qty` | type not specified in source draft | not specified; review required |
| `action_scope` | type not specified in source draft | not specified; review required |
| `occurred_at` | type not specified in source draft | not specified; review required |
| `source_authority` | type not specified in source draft | not specified; review required |
| `evidence_document_id` | type not specified in source draft | not specified; review required |
| `supersedes_id` | type not specified in source draft | nullable in draft |

Rules to review: Append-only release/revocation history. Partial quantities retained; effective balance cannot exceed declared quantity

### shipment_document

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `shipment_id` | type not specified in source draft | not specified; review required |
| `shipment_line_id` | type not specified in source draft | nullable in draft |
| `document_version_id` | type not specified in source draft | not specified; review required |
| `document_role` | type not specified in source draft | not specified; review required |

Rules to review: Transport document, commercial invoice, packing list, certificate or permit are distinct roles

### permit

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `registration_id` | type not specified in source draft | nullable in draft |
| `permit_type` | type not specified in source draft | not specified; review required |
| `reference` | type not specified in source draft | not specified; review required |
| `jurisdiction_code` | type not specified in source draft | not specified; review required |
| `valid_from` | type not specified in source draft | not specified; review required |
| `valid_to` | type not specified in source draft | nullable in draft |
| `evidence_document_id` | type not specified in source draft | not specified; review required |
| `status` | type not specified in source draft | not specified; review required |

Rules to review: Scope through normalized permit_scope rows; different licences have different quantitative limits

### permit_scope

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `permit_id` | type not specified in source draft | not specified; review required |
| `item_id` | type not specified in source draft | nullable in draft |
| `origin_country` | type not specified in source draft | nullable in draft |
| `destination_country` | type not specified in source draft | nullable in draft |
| `permitted_base_qty` | type not specified in source draft | nullable in draft |
| `uom_id` | type not specified in source draft | nullable in draft |

Rules to review: Explicit scope; quantity has a defined item/unit basis; no meaningless total across incompatible goods

### permit_usage

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `permit_scope_id` | type not specified in source draft | not specified; review required |
| `shipment_line_id` | type not specified in source draft | not specified; review required |
| `base_qty` | type not specified in source draft | not specified; review required |
| `usage_type` | type not specified in source draft | not specified; review required |
| `reversal_of_id` | type not specified in source draft | nullable in draft |

Rules to review: Append-only consumption/release, locked cumulative limits; no double spending across concurrent shipments

### requirement_version

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `code` | type not specified in source draft | not specified; review required |
| `revision` | type not specified in source draft | not specified; review required |
| `jurisdiction_code` | type not specified in source draft | not specified; review required |
| `authority_url` | type not specified in source draft | not specified; review required |
| `effective_from` | type not specified in source draft | not specified; review required |
| `effective_to` | type not specified in source draft | nullable in draft |
| `applicability_schema_version` | type not specified in source draft | not specified; review required |
| `definition` | jsonb | not specified; review required |
| `status` | type not specified in source draft | not specified; review required |
| `approved_by` | type not specified in source draft | not specified; review required |

Rules to review: Immutable published rules, validated schema, human-reviewed applicability; no autonomous legal rule generation

### compliance_case

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `shipment_id` | type not specified in source draft | nullable in draft |
| `inventory_transaction_id` | type not specified in source draft | nullable in draft |
| `case_type` | type not specified in source draft | not specified; review required |
| `status` | type not specified in source draft | not specified; review required |
| `assigned_actor_id` | type not specified in source draft | not specified; review required |
| `subject_version` | type not specified in source draft | not specified; review required |
| `subject_hash` | type not specified in source draft | not specified; review required |

Rules to review: Explicitly constrained target; scope is company-consistent and relevant to action

### compliance_check

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `case_id` | type not specified in source draft | not specified; review required |
| `requirement_version_id` | type not specified in source draft | not specified; review required |
| `action_scope` | type not specified in source draft | not specified; review required |
| `outcome` | (pass/fail/unknown/not_applicable) | not specified; review required |
| `evaluated_at` | type not specified in source draft | not specified; review required |
| `valid_until` | type not specified in source draft | nullable in draft |
| `evaluated_subject_hash` | type not specified in source draft | not specified; review required |
| `evidence_document_version_id` | type not specified in source draft | nullable in draft |

Rules to review: Append-only evaluation snapshots; not_applicable requires rationale; changed scope/data invalidates reuse

### inventory_hold

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `provenance_segment_id` | type not specified in source draft | nullable in draft |
| `lot_id` | type not specified in source draft | nullable in draft |
| `shipment_line_id` | type not specified in source draft | nullable in draft |
| `hold_type` | type not specified in source draft | not specified; review required |
| `reason` | type not specified in source draft | not specified; review required |
| `effective_at` | type not specified in source draft | not specified; review required |
| `imposed_by` | type not specified in source draft | not specified; review required |
| `source_check_id` | type not specified in source draft | nullable in draft |

Rules to review: Explicit target and propagation rules; hold event history for impose/release; scoped quantity allocation table if hold is partial

### approval_event

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `case_id` | type not specified in source draft | not specified; review required |
| `decision` | type not specified in source draft | not specified; review required |
| `actor_id` | type not specified in source draft | not specified; review required |
| `role_at_decision` | type not specified in source draft | not specified; review required |
| `reason` | type not specified in source draft | not specified; review required |
| `decided_at` | type not specified in source draft | not specified; review required |
| `subject_hash` | type not specified in source draft | not specified; review required |
| `evidence_document_version_id` | type not specified in source draft | nullable in draft |

Rules to review: Maker/checker where required; approval bound to exact facts, cannot approve a changed shipment accidentally

### document_version

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `document_id` | type not specified in source draft | not specified; review required |
| `version_no` | type not specified in source draft | not specified; review required |
| `storage_key` | type not specified in source draft | not specified; review required |
| `content_hash` | type not specified in source draft | not specified; review required |
| `recorded_at` | type not specified in source draft | not specified; review required |
| `supersedes_id` | type not specified in source draft | nullable in draft |
| `source` | type not specified in source draft | not specified; review required |
| `verification_status` | type not specified in source draft | not specified; review required |

Rules to review: Immutable original files and versions; deleting/replacing an attachment must not rewrite evidence

### audit_review

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `scope` | type not specified in source draft | not specified; review required |
| `period_from` | type not specified in source draft | not specified; review required |
| `period_to` | type not specified in source draft | not specified; review required |
| `reviewer_id` | type not specified in source draft | not specified; review required |
| `reviewed_at` | type not specified in source draft | not specified; review required |
| `finding_count` | type not specified in source draft | not specified; review required |
| `report_document_version_id` | type not specified in source draft | not specified; review required |

Rules to review: Shows actual audit review rather than merely having logs; full finding linkage before implementation

### evidence_export

Source: [compliance-and-trade.md](compliance-and-trade.md). Status: proposed.

| Column | Declared type / reference | Nullability |
| --- | --- | --- |
| `id` | uuid PK | required by draft convention |
| `created_at` | timestamptz | required by draft convention |
| `created_by` | uuid FK actor | required by draft convention |
| `org_id` | uuid FK organization | required by draft convention |
| `case_id` | type not specified in source draft | nullable in draft |
| `requested_by` | type not specified in source draft | not specified; review required |
| `snapshot_hash` | type not specified in source draft | not specified; review required |
| `manifest_storage_key` | type not specified in source draft | not specified; review required |
| `format_version` | type not specified in source draft | not specified; review required |

Rules to review: Reproducible case pack with scoped movements, documents, decisions and external acknowledgements

## Deferred structures without audited columns

- declaration_line_allocation
- hold events and partial hold allocations
- many-input provenance genealogy
- audit findings and review scopes
- role permissions and site scopes
- valuation layers, FX and landed costs
- retention policies and legal holds

These are known design work, not implemented tables. Do not infer complete compliance, permissions or accounting coverage from this inventory.

## Regenerate

Run `python scripts/build_schema_audit.py` after editing the two source dictionaries. Review the generated diff. No database credentials or server are used.

<!-- reading-sequence:start -->
[Previous: Database schema proposal](database-schema.md) | [Next: Posting and ERP integration](posting-and-integration.md)
<!-- reading-sequence:end -->
