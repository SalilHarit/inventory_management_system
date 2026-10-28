# Stakeholders and operational workflows

<!-- reading-sequence:start -->
[Previous: Product goal](../product-goal.md) | [Next: India compliance research](india-compliance-and-trade.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Product goal](../product-goal.md) | [Compliance research](india-compliance-and-trade.md)

Researched 2026-10-28 using scrape.do. Purpose: identify who operates an IMS, how existing software is used, and which operational difficulties deserve validation. This is desk research, not interviews or direct observation. Job titles vary; a small company may assign several responsibilities to one person.

## Evidence register

Source R1: [inFlow user reviews on Capterra](https://www.capterra.com/p/78431/inFlow-Inventory/reviews/), retrieved 2026-10-28. These are reviewer accounts, not verified current product defects. Some are incentivized, and most examples below date to 2024–2025. No review sample is representative of the market.

| ID | Actual reported role / dated evidence | Observed use and friction | Qualification |
| --- | --- | --- | --- |
| R1a | Warehouse manager, construction, 2–10 employees; September 12, 2024 | Wants to hold goods awaiting customer payment while preventing online sales, without treating them as physically gone | Strong reservation-workflow signal; current product support not established |
| R1b | Field Operations Manager, renewables, 11–50 employees; September 11, 2024 | Combines multiple reports in Excel to obtain the required overall view | Report composition problem, not proof that all reports are inadequate |
| R1c | CFO, manufacturing context; May 31, 2024 | Reports scanning and manufacturing ease; requests attribution on stock adjustments and mandatory explanations | Useful supervision/auditability signal from finance, not an external auditor interview |
| R1d | Purchasing and Inventory Control Specialist, health/wellness, 201–500 employees; July 9, 2024 | Used videos during setup and created a Showroom where employees request supplies for their sites | Positive evidence for separating requesters from inventory operators; does not establish a current training defect |
| R1e | Director of Operations, food/beverages, 2–10 employees; September 12, 2024 | Reports switching between web and app for dropshipping, searching and report filters | Historical interface-parity friction; verify current versions before using competitively |
| R1f | Corporate Office Liaison and Compliance Analyst, vehicle manufacturing; April 11, 2025 | Uses BOMs, stock and parts sales; reports manual touch when component-cost changes do not update BOM costing and difficulty with accounting integration | Reviewer explicitly allows that integration issues may involve QuickBooks; source is incentivized. Current standards versus historical cost snapshots need separate treatment |
| R1g | Director, farming; March 6, 2024 | Exported stock lists to Excel and manually removed unavailable items | Vendor replied that Inventory by Location can exclude zero stock. Discoverability/configuration gap, not confirmed missing feature |
| R1h | Finance Manager, construction, 51–200 employees; October 21, 2025 | Reports team preference for the previous purchase-order layout and fulfillment process after an update | Change-management signal, not evidence that the new workflow is objectively worse |
| R1i | Owner, small manufacturing context; September 11, 2024 | Values simpler operation and lower ERP management overhead; wants deeper customer/product integration | Positive evidence for scope discipline, with integration requirements |

Source R2: [Cin7 Core reviews on G2](https://www.g2.com/products/cin7-core/reviews?qs=pros-and-cons), retrieved 2026-10-28. Individual excerpts report Shopify lag/oversells, cumbersome CSV limits and unclear import errors. The page also contains positive integration and support reports. Some excerpts omit dates and job titles; do not invent role-specific attribution. G2-generated summaries are not independent operator interviews. The detailed bank-statement-import example concerns finance import, not a measured stock-entry failure.

Source R3: [ERPNext stock reconciliation documentation](https://docs.frappe.io/erpnext/stock-reconciliation), retrieved 2026-10-28. Documents manual opening/count entry, item/warehouse/quantity/valuation fields, save/submit, exact CSV identifiers and case-sensitive headers, barcode scan mode, and serial/batch reconciliation scope. This establishes a documented workflow, not evidence that users dislike it. It also establishes that bill-free opening stock already exists in other software.

Source R4: [Zoho Shopify integration guide](https://www.zoho.com/us/inventory/help/marketplaces/shopify.html), reviewed during earlier project research. Documents item/warehouse mapping, synchronization history and resync. Treats integration operation as an ongoing responsibility rather than a one-time setup.

Source R5: [ICAI audit-trail guide, revised 2024](https://eirc-icai.org/uploads/background_materials/Revised%202024_Implementation%20Guide%20on%20Reporting%20of%20Audit%20Trail%20(1)_1712114860.pdf), reviewed during earlier compliance research. Provides audit expectations concerning systems, logs and controls. This supports auditor task design, not an assertion that auditors were interviewed. Applicability remains entity/use dependent.

## Stakeholder map

Cadences and responsibility boundaries below are proposed operational models inferred from tasks, not observed time studies. R = actual review signal; D = documented existing workflow; H = hypothesis requiring field validation.

| Stakeholder | How they use existing software | Typical cadence / trigger | Challenges and evidence | Proposed IMS response |
| --- | --- | --- | --- | --- |
| Data-entry / receiving clerk | Finds SKU/supplier, enters quantity/unit/location, attaches available evidence, saves/posts receipts or imports rows | Each delivery or batch of paperwork | Exact master-data identifiers and template rules (D:R3); missing-paperwork, unit ambiguity and duplicate entry are H | Search supplier codes/barcodes; same form with optional bill; draft/resume; precise validation and retry-safe posting |
| Storekeeper / picker / dispatch operator | Scans bins/items, picks eligible lots, moves stock, confirms actual dispatch and discrepancies | Repeated physical operations during a shift | Scanner count workflow documented (D:R3); device switching reported by operations leader (R:R1e), not directly by picker. Scan-speed/connectivity/glove problems remain H | Task-specific receiving/picking screens, clear unit/lot confirmation, visible holds; validate devices onsite before offline commitments |
| Requester / employee / branch user | Searches supplies and requests items for a site rather than editing stock balances | As supplies are needed | Existing employee portal reported positively (R:R1d) | Request quantity/destination/purpose; track approval and fulfillment; no stock-posting permission by default |
| Purchasing officer | Checks availability and incoming orders, selects supplier/unit, creates POs, follows partial receipts | Reorder review and delivery exceptions | PO change friction (R:R1h); supplier-code request from prior research; repeated mapping work remains H | Supplier aliases, units, expected/received/outstanding quantities and visible workflow changes |
| Sales / customer-service user | Checks availability, reserves stock, confirms dates, follows order/dispatch status | Quotes, orders and customer enquiries | Payment-pending stock hold (R:R1a); integration-related oversell reports (R:R2, role unverified) | Separate on-hand/available/reserved; reservation owner/release; display freshness of channel data |
| Warehouse / shift supervisor | Reviews exceptions, approves discrepancies, assigns work and monitors outstanding receipts/transfers | Shift handover and escalations | Reporting assembly (R:R1b); adjustment explanation/actor gap from finance (R:R1c). Assignment and shift-handover difficulties are H | Exception queues, scoped approvals, transaction drill-down and owned unresolved work |
| Production planner / material controller | Reviews material availability/BOMs, records consumption/output, checks shortages and costing | Production planning and completions | Actual manufacturing use, setup complexity and BOM-cost touch time (R:R1f) | Released BOM versions, explainable material availability, explicit costing basis, input/output tracking; no silent rewriting of past costs |
| Quality / regulatory reviewer | Reviews inspection evidence and lot status, imposes/releases holds, investigates rejected/returned goods | Batch receipt, inspection, excursion or recall | Role responsibilities supported by compliance design; direct usability evidence absent (H) | Evidence-linked independent holds, reviewed release, affected-stock trace and role separation |
| Finance / accounts user | Matches receipts to bills, resolves discrepancies, checks valuation and reconciles ERP entries | Invoice processing and accounting close | Adjustment traceability (R:R1c), cost/integration work (R:R1f), purchase-layout changes (R:R1h) | Quantity/cost/document separation; explicit unknown value; bill/receipt differences; audit drill-down |
| Owner / management viewer | Checks shortages, slow stock, service failures and exposure; asks for exception explanations | Daily review, purchasing decisions and management meetings | Simpler ERP sought (R:R1i), spreadsheet cleanup for reports (R:R1g) | Saved role-appropriate views, freshness/as-of labels and totals traceable to facts; read-only is a permission, not a job title |
| Internal / external auditor | Selects samples, reconstructs changes, inspects evidence/approvals and tests operating controls | Periodic/internal review or statutory audit | Supported by R5, not auditor UX interviews; time spent assembling evidence remains H | Scoped time-limited read/export access, historical snapshots, complete evidence manifests, access/export audit events; no record modification |
| Administrator / ERP integration operator | Configures users, master data and mappings; investigates failures and performs upgrades/recovery | Setup, changes, failures and maintenance | Mapping/resync workflow (D:R4), import/integration reports (R:R2; roles unverified) | Health/error queues, safe replay, explicit authority, deployment records; admin role does not automatically confer QC or trade approval |
| Import/export coordinator / broker-facing user | Links shipment, declaration, transport and product evidence; resolves clearance differences | Each cross-border shipment and exception | Existing customs/document controls researched separately; direct operator UX evidence absent (H) | Shipment evidence checklist, partial clearance, ownership of blockers and preserved regulatory sources |

## End-to-end handoff to observe

Example: a supplier delivers 80 of 100 ordered boxes and the bill has not arrived.

1. Receiving clerk finds the item, confirms packaging, counts 80 and records the receipt using the normal form. Missing bill is explicit; unknown cost is not zero.
2. Storekeeper confirms bin and relevant lot/serial details. Quality/customs controls can hold stock independently; physical recording still happens.
3. Supervisor reviews discrepancies or approves an adjustment within assigned scope. The person who entered the facts is recorded separately from the reviewer.
4. Purchasing sees 20 outstanding and follows up. Finance later matches the actual bill without creating a second receipt.
5. Sales sees only the eligible, unreserved quantity. Production has its own action eligibility rather than inheriting permission from a sales flag.
6. Management sees open discrepancies and responsible staff. An auditor can later reconstruct the original receipt, corrections, holds, release and bill match.

The proposed journey must be tested in a real site. Do not assume current software or every operator follows this sequence, or require every small business to employ a separate person for each step.

## Operational challenges to prioritize

1. **Finding the correct item and unit before entry**: distinguish searchable SKU/supplier/barcode aliases; validate with observed wrong-match and unit-correction rates (H plus prior supplier evidence).
2. **Understanding which quantity a screen shows**: users should distinguish physically present, reserved and permitted-to-use stock (R:R1a).
3. **Recovering from a failed or mistaken operation**: exact errors, safe retries and traceable corrections instead of unexplained balances (R:R2; auditability R1c).
4. **Answering a supervisor's question without rebuilding Excel reports**: reusable filters and explanation of totals (R:R1b/R1g, noting vendor response).
5. **Preserving a task across devices and software updates**: minimize unnecessary switching and explain consequential workflow changes (R:R1e/R1h; historical).
6. **Knowing who owns an unresolved exception**: a missing document, failed sync or stock mismatch needs an assignee and next step (H).
7. **Reviewing evidence without altering it**: viewer/auditor roles must have scoped inspection and export; actual audit interaction pain still needs validation (R5/H).

## Proposed responsibility and access boundaries

Model permissions by action, organization, site and record scope. A title alone is insufficient.

- Request: requester creates demand; cannot adjust inventory.
- Capture: clerk creates drafts and, where policy permits, routine receipts in assigned sites.
- Post: trained operator confirms physical transactions; irreversible history requires explicit correction paths.
- Review/approve: supervisor/QC/trade reviewer acts only in assigned scope and cannot silently self-approve when separation is required.
- View/export: management, customer-service and auditors see their authorized stock/value/evidence scope; cost and personal information can require separate access.
- Configure: system administrator manages technical settings; business approvals remain distinct.

Small-team combined roles are possible where allowed, with explicit conflict policy and visible history. Auditability does not mean exposing all supplier prices, personal data or company records to every viewer.

## Field research next

Recruit by responsibility, not just industry: receiving clerk, picker/storekeeper, supervisor, purchasing/accounts operator, viewer and independent reviewer, plus quality/trade roles at relevant sites. Do not substitute only owner interviews for frontline observation. No outreach has been sent.

Ask each participant to demonstrate a recent task in their existing tool, using sanitized data: receive without a bill; resolve a unit mismatch; reserve pending payment; find a missing transfer; explain a count adjustment; compile a report; reconstruct a batch/shipment decision. For quality/auditors ask what evidence was rejected or unavailable, rather than assuming they want more dashboards.

Record steps, interruptions, searches, handoffs, duplicate typing, errors, correction time, external spreadsheets/messages, device and training needs. Separate product absence from configuration, permission, training, stale data and process failures. Capture what works well and should be preserved. Measure baseline before setting targets.

Desk-research limitations: no firsthand observation, no direct frontline clerk/picker or external-auditor interviews, no India-specific representative operator sample, no verified current-version reproduction of historical complaints. These gaps should guide the next validation rather than be hidden behind detailed personas.

<!-- reading-sequence:start -->
[Previous: Product goal](../product-goal.md) | [Next: India compliance research](india-compliance-and-trade.md)
<!-- reading-sequence:end -->
