# Proposed table relationships

<!-- reading-sequence:start -->
[Previous: Table and column audit](schema-audit.md) | [Next: Posting and ERP integration](posting-and-integration.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Table and column audit](schema-audit.md) | [Schema proposal](database-schema.md) | [Trade design](compliance-and-trade.md)

These diagrams describe the **proposed design**, not an applied PostgreSQL schema. They are split by domain and show selected identifiers and relationships. For the complete column inventory, see the [table and column audit](schema-audit.md). The [posting contract](posting-and-integration.md) describes concurrency and business invariants that diagrams alone cannot enforce.

In Mermaid notation, `||` means exactly one, `o|` zero or one, and `o{` zero or many. Each line describes a relationship in both directions: for example, `organization ||--o{ item` means one organization can have many items, and each item belongs to exactly one organization. Optionality and cardinalities are draft interpretations of the dictionary, not verified constraints. Links to common `org_id`, `created_by` and other shared metadata are omitted from most diagrams to keep them readable; organization-owned foreign keys are intended to include `org_id` for cross-organization integrity. Currency is global.

## 1. Organization, catalog and suppliers

`party` represents an organization or individual in a business relationship. `party_role` records whether it acts as a supplier, customer or manufacturer. An item can have different supplier codes and units without duplicating its internal SKU.

```mermaid
erDiagram
    organization ||--o{ organization_actor : has
    actor ||--o{ organization_actor : assigned
    currency ||--o{ organization : base_currency
    organization ||--o{ item : owns
    organization ||--o{ uom : defines
    organization ||--o{ party : registers
    uom ||--o{ item : base_unit
    item ||--o{ item_uom : supports
    uom ||--o{ item_uom : identifies
    item ||--o{ item_identifier : has
    item_uom o|--o{ item_identifier : labels
    party ||--o{ party_role : has
    party ||--o{ supplier_item : supplies
    item ||--o{ supplier_item : sourced_as
    item_uom ||--o{ supplier_item : purchase_unit
    supplier_item ||--o{ supplier_price : priced_at
    currency ||--o{ supplier_price : denominates

    organization {
        uuid id PK
        string code
        string name
        string base_currency_code FK
    }
    actor {
        uuid id PK
        string display_name
        string kind
    }
    organization_actor {
        uuid id PK
        uuid org_id FK
        uuid actor_id FK
        string role_code
    }
    currency {
        string code PK
        string name
    }
    uom {
        uuid id PK
        string code
        string dimension
    }
    item {
        uuid id PK
        string sku
        uuid base_uom_id FK
        string tracking_mode
    }
    item_uom {
        uuid id PK
        uuid item_id FK
        uuid uom_id FK
        decimal factor_to_base
    }
    item_identifier {
        uuid id PK
        uuid item_id FK
        uuid item_uom_id FK
        string value
    }
    party {
        uuid id PK
        string code
        string name
    }
    party_role {
        uuid id PK
        uuid party_id FK
        string role_code
    }
    supplier_item {
        uuid id PK
        uuid supplier_id FK
        uuid item_id FK
        string supplier_sku
    }
    supplier_price {
        uuid id PK
        uuid supplier_item_id FK
        decimal unit_price
    }

    classDef readable color:#6683a6
    class organization,actor,organization_actor,currency,uom,item,item_uom,item_identifier,party,party_role,supplier_item,supplier_price readable
```

## 2. Physical stock, movements and reservations

`stock_bucket` identifies a position; `stock_balance` is a maintained projection; `stock_ledger_entry` records posted movements. Source and destination buckets are optional separately, but a line needs at least one. An internal transfer needs both. A `provenance_segment` keeps stock with distinct provenance or customs treatment from being merged; its creation cycle with receipt lines is unresolved.

```mermaid
erDiagram
    location o|--o{ location : parent_of
    item ||--o{ lot : tracked_by
    item ||--o{ serial : identified_by
    lot o|--o{ serial : contains
    item ||--o{ stock_bucket : held_as
    location ||--o{ stock_bucket : stores
    stock_status ||--o{ stock_bucket : categorizes
    party o|--o{ stock_bucket : owns
    lot o|--o{ stock_bucket : identifies
    serial o|--o{ stock_bucket : identifies
    provenance_segment o|--o{ stock_bucket : qualifies
    stock_bucket ||--o| stock_balance : has
    inventory_transaction ||--o{ inventory_line : contains
    item ||--o{ inventory_line : moved
    item_uom ||--o{ inventory_line : entered_in
    stock_bucket o|--o{ inventory_line : source
    stock_bucket o|--o{ inventory_line : destination
    inventory_line ||--o{ stock_ledger_entry : posts
    stock_bucket ||--o{ stock_ledger_entry : affects
    item ||--o{ reservation : requested_for
    reservation ||--o{ reservation_allocation : allocates
    stock_bucket ||--o{ reservation_allocation : provides
    reservation_allocation ||--o{ reservation_event : records
    inventory_line o|--o{ reservation_event : consumes

    location {
        uuid id PK
        uuid parent_id FK
        string kind
    }
    stock_status {
        uuid id PK
        string code
        boolean allocatable
    }
    lot {
        uuid id PK
        uuid item_id FK
        string internal_code
    }
    serial {
        uuid id PK
        uuid item_id FK
        uuid lot_id FK
    }
    provenance_segment {
        uuid id PK
        uuid originating_receipt_line_id FK
        string customs_regime
    }
    stock_bucket {
        uuid id PK
        uuid item_id FK
        uuid location_id FK
        uuid provenance_segment_id FK
    }
    stock_balance {
        uuid id PK
        uuid bucket_id FK
        decimal on_hand_qty
        decimal reserved_qty
    }
    inventory_transaction {
        uuid id PK
        string number
        string kind
        string status
    }
    inventory_line {
        uuid id PK
        uuid transaction_id FK
        uuid source_bucket_id FK
        uuid destination_bucket_id FK
        decimal base_qty
    }
    stock_ledger_entry {
        uuid id PK
        uuid transaction_line_id FK
        uuid bucket_id FK
        decimal qty_delta
    }
    reservation {
        uuid id PK
        uuid item_id FK
        decimal requested_base_qty
    }
    reservation_allocation {
        uuid id PK
        uuid reservation_id FK
        uuid bucket_id FK
    }
    reservation_event {
        uuid id PK
        uuid allocation_id FK
        decimal qty
    }

    classDef readable color:#6683a6
    class location,stock_status,lot,serial,provenance_segment,stock_bucket,stock_balance,inventory_transaction,inventory_line,stock_ledger_entry,reservation,reservation_allocation,reservation_event readable
```

**Provenance note:** the addendum requires a segment for tracked trade stock and proposes an ordinary segment for domestic stock. The base dictionary originally made no such link. Whether every bucket must have a segment, and how an opening or produced segment is created, remains under review; the diagram uses the most permissive unresolved cardinality.

## 3. Orders, optional bills and documents

A receipt line can be linked to an order and a bill later. A physical transaction can exist without any bill or document. Allocation tables support partial and split matching.

```mermaid
erDiagram
    party ||--o{ purchase_order : supplier
    purchase_order ||--o{ purchase_order_line : contains
    item ||--o{ purchase_order_line : ordered
    supplier_item o|--o{ purchase_order_line : sourced_as
    purchase_order_line ||--o{ receipt_order_allocation : matched
    inventory_line ||--o{ receipt_order_allocation : received
    party ||--o{ supplier_bill : issues
    supplier_bill ||--o{ supplier_bill_line : contains
    item o|--o{ supplier_bill_line : billed
    supplier_bill_line ||--o{ bill_receipt_allocation : matched
    inventory_line ||--o{ bill_receipt_allocation : received
    document o|--o{ supplier_bill : supports
    inventory_transaction ||--o{ transaction_document : references
    document ||--o{ transaction_document : attached
    document ||--o{ document_version : versioned
    party o|--o{ sales_order : customer
    sales_order ||--o{ sales_order_line : contains
    item ||--o{ sales_order_line : ordered
    sales_order_line o|--o{ reservation : requested_for
    sales_order_line ||--o{ dispatch_order_allocation : matched
    inventory_line ||--o{ dispatch_order_allocation : dispatched

    purchase_order {
        uuid id PK
        uuid supplier_id FK
        string number
    }
    purchase_order_line {
        uuid id PK
        uuid order_id FK
        uuid item_id FK
        decimal ordered_qty
    }
    receipt_order_allocation {
        uuid id PK
        uuid inventory_line_id FK
        uuid purchase_order_line_id FK
    }
    supplier_bill {
        uuid id PK
        uuid supplier_id FK
        uuid document_id FK
    }
    supplier_bill_line {
        uuid id PK
        uuid bill_id FK
        uuid item_id FK
    }
    bill_receipt_allocation {
        uuid id PK
        uuid bill_line_id FK
        uuid inventory_line_id FK
    }
    document {
        uuid id PK
        string kind
        string reference
    }
    document_version {
        uuid id PK
        uuid document_id FK
        string content_hash
    }
    transaction_document {
        uuid id PK
        uuid transaction_id FK
        uuid document_id FK
    }
    sales_order {
        uuid id PK
        uuid customer_id FK
        string number
    }
    sales_order_line {
        uuid id PK
        uuid order_id FK
        uuid item_id FK
    }
    dispatch_order_allocation {
        uuid id PK
        uuid inventory_line_id FK
        uuid sales_order_line_id FK
    }

    classDef readable color:#6683a6
    class purchase_order,purchase_order_line,receipt_order_allocation,supplier_bill,supplier_bill_line,bill_receipt_allocation,document,document_version,transaction_document,sales_order,sales_order_line,dispatch_order_allocation readable
```

Document file metadata overlaps between `document` and `document_version`; the final boundary needs review before implementation.

## 4. Counts, valuation, quality and manufacturing

Production consumption and output use inventory lines. `production_genealogy` links inputs to outputs, while the longer-term segment-level lineage needed for cross-border cases still requires design. The separate `quality_inspection` targets are optional individually, with at least one required.

```mermaid
erDiagram
    inventory_line ||--o| line_cost_estimate : has
    inventory_line ||--o{ valuation_event : valued_by
    bill_receipt_allocation o|--o{ valuation_event : supports
    location ||--o{ stock_count : counted_at
    stock_count ||--o{ stock_count_line : contains
    stock_bucket ||--o{ stock_count_line : counted
    inventory_line o|--o{ stock_count_line : adjusts
    lot o|--o{ quality_inspection : inspected
    inventory_line o|--o{ quality_inspection : received
    quality_inspection ||--o{ quality_result : includes
    item ||--o{ bom : output
    bom ||--o{ bom_component : contains
    item ||--o{ bom_component : input
    bom ||--o{ production_order : planned_from
    production_order ||--o{ production_posting : posts
    inventory_transaction ||--o| production_posting : represents
    inventory_line ||--o{ production_genealogy : consumed_input
    inventory_line ||--o{ production_genealogy : produced_output

    line_cost_estimate {
        uuid id PK
        uuid inventory_line_id FK
        string basis
    }
    valuation_event {
        uuid id PK
        uuid inventory_line_id FK
        decimal amount_base_currency
    }
    stock_count {
        uuid id PK
        uuid location_id FK
        string status
    }
    stock_count_line {
        uuid id PK
        uuid count_id FK
        uuid bucket_id FK
        decimal counted_qty
    }
    quality_inspection {
        uuid id PK
        uuid lot_id FK
        uuid receipt_line_id FK
        string status
    }
    quality_result {
        uuid id PK
        uuid inspection_id FK
        string test_code
    }
    bom {
        uuid id PK
        uuid output_item_id FK
        string revision
    }
    bom_component {
        uuid id PK
        uuid bom_id FK
        uuid component_item_id FK
    }
    production_order {
        uuid id PK
        uuid bom_id FK
        string status
    }
    production_posting {
        uuid id PK
        uuid production_order_id FK
        uuid transaction_id FK
    }
    production_genealogy {
        uuid id PK
        uuid consumed_line_id FK
        uuid output_line_id FK
    }

    classDef readable color:#6683a6
    class line_cost_estimate,valuation_event,stock_count,stock_count_line,quality_inspection,quality_result,bom,bom_component,production_order,production_posting,production_genealogy readable
```

## 5. ERP integration and audit

Mappings connect internal identities to external IDs. Inbound events and outbound deliveries support retries and reconciliation; they do not guarantee exactly-once delivery. The generic `entity_registry` is a proposed design choice and remains open to review.

```mermaid
erDiagram
    integration_connection ||--o{ external_mapping : maps
    entity_registry ||--o{ external_mapping : identifies
    integration_connection ||--o{ integration_inbox : receives
    entity_registry ||--o{ integration_outbox : emits
    integration_outbox ||--o{ integration_delivery : delivered_as
    integration_connection ||--o{ integration_delivery : receives
    entity_registry o|--o{ audit_event : concerns
    actor ||--o{ audit_event : performs

    entity_registry {
        uuid id PK
        string entity_type
    }
    integration_connection {
        uuid id PK
        string provider
        uuid external_company_id FK
    }
    external_mapping {
        uuid id PK
        uuid connection_id FK
        uuid entity_id FK
        uuid external_id FK
    }
    integration_inbox {
        uuid id PK
        uuid connection_id FK
        string event_key
        string payload_hash
    }
    integration_outbox {
        uuid id PK
        uuid entity_id FK
        bigint entity_version
    }
    integration_delivery {
        uuid id PK
        uuid outbox_id FK
        uuid connection_id FK
        string status
    }
    audit_event {
        uuid id PK
        uuid actor_id FK
        uuid entity_id FK
        string action
    }

    classDef readable color:#6683a6
    class entity_registry,integration_connection,external_mapping,integration_inbox,integration_outbox,integration_delivery,audit_event readable
```

## 6. Shipments, customs and permits

Classification, registration and clearance are shipment- and jurisdiction-dependent. A customs declaration is evidence about a shipment; a document or stock receipt alone does not establish clearance. The direct declaration-line-to-shipment-line relationship below reflects the present draft, but must be replaced or extended with an allocation table where many-to-many matching is needed.

```mermaid
erDiagram
    location ||--o{ establishment : represents
    establishment o|--o{ business_registration : holds
    party o|--o{ business_registration : holds
    item ||--o{ item_classification : classified_as
    party ||--o{ trade_shipment : importer
    party ||--o{ trade_shipment : exporter
    party o|--o{ trade_shipment : consignee
    trade_shipment ||--o{ trade_shipment_line : contains
    item ||--o{ trade_shipment_line : shipped
    item_classification ||--o{ trade_shipment_line : classified_by
    trade_shipment_line ||--o{ shipment_stock_allocation : allocates
    inventory_line ||--o{ shipment_stock_allocation : records
    provenance_segment ||--o{ shipment_stock_allocation : traces
    inventory_line ||--o{ provenance_segment : originates
    trade_shipment ||--o{ customs_declaration : declared_by
    customs_declaration ||--o{ customs_declaration_line : contains
    trade_shipment_line ||--o{ customs_declaration_line : declared
    customs_declaration_line ||--o{ customs_release_event : released_by
    trade_shipment ||--o{ shipment_document : references
    trade_shipment_line o|--o{ shipment_document : scopes
    document_version ||--o{ shipment_document : evidences
    business_registration o|--o{ permit : supports
    permit ||--o{ permit_scope : defines
    permit_scope ||--o{ permit_usage : records
    trade_shipment_line ||--o{ permit_usage : uses

    establishment {
        uuid id PK
        uuid location_id FK
        string legal_name
    }
    business_registration {
        uuid id PK
        uuid establishment_id FK
        uuid party_id FK
        string identifier
    }
    item_classification {
        uuid id PK
        uuid item_id FK
        string jurisdiction_code
        string code
    }
    trade_shipment {
        uuid id PK
        string direction
        string origin_country
        string destination_country
    }
    trade_shipment_line {
        uuid id PK
        uuid shipment_id FK
        uuid item_id FK
        uuid classification_id FK
    }
    shipment_stock_allocation {
        uuid id PK
        uuid shipment_line_id FK
        uuid inventory_line_id FK
        uuid provenance_segment_id FK
    }
    customs_declaration {
        uuid id PK
        uuid shipment_id FK
        string declaration_type
    }
    customs_declaration_line {
        uuid id PK
        uuid declaration_id FK
        uuid shipment_line_id FK
    }
    customs_release_event {
        uuid id PK
        uuid declaration_line_id FK
        decimal released_base_qty
    }
    shipment_document {
        uuid id PK
        uuid shipment_id FK
        uuid document_version_id FK
    }
    permit {
        uuid id PK
        uuid registration_id FK
        string permit_type
    }
    permit_scope {
        uuid id PK
        uuid permit_id FK
        decimal permitted_base_qty
    }
    permit_usage {
        uuid id PK
        uuid permit_scope_id FK
        uuid shipment_line_id FK
    }

    classDef readable color:#6683a6
    class establishment,business_registration,item_classification,trade_shipment,trade_shipment_line,shipment_stock_allocation,customs_declaration,customs_declaration_line,customs_release_event,shipment_document,permit,permit_scope,permit_usage readable
```

`business_registration` has two optional subject references, with exactly one required by the proposal. Receipt provenance for opening stock and production output needs clarification; the displayed origin relationship is the current draft, not a settled universal requirement.

## 7. Compliance cases, holds and review evidence

A compliance case can reference a shipment or a physical transaction. Checks, approvals and holds are scoped records; no single status represents all quality, customs and documentation requirements. Hold event history, partial quantities and detailed auditor findings remain unspecific in the draft.

```mermaid
erDiagram
    trade_shipment o|--o{ compliance_case : reviewed_for
    inventory_transaction o|--o{ compliance_case : reviewed_for
    compliance_case ||--o{ compliance_check : evaluated_by
    requirement_version ||--o{ compliance_check : applies
    document_version o|--o{ compliance_check : evidence
    compliance_case ||--o{ approval_event : approved_by
    actor ||--o{ approval_event : decides
    document_version o|--o{ approval_event : evidence
    compliance_check o|--o{ inventory_hold : triggers
    provenance_segment o|--o{ inventory_hold : restricted
    lot o|--o{ inventory_hold : restricted
    trade_shipment_line o|--o{ inventory_hold : restricted
    document_version ||--o{ audit_review : reports
    compliance_case o|--o{ evidence_export : assembled_from

    requirement_version {
        uuid id PK
        string code
        string revision
        string jurisdiction_code
    }
    compliance_case {
        uuid id PK
        uuid shipment_id FK
        uuid inventory_transaction_id FK
        string status
    }
    compliance_check {
        uuid id PK
        uuid case_id FK
        uuid requirement_version_id FK
        string outcome
    }
    inventory_hold {
        uuid id PK
        uuid provenance_segment_id FK
        uuid lot_id FK
        uuid shipment_line_id FK
        string hold_type
    }
    approval_event {
        uuid id PK
        uuid case_id FK
        uuid actor_id FK
        string decision
    }
    audit_review {
        uuid id PK
        uuid report_document_version_id FK
        string scope
    }
    evidence_export {
        uuid id PK
        uuid case_id FK
        string snapshot_hash
    }

    classDef readable color:#6683a6
    class requirement_version,compliance_case,compliance_check,inventory_hold,approval_event,audit_review,evidence_export readable
```

## Relationship decisions still open

- **Authorization:** role assignments exist, but permissions and site scope tables are not yet specified.
- **Provenance cycle:** a receipt line, its provenance segment and its destination bucket can depend on each other; define creation order and constraints before migration.
- **Documents:** resolve duplicated file fields between logical documents and immutable versions.
- **Customs allocation:** define the many-to-many declaration-line allocation table, quantities and keys; the current direct link is provisional.
- **Holds:** define event history, releases, partial quantities and concurrency guards before relying on holds.
- **Manufacturing lineage:** decide how multiple consumed provenance segments map to output segments without assuming automatic country-of-origin conclusions.
- **Audit coverage:** common audit fields and business-event actors have different possible meanings; the full immutable audit/control model is not settled.
- **Cardinality and nullability:** trade and compliance proposals contain incomplete details. Review them table by table before treating these diagrams as executable constraints.

<!-- reading-sequence:start -->
[Previous: Table and column audit](schema-audit.md) | [Next: Posting and ERP integration](posting-and-integration.md)
<!-- reading-sequence:end -->
