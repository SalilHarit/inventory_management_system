# IMS product goal

<!-- reading-sequence:start -->
[Previous: Documentation index](README.md) | [Next: Stakeholders and workflows](research/stakeholders-and-operational-workflows.md)
<!-- reading-sequence:end -->

[Documentation index](README.md) | [Project home](../README.md) | [Stakeholder research](research/stakeholders-and-operational-workflows.md) | [Decisions](decisions/decision-register.md)

Date: 2026-10-28. Status: proposed product definition grounded in confirmed project direction and initial research. Business impact and adoption hypotheses require validation with operators; no pilot results exist yet.

## Goal

### Problem statement

Small and midsize businesses with several people handling inventory struggle to maintain a shared, explainable view of physical stock and its eligibility for use or dispatch. Information is split across inventory screens, spreadsheets, documents, staff knowledge and connected systems. At handoffs, people must search, re-enter, reconcile or ask someone else before acting. This creates avoidable delays, stock commitments that cannot be fulfilled, unnecessary purchases and difficult investigations.

This is the working problem hypothesis supported by initial desk research, not a claim that every business experiences every failure. Missing paperwork, units, reservations, quality/customs restrictions and stale integrations are different causes that must remain distinguishable.

### Outcome and product promise

Enable the person doing the work to record it accurately, the next person to act on an understandable stock position, and a supervisor or auditor to reconstruct what happened and why.

Working product promise: **Know what exists, what can be used, what needs attention, and why.**

### Primary job to be done

When goods arrive, move, become committed, are consumed or leave, help me record the facts and understand the remaining eligible quantity without reconstructing the answer across tools and colleagues—so the next operational decision is timely and defensible.

### Where the problem is concentrated

The proposed initial adoption profile has multiple inventory participants and repeated handoffs: receiving to storage, purchasing to finance, stock to sales/production, and operators to supervisors/reviewers. Existing tooling may be a spreadsheet, an IMS or an ERP. Prioritize demonstrated reconciliation and exception-handling burden over company size or sector labels alone. Occasional single-user lists may not justify the workflow overhead; advanced regulated deployments require capabilities beyond the initial shared loop.

### Solution approach

1. Capture physical reality through one consistent stock-entry model, with optional bills and honest unknowns.
2. Maintain explainable stock positions: quantity, unit, location, ownership, commitments and applicable independent holds.
3. Support role-specific actions and handoffs: capture, execute, supervise, view, review and administer, with clear ownership of unresolved exceptions.
4. Preserve history and evidence across corrections, documents, approvals and ERP synchronization.
5. Add reviewed sector and jurisdiction controls where applicable; completion of a software record never substitutes for the underlying authorization.

### Product boundaries

The first proposed release addresses dependable physical stock control and its operational handoffs. It does not promise to replace all ERP/accounting functions, predict all demand, or certify legal compliance across industries and countries. Open source and PostgreSQL support inspectability, integration and local control; they are implementation/delivery choices rather than the customer problem. Existing products already offer many individual capabilities; our coherent workflow and ease-of-operation advantage still needs user validation.

### Prioritization rule

Before adding a feature, identify the user, concrete trigger, failed decision or handoff, current workaround, business consequence and measurable improvement. Prefer a small complete workflow over broad feature coverage. Classify evidence as observed directly, reported by a user, documented capability or hypothesis. Preserve positive feedback and distinguish configuration/training problems from missing functionality.

The sections below retain the detailed user map, candidate behaviors, scope and measurement plan supporting this framing.

Help small and midsize businesses know what stock they have, where it is, what they can use or promise, and why it changed—so they can fulfill demand with fewer shortages, avoidable purchases and manual reconciliations.

Support the inventory businesses actually possess, including items without original bills, while preserving honest uncertainty about cost and provenance. Make the shared core usable across sectors, with additional tracking requirements enabled where needed.

Also help users establish which actions are permitted and produce the evidence behind those decisions. The user selected India-based businesses trading internationally as the first jurisdictional context. Physical presence, quality release, customs clearance, documentation and commercial availability remain separate facts. Receiving without an original bill remains native; it does not establish lawful tax treatment or permission to use/export goods. See [India research](research/india-compliance-and-trade.md) and [compliance design](design/compliance-and-trade.md).

## Business problem

Inventory decisions become unreliable when physical stock, spreadsheets, staff knowledge and ERP records disagree. Staff then spend time recounting, looking for goods, checking with colleagues, and reconstructing movements before purchasing, shipping or starting production. A quantity alone is insufficient: goods can be reserved, damaged, expired, awaiting inspection or moving between sites.

Initial research found contextual reports of sync lag, reservation difficulties, reporting workarounds, unclear adjustments and supplier-code friction. See [research context and source links](decisions/decision-register.md). These reports support investigation, not a claim that every business has these problems or every competing product lacks a solution.

## Who we serve

The [stakeholder and operational-workflow research](research/stakeholders-and-operational-workflows.md) distinguishes actual role-attributed review signals, documented software workflows and unvalidated role hypotheses. Role-specific access and everyday handoffs should shape the UI; an industry label alone is insufficient.

The cross-sector audience is confirmed. The proposed first adoption profile is a business with multiple people receiving, moving or issuing stock, currently struggling to reconcile its records, and willing to establish consistent recording practices. Employee count or sector alone is not an eligibility rule.

| User | Decision they need to make | Useful outcome |
| --- | --- | --- |
| Owner / operations manager | Can we trust our stock and identify unresolved discrepancies? | Less time investigating and clearer accountability |
| Storekeeper / warehouse operator | What arrived, where should it go, and what can leave? | Quick, accurate receiving, movement and dispatch |
| Purchasing staff | What do we need, what is already ordered, and from whom? | Fewer duplicate or emergency purchases |
| Sales / fulfillment staff | What can we promise without using someone else's reservation? | Fewer stock-related cancellations and delays |
| Production staff | Which materials are available and which lots became finished goods? | Clear consumption, output and traceability |
| Quality staff | What is held, rejected or released? | Physical presence does not imply permission to use |
| Trade/compliance staff | Are this route, item, party and quantity covered by current evidence and permissions? | Explainable holds and fewer unresolved shipment exceptions |
| Auditor / internal reviewer | Can we reconstruct decisions, corrections and operating controls? | Retrievable evidence across inventory, quality, trade and ERP records |
| Finance / ERP administrator | How do physical receipts relate to bills and external records? | Explainable differences and fewer duplicate entries |

## How the product addresses the problem

| Business failure | Product behavior | How it helps | What to measure |
| --- | --- | --- | --- |
| Existing stock cannot be entered because paperwork is missing | Same receiving/stock-entry form with optional bill, supplier, attachment and cost | Business can establish a stock record immediately without inventing documents or prices | Successful no-bill entries; entry time; unresolved unknown-cost quantities |
| Different staff report different quantities | Record receipts, issues, transfers, returns and corrections in a traceable movement history | Shared quantities can be explained and checked against physical counts | Count agreement; discrepancy investigation time |
| Goods on shelves are already committed or unusable | Separate on-hand, reserved, available, transit and held/damaged states | Staff make promises against eligible quantities | Stock-related cancellations; reservation conflicts; attempts to issue held stock |
| Errors spread during imports or repeated integration events | Validate imports, identify exact failures, and process retries idempotently | Correctable failures and fewer duplicate movements | Import correction time; duplicate business effects; unresolved sync failures |
| Purchasing uses different supplier codes or packaging | Map supplier codes and purchasing units to one internal item | Less lookup and fewer wrong-item or wrong-quantity orders | Purchasing correction rate; manual code lookups |
| Reports require assembling several spreadsheets | Saved operational views with drill-down into movements | Users can answer everyday questions from the system | Time to answer stock questions; external reconciliation effort |
| Changes are difficult to investigate | Retain actor, reason, document links and correction history | Faster investigation and clear responsibility | Time to explain sampled adjustments; attribution completeness |
| Inventory must coexist with an ERP | Explicit mappings, ownership rules, visible synchronization and reconciliation | Physical operations and financial systems can cooperate | Reconciliation exceptions and their age; repeated manual entry |

These are intended outcomes, not guaranteed savings. Software still depends on staff recording real movements, usable item data and appropriate access controls.

## Cross-sector examples

- A manufacturer enters 200 kg of existing material without a bill, consumes 30 kg against production, and records outputs and waste with lot links where enabled.
- A pharma distributor receives a batch into a held state, records applicable tracking details, and makes it available only after the configured release step. Specific regulatory requirements must be researched separately before any compliance claim.
- A wholesaler receives cases, sells individual units, and reserves quantities while an order awaits payment.
- A maintenance team tracks supplies received, moved and consumed internally, even when customer sales and purchasing documents are irrelevant.

Each example uses the shared catalog, locations and movement core. Sector modules should add information and controls where useful, without forcing every user through manufacturing or pharma screens.

## Proposed initial release boundary

Complete one dependable operational loop: establish existing stock, receive more, locate and transfer it, reserve/issue it, count it, and explain corrections. Provide barcode/manual entry, safe spreadsheet import, essential operational views and full export. Documents are optional throughout physical entry; required tracking information follows item policy.

Prioritize correctness and adoption of that loop before implementing broad forecasting, full accounting, many ERP connectors or advanced production planning. Manufacturing and pharma remain intended audiences; their specialized production/quality workflows require their own acceptance criteria and should not be advertised as complete simply because the schema has extension tables.

Open source is a delivery and governance choice: inspectable behavior, extensibility, local deployment and data portability. It does not by itself deliver accurate counts, low maintenance costs or support. Installation, backup/restore, upgrade documentation and clear ownership of operational tasks are part of a usable self-hosted product.

## Success measures

Primary proposed measure: **count agreement at the item/location/lot/status level**, the percentage of physically counted positions whose recorded quantity agrees within the declared unit-specific tolerance. Freeze the tolerance before a pilot. Report sample size, sampling approach and discrepancy magnitude alongside the percentage so small or easy samples do not conceal problems.

Supporting measures:

- Median and 90th-percentile time to receive or issue a typical line, with and without a bill.
- Staff time spent reconciling discrepancies per week, using the same task definition before and after adoption.
- Number of orders delayed/cancelled for stock availability errors divided by eligible fulfilled/cancelled orders, with reasons reviewed.
- Time from observing a movement to recording it; proportion left unrecorded in sampled observations.
- Active unresolved discrepancies and sync failures, including their age.
- Quantity and value coverage with unknown/estimated/final costs shown separately; never improve coverage by treating unknown as zero.
- Time to assemble a shipment/batch evidence pack; unresolved holds and evidence gaps by age; stale approvals detected before action. No pilot results or targets exist yet.

Integrity acceptance requirements: no duplicate receipt on retry, no over-allocation under tested concurrency, no partial transfer on rollback, and traceable actor/reason on every posted movement. These are engineering acceptance conditions, not substitutes for business outcome measurements.

Collect a baseline and agree numerical targets with pilot businesses before claiming improvement. A stock audit can be accurate immediately after a forced recount while everyday workflows remain poor; measure sustained agreement and operator effort over repeated cycles.

## Validation and prioritization

Observe representative users from the intended sectors performing a recent receipt without a bill, discrepancy investigation and issue/dispatch. Ask for actual examples of supplier-code mismatches, spreadsheet workarounds and held stock. Record frequency, time lost, business consequence and current workaround; do not collect confidential bills or personal data unnecessarily.

Prioritize work that addresses frequent or costly failures in the shared loop, has a measurable benefit, and can be supported reliably. A feature request without an identifiable task and outcome remains a hypothesis. Revisit the first adoption profile and release scope when observed workflows contradict them.

## Product decision test

For every proposed feature, ask: whose inventory decision becomes more reliable, what manual work or error is reduced, what is the smallest complete workflow, and how will we verify improvement?

<!-- reading-sequence:start -->
[Previous: Documentation index](README.md) | [Next: Stakeholders and workflows](research/stakeholders-and-operational-workflows.md)
<!-- reading-sequence:end -->
