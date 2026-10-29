# PostgreSQL schema proposal v0.1

<!-- reading-sequence:start -->
[Previous: Table discussions](table-discussions.md) | [Next: Table and column audit](schema-audit.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Table audit](schema-audit.md) | [Posting and integration](posting-and-integration.md) | [Trade design](compliance-and-trade.md)

Date: 2026-10-28. Status: design dictionary, NOT an applied migration or production-ready implementation. Grounding: [upstream schema research](../research/existing-system-schemas.md). Concurrency and cross-row invariants are specified in [posting contract](posting-and-integration.md).

The [compliance and trade addendum](compliance-and-trade.md) extends this draft with independent holds, provenance segments in stock identity, shipment/declaration allocations and versioned evidence. Read it before implementing stock_bucket or a single status-based eligibility rule.

See the [table relationship diagrams](table-relationships.md) for a visual overview of the proposed entities and their links.

## Scope and conventions

One shared stock core across industries. Modules add purchasing, manufacturing and quality without requiring a bill for receipt. A tracked item is a distinct SKU/variant, not a free-text bill description. The proposal targets PostgreSQL 17, whose client is available locally; server configuration is unverified.

Notation below: PK primary key, FK foreign key, UQ unique, ? nullable. Except currency, every table has id uuid PK, created_at timestamptz, created_by uuid FK actor (nullable only for bootstrap actor). All tables except organization, actor and currency also have org_id uuid NOT NULL FK organization and UNIQUE(org_id,id). Provision the bootstrap actor first. Referenced organization-owned rows use composite FK (org_id, referenced_id). Currency is a global reference table with code text PK and no org_id. Mutable master records and draft headers additionally have updated_at timestamptz, updated_by actor and version bigint NOT NULL DEFAULT 1. These common columns are omitted from rows below. Immutable tables do not carry editable update metadata.

Quantity: numeric(24,8); monetary unit cost: numeric(24,10); money: numeric(24,8); currency_code: text FK currency. All numeric values must be finite (reject PostgreSQL numeric NaN and infinities); precision/rounding is validated before posting. Dates use date; moments use timestamptz. IDs are internal; human document numbers and ERP identifiers are separate. Use text with CHECK or reference tables for finite code sets, not unexplained magic integers. No stock quantities use floating point.

## Identity and shared catalog

| Table | Business columns | Keys / rules |
| --- | --- | --- |
| organization | code text, name text, base_currency_code FK currency, display_timezone text | UQ code; timezone validated against PostgreSQL timezone names. Organization is a legal stock/accounting boundary. |
| actor | display_name text, kind text (human/service), external_subject text?, active boolean | UQ external_subject where present; service imports still have an actor. No password/secret storage in inventory tables. |
| organization_actor | actor_id FK actor, role_code text, active boolean | UQ(org_id,actor_id,role_code); role permission details deferred. |
| currency | code text PK, name text, minor_units smallint | Global reference table; minor_units >= 0. All currency_code fields reference code directly. |
| uom | code text, name text, dimension text, fractional_allowed boolean | UQ(org_id,code); examples each, mass, length. |
| item | sku text, name text, description text?, base_uom_id FK uom, tracking_mode text (none/lot/serial), expiry_required boolean, active boolean | UQ(org_id,sku). No quantity or invoice FK. Base unit and tracking mode cannot change after stock exists without a migration. |
| item_uom | item_id FK item, uom_id FK uom, factor_to_base numeric(24,10), is_purchase_default boolean, is_sales_default boolean | UQ(org_id,item_id,uom_id); factor > 0, same dimension or explicit packaging conversion. Partial UQ for each default. Base item unit factor = 1. |
| item_identifier | item_id FK item, item_uom_id FK item_uom?, scheme text, value text | UQ(org_id,scheme,value); optional unit identifies a case barcode. Validate unit belongs to item. |
| party | code text, name text, active boolean | UQ(org_id,code); supplier/customer/manufacturer are roles, not duplicate party records. |
| party_role | party_id FK party, role_code text (supplier/customer/manufacturer) | UQ(org_id,party_id,role_code). |
| supplier_item | supplier_id FK party, item_id FK item, supplier_sku text, purchase_item_uom_id FK item_uom, minimum_qty quantity?, order_multiple quantity?, lead_time_days integer? | UQ(org_id,supplier_id,supplier_sku); purchase unit belongs to item; positive quantities, nonnegative lead time. Multiple supplier codes may map to one item. |
| supplier_price | supplier_item_id FK supplier_item, currency_code FK currency, minimum_qty quantity, unit_price money, valid_from date, valid_to date? | minimum_qty > 0, price >= 0, valid_to >= valid_from; reject overlapping effective periods for same supplier item/currency/quantity tier. Historical lines retain price snapshots. |

Global currencies are reference data, not organization-owned business records. Unit definitions remain organization-scoped because packaging and operating conventions can differ.

## Locations, tracking and physical stock

| Table | Business columns | Keys / rules |
| --- | --- | --- |
| location | code text, name text, parent_id FK location?, kind text (warehouse/bin/transit/external), active boolean | UQ(org_id,code); no hierarchy cycles; only leaf locations hold stock. Transit is physically owned stock outside source/destination bins. |
| stock_status | code text, name text, allocatable boolean | UQ(org_id,code); available, quarantine, damaged, rejected. Allocation policy uses this flag. |
| lot | item_id FK item, internal_code text, manufacturer_id FK party?, manufacturer_lot text?, manufactured_on date?, expires_on date? | UQ(org_id,item_id,internal_code); expiry >= manufacture date when both known. Supplier is receipt provenance, not unique identity of the batch. |
| serial | item_id FK item, serial_number text, lot_id FK lot? | UQ(org_id,item_id,serial_number); lot must belong to item. |
| stock_bucket | item_id FK item, location_id FK location, status_id FK stock_status, owner_party_id FK party?, lot_id FK lot?, serial_id FK serial? | UNIQUE NULLS NOT DISTINCT(org_id,item_id,location_id,status_id,owner_party_id,lot_id,serial_id). NULL owner means organization-owned; lots/serials must match item and serial lot. This is the stable lockable identity of a stock position. |
| stock_balance | bucket_id FK stock_bucket, on_hand_qty quantity, reserved_qty quantity, version bigint | UQ(org_id,bucket_id); 0 <= reserved <= on_hand; quantity nonnegative initially. Deliberate projection maintained atomically with ledger. Not a master-data field. |
| inventory_transaction | number text, kind text (receipt/issue/transfer/adjustment/production/return/status_change), status text (draft/posted), reason_code text, notes text?, occurred_at timestamptz, recorded_at timestamptz?, posted_by FK actor?, counterparty_id FK party?, reversal_of_id FK inventory_transaction?, request_key text, request_hash text | UQ(org_id,number), UQ(org_id,request_key), partial UQ(org_id,reversal_of_id) for full reversals. Bill is NOT required. Posted metadata required when posted; posted records immutable. |
| inventory_line | transaction_id FK inventory_transaction, line_no integer, item_id FK item, item_uom_id FK item_uom, entered_qty quantity, factor_to_base numeric(24,10), base_qty quantity, source_bucket_id FK stock_bucket?, destination_bucket_id FK stock_bucket? | UQ(org_id,transaction_id,line_no), quantities > 0, factor > 0, base_qty = entered_qty * factor rounded under unit rules. At least one bucket; both must differ; item matches buckets and unit. This snapshots conversion used at posting. |
| stock_ledger_entry | transaction_line_id FK inventory_line, bucket_id FK stock_bucket, side text (source/destination), qty_delta quantity, posted_at timestamptz | UQ(org_id,transaction_line_id,side); source negative, destination positive; never zero. Append-only. Index(org_id,bucket_id,posted_at,id). Ledger contains posted lines only. |
| reservation | number text, item_id FK item, requested_base_qty quantity, expires_at timestamptz?, status text (active/fulfilled/released/expired), sales_order_line_id FK sales_order_line?, purpose text | UQ(org_id,number); requested quantity > 0. This is a demand header; does not change physical stock. |
| reservation_allocation | reservation_id FK reservation, bucket_id FK stock_bucket, allocated_qty quantity, consumed_qty quantity, released_qty quantity | UQ(org_id,reservation_id,bucket_id); quantities >= 0, consumed + released <= allocated; outstanding = allocated - consumed - released. Balance reserved equals sum outstanding allocations. |
| reservation_event | allocation_id FK reservation_allocation, event_type text, qty quantity, actor_id FK actor, occurred_at timestamptz, transaction_line_id FK inventory_line? | Append-only explanation of allocate/consume/release/expire. Consumption links to actual dispatch. |

Serialized stock requires a serial-position guard: lock serial row and enforce total owned physical quantity across buckets <= 1, each movement integral and of quantity 1. A per-bucket CHECK alone cannot enforce uniqueness across locations. Lot tracking/expiry and allocatable status policies must be checked by the posting routine. A bill is never a substitute for lot/expiry data where that item's policy requires it.

## Optional documents, purchasing and sales

All receiving uses inventory_transaction + inventory_line. Users can optionally attach a bill, order, photo, opening-count evidence, or other document directly in that same form; absence is accepted. Optional links are not separate receipt workflows.

| Table | Business columns | Keys / rules |
| --- | --- | --- |
| document | kind text (bill/delivery_note/photo/count_sheet/other), original_name text?, storage_key text?, sha256 text?, document_date date?, reference text? | Document registry, not a bill-specific requirement. Attachment storage and access policy separate. |
| transaction_document | transaction_id FK inventory_transaction, document_id FK document | UQ(org_id,transaction_id,document_id). A transaction can have zero documents. |
| purchase_order | number text, supplier_id FK party, status text, currency_code FK currency, ordered_on date, expected_on date? | UQ(org_id,number); order creates expectation, not stock. |
| purchase_order_line | order_id FK purchase_order, line_no integer, item_id FK item, supplier_item_id FK supplier_item?, item_uom_id FK item_uom, ordered_qty quantity, cancelled_qty quantity, factor_to_base numeric(24,10), unit_price money? | UQ(org_id,order_id,line_no); quantity > 0, 0 <= cancelled <= ordered; snapshot supplier code and description in text columns for historical printing. |
| receipt_order_allocation | inventory_line_id FK inventory_line, purchase_order_line_id FK purchase_order_line, base_qty quantity | UQ(org_id,inventory_line_id,purchase_order_line_id); quantity > 0. Supports partial/split receipts; lock order line when validating cumulative received quantity. |
| supplier_bill | supplier_id FK party, supplier_invoice_number text?, invoice_date date?, currency_code FK currency, status text, total_amount money?, document_id FK document? | Partial UQ(org_id,supplier_id,supplier_invoice_number) when present, with explicit credit-note/duplicate exception policy deferred. Capturing an attachment is optional. No automatic quantity posting. |
| supplier_bill_line | bill_id FK supplier_bill, line_no integer, item_id FK item?, description text, billed_qty quantity?, item_uom_id FK item_uom?, unit_price money?, line_amount money | UQ(org_id,bill_id,line_no); non-stock charges allowed. Item/UOM pairing consistency required when present. |
| bill_receipt_allocation | bill_line_id FK supplier_bill_line, inventory_line_id FK inventory_line, base_qty quantity, allocated_amount money | UQ(org_id,bill_line_id,inventory_line_id); supports one bill to many receipts and vice versa. Matching compares bills and deliveries without changing received quantities. |
| sales_order | number text, customer_id FK party?, status text, ordered_at timestamptz | UQ(org_id,number); cash/direct dispatch may omit an order. |
| sales_order_line | order_id FK sales_order, line_no integer, item_id FK item, item_uom_id FK item_uom, ordered_qty quantity, factor_to_base numeric(24,10) | UQ(org_id,order_id,line_no); positive quantity and factor. |
| dispatch_order_allocation | inventory_line_id FK inventory_line, sales_order_line_id FK sales_order_line, base_qty quantity | UQ(org_id,inventory_line_id,sales_order_line_id); cumulative dispatch bounded under row lock. |

Unknown supplier, absent original invoice and unknown cost are independent facts. None requires fake values. Bills can be added and matched later without rewriting a posted quantity transaction. Inventory with incomplete provenance still obeys sector-specific receiving/hold policy.

## Valuation, counts and sector extensions

| Table | Business columns | Keys / rules |
| --- | --- | --- |
| line_cost_estimate | inventory_line_id FK inventory_line, unit_cost money?, currency_code FK currency?, basis text (unknown/estimated/documented/zero_cost), source_document_id FK document? | UQ(org_id,inventory_line_id); unknown => NULL cost/currency; other bases require cost >= 0 and currency; zero_cost => cost=0. Freeze on posting. Not the final accounting valuation ledger. |
| valuation_event | inventory_line_id FK inventory_line, amount_base_currency money?, base_qty quantity, status text (pending/estimated/final), method text?, effective_at timestamptz, reverses_id FK valuation_event?, bill_allocation_id FK bill_receipt_allocation? | Append-only; pending amount NULL; final amount not NULL. Revaluation adds events, not quantity. Full FIFO layers, consumption allocations, FX snapshots and landed-cost rules need a separate accounting design before authoritative valuation. |
| stock_count | number text, location_id FK location, status text, snapshot_at timestamptz?, completed_at timestamptz? | UQ(org_id,number); blind counting can hide expected quantities in UI. |
| stock_count_line | count_id FK stock_count, bucket_id FK stock_bucket, expected_qty quantity, counted_qty quantity?, expected_balance_version bigint, adjustment_line_id FK inventory_line? | UQ(org_id,count_id,bucket_id); reject stale approval if balance version changed, or recount. Do not overwrite quantity with stale counted totals. |
| quality_inspection | lot_id FK lot?, receipt_line_id FK inventory_line?, status text (pending/pass/fail), inspected_by FK actor?, inspected_at timestamptz?, notes text? | At least one target; release via stock status-change transaction. Policy and evidence requirements are sector-specific. |
| quality_result | inspection_id FK quality_inspection, test_code text, measured_value text?, result text, document_id FK document? | UQ(org_id,inspection_id,test_code); typed measurement limits deferred to sector module. |
| bom | output_item_id FK item, revision text, output_base_qty quantity, status text | UQ(org_id,output_item_id,revision); output > 0; released revision immutable. |
| bom_component | bom_id FK bom, line_no integer, component_item_id FK item, base_qty quantity, scrap_allowance numeric(10,6) | UQ(org_id,bom_id,line_no); quantity > 0, allowance >= 0; detect recursive BOM cycles. |
| production_order | number text, bom_id FK bom, planned_output_base_qty quantity, status text | UQ(org_id,number); positive output; exact released BOM revision preserved. |
| production_posting | production_order_id FK production_order, transaction_id FK inventory_transaction | UQ(org_id,transaction_id); transaction lines distinguish consumption and outputs through their source/destination. |
| production_genealogy | consumed_line_id FK inventory_line, output_line_id FK inventory_line, attributed_input_base_qty quantity | UQ(org_id,consumed_line_id,output_line_id); positive input, both in compatible production context. Links ingredient lots to outputs for traceability, not a compliance certification. |

## Integration and audit

| Table | Business columns | Keys / rules |
| --- | --- | --- |
| entity_registry | entity_type text, retired_at timestamptz? | Shared integration identity. Integratable core rows use their id as FK to registry; deferred validation verifies registry type matches real row. Avoid unvalidated object_type/object_id pointers. |
| integration_connection | code text, provider text, external_company_id text?, authority_policy jsonb, enabled boolean, secret_reference text? | UQ(org_id,code); secrets outside tables; authority policy validated against a versioned schema. |
| external_mapping | connection_id FK integration_connection, entity_id FK entity_registry, external_type text, external_id text, external_version text?, last_seen_at timestamptz? | UQ(org_id,connection_id,external_type,external_id), UQ(org_id,connection_id,entity_id,external_type). Merges/aliases need explicit policy, not accidental overwrites. |
| integration_inbox | connection_id FK integration_connection, event_key text, payload_hash text, payload jsonb, status text, received_at timestamptz, processed_at timestamptz?, attempts integer, error_code text? | UQ(org_id,connection_id,event_key); same key/different hash is conflict; payload retention/redaction policy required. |
| integration_outbox | entity_id FK entity_registry, event_type text, entity_version bigint, payload jsonb, occurred_at timestamptz | UQ(org_id,entity_id,entity_version,event_type); inserted with local business transaction. |
| integration_delivery | outbox_id FK integration_outbox, connection_id FK integration_connection, status text, attempts integer, available_at timestamptz, lease_until timestamptz?, last_error text?, delivered_at timestamptz? | UQ(org_id,outbox_id,connection_id); independent delivery state per destination. |
| audit_event | actor_id FK actor, entity_id FK entity_registry?, action text, request_id text, occurred_at timestamptz, changes jsonb | Append-only, restrict access; redact credentials/PII; not a substitute for quantity ledger. |

Entity registry is a proposal to preserve FK-backed generic integration references. Typed mapping tables are a simpler alternative if initial integrations cover only a few entity types. Registry implementation requires deferred constraint triggers; this dictionary does not pretend an ordinary FK can verify a discriminator.

## Native input form mapped to tables

Always visible: item, quantity, unit, location, condition/status, occurrence date, reason and notes. Actor comes from authenticated session. Optional in the same form: supplier, purchase order, bill reference/upload, cost/basis, lot/serial where relevant. Lot/serial/expiry requirements derive from item policy, not whether a bill exists.

Saving a draft creates header and lines only. Posting writes ledger and balance changes atomically. A no-bill entry produces exactly the same ledger shape as an otherwise identical entry with a bill. Later bill matching adds links and valuation information, not another receipt.

## Implementation boundary

This dictionary includes planned extension tables; it is not a demand to implement every module immediately. Initial migration should implement identity, catalog, locations, transaction/ledger/balances, optional documents and idempotent posting first. Purchasing, reservations, ERP delivery, valuation and sector modules follow behind explicit acceptance tests. Resolve registry approach before DDL. No migration should be called safe until same-company/item constraints, permissions, posting and concurrency tests pass.

<!-- reading-sequence:start -->
[Previous: Table discussions](table-discussions.md) | [Next: Table and column audit](schema-audit.md)
<!-- reading-sequence:end -->
