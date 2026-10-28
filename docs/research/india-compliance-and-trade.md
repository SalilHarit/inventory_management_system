# India compliance, auditability and cross-border inventory

<!-- reading-sequence:start -->
[Previous: Stakeholders and workflows](stakeholders-and-operational-workflows.md) | [Next: Existing-system schema research](existing-system-schemas.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Compliance design](../design/compliance-and-trade.md) | [Stakeholder research](stakeholders-and-operational-workflows.md)

Research date: 2026-10-28. Scope confirmed by user: India-based businesses importing/exporting internationally. Destination country, commodity, legal form, licence and customs regime are not yet selected. This is a product-design evidence record, not a determination that any specific shipment is lawful or that the software is certified.

Retrieval: earlier primary evidence was collected before the user requested a provider change. Subsequent retrieval uses scrape.do; no further Firecrawl requests are authorized. API credentials must never be committed. The revised Schedule M PDF was fetched successfully through scrape.do from CDSCO and its English text extracted locally. Reviewed PDF pages 167, 178 and 179 (printed pages 166–178, with intervening pages not reviewed in detail).

## What the evidence establishes

| Source | Relevant finding | Design implication / scope limit |
| --- | --- | --- |
| [CBIC, CGST Rule 56](https://taxinformation.cbic.gov.in/content/html/tax_repository/gst/rules/cgst_rules/active/chapter7/rule56_v1.00.html) | Covers relevant import/export records; stock receipts/supplies and losses, destruction, write-offs, gifts/samples; manufacturing quantities including waste/by-products; electronic edit/delete logs. Applicability includes explicit exceptions in the rule. | Distinct movement reasons and production outputs, supporting documents, location history and audit records. A software receipt does not establish valid documentation or tax treatment. |
| [DGFT, FTP Chapter 2](https://content.dgft.gov.in/Website/Chapter_2_Revised_FTP_v1.2.2.pdf), sections 2.01–2.06 | Product policies depend on classification; domestic requirements may also apply. IEC has exceptions. General document lists distinguish transport documents, commercial invoice/packing list and Bill of Entry or shipping/export declarations. Additional product-specific documents can apply. | Shipment-level classification and document checks with jurisdiction and effective versions. Supplier bill, commercial invoice, Bill of Entry and e-waybill are different records. |
| [ICEGATE download utility manual](https://www.icegate.gov.in/sites/default/files/2024-03/User%20Manual%20-%20Download%20Utility%20v1.08.pdf) | Distinguishes assessed documents, import Out of Charge and export Let Export Order documents. | Filing, assessment and release are separate events. Customs status must not be inferred from an invoice or physical receipt. The manual is operational evidence, not a complete statement of customs law. |
| [ICAI revised 2024 audit-trail implementation guide](https://eirc-icai.org/uploads/background_materials/Revised%202024_Implementation%20Guide%20on%20Reporting%20of%20Audit%20Trail%20(1)_1712114860.pdf) | Discusses accounting records across software/interfaces, attribution, protected logs, direct database changes, preservation and operating controls. | Assess whether this IMS contributes to books of account for the entity. Application history alone and ordinary backups alone do not establish adequate audit coverage. This is professional implementation guidance, not a substitute for governing rules. |
| [CDSCO, revised Schedule M notification G.S.R. 922(E), 28 December 2023](https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadGazette_NotificationsFiles/2023.12.28_DR_Final%20G.S.R.%20922(E)_Notification%20of%20Schedule%20M%20of.pdf) | Paragraphs 17.2.6–17.2.8 address document corrections and electronic records. Paragraphs 20.1–20.9 address system validation, access/change controls, previous values and actor/time, critical manual-entry checks, incidents, controlled system changes and backups. | Controls must be implemented and validated for the actual deployment. Manufacturing requirements must not be indiscriminately assigned to every distributor. Implementation timelines/amendments and destination obligations remain to be checked. |

No universal tax thresholds, retention duration, licence checklist or deadline is hardcoded from this preliminary review. Maintain applicability by entity, activity, product, route, effective date and source. Review amendments before enabling a jurisdiction-specific rule pack.

## What existing software already addresses

- [Odoo 18 India localization](https://www.odoo.com/documentation/18.0/applications/finance/fiscal_localizations/india.html) documents e-invoicing, e-waybills, inventory-related e-waybill creation and GST integrations. These are not market-wide missing features.
- [SAP Global Trade Services](https://www.sap.com/products/financial-management/global-trade-management.html) describes classification, licence management, screening, customs processes and blocking/release. This establishes marketed capability, not independent implementation performance.
- Our [upstream schema research](existing-system-schemas.md) already found lots, suppliers, ownership and stock tracking in open-source systems. Adding those fields is not novel by itself.

**Unvalidated opportunity:** make the interaction between these controls affordable to operate, understandable, traceable and integrated for smaller teams. We have not established that all existing products fail at this, or that buyers will switch. Validate time spent assembling evidence across stock, quality, ERP, broker and transport records; missed holds; stale approvals; and reconciliation problems.

## Practical overlap scenarios

| Scenario | Failure we must prevent | Proposed behavior |
| --- | --- | --- |
| Imported raw material passes QC but customs release is pending | QC approval accidentally makes restricted material usable | Separate customs, quality and documentation holds; eligible only when all applicable gates pass |
| Same SKU and batch arrives under two customs treatments | Merging balances loses restrictions attached to one receipt | Preserve provenance segments by receipt/regime/owner; movements and production consume identified segments |
| Imported inputs become an exported finished batch | Input provenance disappears at production completion | Link received lots/segments to consumption, output lots and shipment allocations; origin claims remain separately reviewed |
| Destination changes after approval | Reuse of approval against a different route | Invalidate relevant checks and repeat route/product/party review against a new snapshot |
| Bill or transport evidence is missing | Fabricated invoice or a misleading compliant flag | Capture stock through normal form, show missing facts and apply the relevant hold; entry does not grant permission to trade |
| Partial customs clearance or split shipment | Full stock released on partial approval | Allocate clearance and documents at line/quantity scope |
| Export return / re-import | Automatic resale or loss of original declaration links | Link original shipment, returned lots and new declaration/review; inspect before release where required |
| Cold-chain excursion or recall after allocation | Existing reservation bypasses newly imposed hold | Hold propagation, reservation review, dispatch recheck and trace-forward to affected customers |
| ERP and customs broker disagree | A connector overwrites a more authoritative status | Explicit source authority, conflicting evidence retained and assigned for resolution |

The scenarios are product test cases, not universal legal rules. Bonded storage, processing schemes, controlled goods, preferential origin and destination pharma requirements need dedicated reviewed modules before support is advertised.

<!-- reading-sequence:start -->
[Previous: Stakeholders and workflows](stakeholders-and-operational-workflows.md) | [Next: Existing-system schema research](existing-system-schemas.md)
<!-- reading-sequence:end -->
