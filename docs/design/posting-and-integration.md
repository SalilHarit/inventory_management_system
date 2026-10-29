# Posting, concurrency and ERP contracts

<!-- reading-sequence:start -->
[Previous: Table relationships](table-relationships.md) | [Next: Compliance and trade design](compliance-and-trade.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Schema proposal](database-schema.md) | [Trade design](compliance-and-trade.md)

Status: proposed behavior; not yet implemented or concurrency-tested. PostgreSQL 17 references: [row locks and deadlocks](https://www.postgresql.org/docs/17/explicit-locking.html), [constraints and NULL uniqueness](https://www.postgresql.org/docs/17/ddl-constraints.html), [transaction isolation](https://www.postgresql.org/docs/17/transaction-iso.html), [SELECT locking / SKIP LOCKED](https://www.postgresql.org/docs/17/sql-select.html), [INSERT / ON CONFLICT](https://www.postgresql.org/docs/17/sql-insert.html).

## Physical posting transaction

1. Begin transaction. Authenticate actor and organization. Claim UNIQUE(org_id,request_key); compare a canonical request hash, stored alongside request_key on inventory_transaction. Same key + different request must fail, not silently reuse a receipt. Same key + same request returns prior result.
2. Lock the draft header FOR UPDATE. Reject already posted drafts unless returning the idempotent result. All draft edits must acquire this same header lock and check status/version, including child-line edits. This prevents edits racing with posting.
3. Validate lines, conversions, dates, location/status policies and organization/item/lot/serial coherence. Receipt can have no supplier, bill, order, attachment or known cost. Tracking rules remain independent.
4. Gather all relevant serial rows and lock them in UUID order. Create/resolve stock buckets using the natural UNIQUE NULLS NOT DISTINCT key. Insert missing stock_balance rows with ON CONFLICT DO NOTHING in deterministic bucket order, then lock all affected balances FOR UPDATE in that order. Other posting/reservation/count routines must use the same lock hierarchy.
5. Lock demand, purchase/sales order lines and reservation allocations under one documented global order. Within each category sort by ID. Validate total receipt/dispatch allocations and reservations under locks. Initial implementation may serialize posting per organization if the finer lock hierarchy is not yet proven correct; measure before optimizing.
6. Calculate all deltas. Require nonnegative physical stock and reserved <= physical. An ordinary issue can consume only unreserved stock. A reserved dispatch atomically reduces allocation outstanding, balance reserved and on-hand. Status changes/transfer cannot strand reservations. Block expired/quarantined stock from allocation/dispatch according to item policy.
7. Write negative source and positive destination ledger entries. Internal transfers have equal-and-opposite quantity in the same item/base unit. Receipts have one positive leg; issues one negative leg; production has separate input/output lines with BOM and genealogy validation. Do not impose cross-item quantity conservation on manufacturing.
8. Update balances and version numbers. Mark header posted and write recorded_at/actor, audit and outbox events in the SAME transaction. Commit. Any failure rolls everything back, including stock and outbox.

No network calls while holding stock locks. No read-then-write stock check outside the transaction. READ COMMITTED plus consistent explicit locks and uniqueness is the initial proposal; SERIALIZABLE is an alternative requiring whole-transaction retries. Retry deadlocks (40P01) and serialization failures (40001) with bounded backoff, preserving idempotency key. Business validation failures are not automatically retried.

No application role may bypass posting by directly editing ledger or balance tables. Implement restricted DML grants plus stored posting routines (carefully secured search_path if SECURITY DEFINER), or an equivalent trusted transaction boundary. Triggers reject UPDATE/DELETE of posted headers/lines/ledger and invalid inserts referencing posted history. Deferred constraint triggers enforce exact ledger legs and balanced transfers at commit. Merely adding CHECK(status='posted') cannot inspect another row.

## Normalization and relational constraints

- Use PKs and named FKs/UQs/CHECKs, not string lookups. Add child indexes on FK paths used in joins/deletion checks; PostgreSQL does not automatically index every referencing FK.
- All organization-owned parents expose UNIQUE(org_id,id). Composite FKs prevent cross-company links. Role checks still determine whether an actor can operate in that organization.
- Add UNIQUE(org_id,item_id,id) to item_uom, lot, serial and stock_bucket where needed; use matching composite FKs to enforce item coherence. Validate serial-to-lot coherence as well. A FK on item_id and a separate FK on lot_id do not prove they describe the same item.
- UNIQUE NULLS NOT DISTINCT avoids duplicate untracked buckets where lot/serial/owner is NULL. Do not rely on default UNIQUE NULL behavior.
- Item quantities and supplier lists do not live in JSON or comma-separated strings. Input unit, conversion and price snapshots are deliberate historical facts, not accidental duplicates of current master values.
- on_hand and reserved balances are deliberate projections. Reconcile ledger sum to on_hand, and allocation outstanding sum to reserved. Unexpected drift blocks affected positions and requires investigation; never silently overwrite history.
- Master data is deactivated, not cascade-deleted through history. FK deletion defaults should be RESTRICT for referenced business records.
- Reserve serial and tracked-stock invariants for cross-row enforcement under locks/constraint triggers. CHECK constraints alone cannot enforce cross-row totals or absence of hierarchy cycles.

## Corrections, transfers and stock counts

Posted mistakes get an explicit reversal linked to original; original remains visible. Full reversal only initially; partial corrections use separate explicit adjustment/return transactions. Reversal must revalidate stock and reservations, so already-dispatched receipts cannot simply be reversed into negative stock.

Inter-warehouse transit is two postings: source -> transit, then transit -> destination. Partial arrivals leave the remainder in transit. A transfer/order linkage extension is needed before implementing long-running shipment tracking; don't disguise it as an instantaneous transfer. Transit stock is not allocatable to normal customer orders.

Count approval locks relevant balances and checks captured version. If stock moved since the count snapshot, require recount or an explicitly designed movement-aware reconciliation. The initial version rejects stale approvals. Counter identity and approval actor remain traceable.

Reservation expiration locks the reservation/allocation and balances, rechecks status, and releases only remaining outstanding quantity. Dispatch and expiration racing must have one consistent winner. The expiry worker cannot just decrement a cached reserved quantity without allocation history.

## ERP integration boundaries

Internal UUIDs never depend on ERP identifiers. external_mapping scopes external IDs to connection, object type and company. Do not assume an ERP invoice number is globally unique.

For each connector specify an authority matrix: e.g. ERP owns supplier accounting details and bills; IMS owns physical stock and reservations; product catalog authority is explicitly selected. Avoid reciprocal updates that loop. Include origin system and causation/correlation IDs in integration envelopes; add schema_version and aggregate version to outbox payloads.

Inbound events are stored with provider event ID and canonical payload hash. Processing locks an inbox row and applies mappings/business posting transactionally; its completion marker must commit with local changes. Duplicate delivery is harmless; different payload under same event ID is a visible conflict. If provider has no stable event ID, define a source-specific deduplication key, never assume timestamp alone suffices.

Outbox is committed alongside stock changes. Workers claim delivery rows using FOR UPDATE SKIP LOCKED, set leases and commit before making HTTP calls. On success acknowledge delivery; on failure retry with backoff and expose errors. A crash after remote success but before acknowledgement causes redelivery, so delivery is AT LEAST ONCE. Send stable idempotency keys where the receiver supports them; otherwise reconcile before retrying unsafe writes.

Per-destination delivery rows prevent one successful connector hiding another failed connector. Preserve aggregate ordering using entity version and serialized delivery per entity/connection, or require receiver version checks. Poison messages go to a visible failed state with operator replay, not endless silent retries. Missing dependencies are deferred, not fabricated.

Reconcile counts, external IDs, stock balances and bills on a schedule. Expose last successful sync, unresolved mismatch and retry state. Full exports must include internal IDs, external mappings, quantities, tracking and history. Do not promise instantaneous or exactly-once cross-system synchronization.

## Required verification before implementation is accepted

1. Two concurrent dispatches of 4 from stock 5: exactly one succeeds; balance 1.
2. Concurrent reservations of 4 from stock 5: exactly one succeeds; outstanding <= on-hand.
3. Duplicate receipt request/event: one receipt and one set of ledger legs. Same key/different payload rejected.
4. Opposite-direction transfers under contention: atomic and no drift; deadlock retries bounded.
5. Same physical serial received into different locations concurrently: only one valid position.
6. New NULL-tracking bucket created concurrently: exactly one bucket/balance.
7. Posting failure after ledger insert: no partial ledger, balances, posted status or outbox.
8. Draft edits racing with posting: either edit included before post, or rejected after post.
9. Late supplier bill matching: no quantity movement; unknown cost distinguishable from zero.
10. Bill-free and bill-attached receipt: equivalent physical results, same posting path.
11. Cross-organization/item/lot references rejected by database enforcement.
12. Concurrent count approval and movement: stale count rejected, no lost movement.
13. Dispatch racing with reservation expiry: quantity consumed or released once, never both.
14. Outbox crash after remote success: duplicate remote effect prevented or surfaced for reconciliation.
15. Manufacturing input/output and lot genealogy preserved; quarantine cannot be allocated as released stock.

These are test specifications, not claims of passing tests.

<!-- reading-sequence:start -->
[Previous: Table relationships](table-relationships.md) | [Next: Compliance and trade design](compliance-and-trade.md)
<!-- reading-sequence:end -->
