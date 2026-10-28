# Existing inventory systems: tables and columns

<!-- reading-sequence:start -->
[Previous: India compliance research](india-compliance-and-trade.md) | [Next: Decision register](../decisions/decision-register.md)
<!-- reading-sequence:end -->

[Documentation index](../README.md) | [Project home](../../README.md) | [Schema proposal](../design/database-schema.md)

Research date: 2026-10-28. Sources are pinned to exact commits below. These are static framework model/DocType declarations, not live database introspection. Fields may be computed, related, virtual or inherited; therefore not every name is a physical SQL column. Field types and reference targets are preserved in [machine-readable evidence](upstream-schema-fields.json).

ERPNext develop and InvenTree master are development snapshots; Odoo uses its 18.0 branch. These are not equivalent release baselines. No performance or concurrency claims are inferred merely from field names.

## Findings and design implications

| System | Observed structure | Implication for our proposal |
| --- | --- | --- |
| ERPNext | Item, Item Supplier, Stock Entry / Detail, Stock Ledger Entry, Bin, Batch | Separate catalog, operational header/lines, history and balance projection. Item supplier codes are first-class child records. |
| Odoo | StockMove, StockMoveLine, StockQuant and QuantPackage | Distinguish demand/planning from actual operations; stock identity includes product, location, lot, package and owner. |
| InvenTree | StockItem, supplier/manufacturer parts, stock locations and test results | Track provenance, supplier packaging and technical/quality results independently. |

These systems already support many sophisticated features. Our opportunity is accessible, coherent workflows; this research does not support claiming lots, reservations or supplier aliases are absent throughout the market.

## Source field inventory

### frappe/erpnext — item.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/item/item.json).

**Item** — 81 directly declared fields

`naming_series`, `item_code`, `variant_of`, `item_name`, `item_group`, `stock_uom`, `disabled`, `allow_alternative_item`, `is_stock_item`, `include_item_in_manufacturing`, `opening_stock`, `valuation_rate`, `standard_rate`, `is_fixed_asset`, `asset_category`, `asset_naming_series`, `image`, `brand`, `description`, `barcodes`, `shelf_life_in_days`, `end_of_life`, `default_material_request_type`, `valuation_method`, `warranty_period`, `weight_per_unit`, `weight_uom`, `reorder_levels`, `uoms`, `has_batch_no`, `create_new_batch`, `batch_number_series`, `has_expiry_date`, `retain_sample`, `sample_quantity`, `has_serial_no`, `serial_no_series`, `use_serial_no_wise_valuation`, `has_variants`, `variant_based_on`, `attributes`, `item_defaults`, `is_purchase_item`, `purchase_uom`, `min_order_qty`, `safety_stock`, `lead_time_days`, `last_purchase_rate`, `is_customer_provided_item`, `delivered_by_supplier`, `supplier_items`, `country_of_origin`, `customs_tariff_number`, `sales_uom`, `is_sales_item`, `max_discount`, `enable_deferred_revenue`, `no_of_months`, `enable_deferred_expense`, `no_of_months_exp`, `customer_items`, `taxes`, `inspection_required_before_purchase`, `inspection_required_before_delivery`, `quality_inspection_template`, `default_bom`, `is_sub_contracted_item`, `customer_code`, `total_projected_qty`, `over_delivery_receipt_allowance`, `over_billing_allowance`, `auto_create_assets`, `default_item_manufacturer`, `default_manufacturer_part_no`, `grant_commission`, `is_grouped_asset`, `allow_negative_stock`, `purchase_tax_withholding_category`, `sales_tax_withholding_category`, `restrict_to_companies`, `allowed_companies`

### frappe/erpnext — bin.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/bin/bin.json).

**Bin** — 16 directly declared fields

`warehouse`, `item_code`, `reserved_qty`, `actual_qty`, `ordered_qty`, `indented_qty`, `planned_qty`, `projected_qty`, `reserved_qty_for_production`, `reserved_qty_for_sub_contract`, `stock_uom`, `company`, `valuation_rate`, `stock_value`, `reserved_qty_for_production_plan`, `reserved_stock`

### frappe/erpnext — stock_ledger_entry.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/stock_ledger_entry/stock_ledger_entry.json).

**Stock Ledger Entry** — 31 directly declared fields

`item_code`, `serial_no`, `batch_no`, `warehouse`, `posting_date`, `posting_time`, `voucher_type`, `voucher_no`, `voucher_detail_no`, `actual_qty`, `incoming_rate`, `outgoing_rate`, `stock_uom`, `qty_after_transaction`, `valuation_rate`, `stock_value`, `stock_value_difference`, `stock_queue`, `project`, `company`, `fiscal_year`, `is_cancelled`, `to_rename`, `dependant_sle_voucher_detail_no`, `recalculate_rate`, `serial_and_batch_bundle`, `has_batch_no`, `has_serial_no`, `is_adjustment_entry`, `auto_created_serial_and_batch_bundle`, `posting_datetime`

### frappe/erpnext — stock_entry.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/stock_entry/stock_entry.json).

**Stock Entry** — 60 directly declared fields

`naming_series`, `stock_entry_type`, `weight_per_piece`, `outgoing_stock_entry`, `source_stock_entry`, `purpose`, `company`, `work_order`, `is_fg_conversion`, `purchase_order`, `subcontracting_order`, `delivery_note_no`, `sales_invoice_no`, `purchase_receipt_no`, `posting_date`, `posting_time`, `set_posting_time`, `inspection_required`, `from_bom`, `bom_no`, `fg_completed_qty`, `use_multi_level_bom`, `from_warehouse`, `source_warehouse_address`, `source_address_display`, `to_warehouse`, `target_warehouse_address`, `target_address_display`, `scan_barcode`, `items`, `total_incoming_value`, `total_outgoing_value`, `value_difference`, `additional_costs`, `total_additional_costs`, `supplier`, `supplier_name`, `supplier_address`, `address_display`, `select_print_heading`, `letter_head`, `is_opening`, `project`, `remarks`, `per_transferred`, `total_amount`, `job_card`, `amended_from`, `credit_note`, `pick_list`, `add_to_transit`, `apply_putaway_rule`, `is_return`, `process_loss_qty`, `process_loss_percentage`, `asset_repair`, `last_scanned_warehouse`, `is_additional_transfer_entry`, `subcontracting_inward_order`, `cost_center`

### frappe/erpnext — stock_entry_detail.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/stock_entry_detail/stock_entry_detail.json).

**Stock Entry Detail** — 56 directly declared fields

`barcode`, `s_warehouse`, `t_warehouse`, `item_code`, `item_name`, `description`, `image`, `image_view`, `qty`, `basic_rate`, `basic_amount`, `additional_cost`, `amount`, `valuation_rate`, `uom`, `conversion_factor`, `stock_uom`, `transfer_qty`, `retain_sample`, `sample_quantity`, `serial_no`, `batch_no`, `quality_inspection`, `expense_account`, `cost_center`, `allow_zero_valuation_rate`, `actual_qty`, `bom_no`, `allow_alternative_item`, `material_request`, `material_request_item`, `pick_list_item`, `original_item`, `subcontracted_item`, `against_stock_entry`, `ste_detail`, `transferred_qty`, `item_group`, `reference_purchase_receipt`, `project`, `po_detail`, `sco_rm_detail`, `set_basic_rate_manually`, `putaway_rule`, `is_finished_item`, `job_card_item`, `has_item_scanned`, `serial_and_batch_bundle`, `use_serial_batch_fields`, `landed_cost_voucher_amount`, `customer_provided_item_cost`, `scio_detail`, `against_fg`, `secondary_item_type`, `bom_secondary_item`, `valuation_type`

### frappe/erpnext — batch.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/batch/batch.json).

**Batch** — 18 directly declared fields

`disabled`, `batch_id`, `item`, `image`, `parent_batch`, `manufacturing_date`, `expiry_date`, `supplier`, `reference_doctype`, `reference_name`, `description`, `item_name`, `batch_qty`, `stock_uom`, `qty_to_produce`, `produced_qty`, `use_batchwise_valuation`, `allow_negative_stock_for_batch`

### frappe/erpnext — item_supplier.json

Ref: `develop`; commit: `ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0`. [Source definition](https://github.com/frappe/erpnext/blob/ec20fe5ca1375934f12e2ccd51a35eaf19ecf4e0/erpnext/stock/doctype/item_supplier/item_supplier.json).

**Item Supplier** — 2 directly declared fields

`supplier`, `supplier_part_no`

### odoo/odoo — stock_move.py

Ref: `18.0`; commit: `0589e24259d971b8331c1b2ed960264a0d072b40`. [Source definition](https://github.com/odoo/odoo/blob/0589e24259d971b8331c1b2ed960264a0d072b40/addons/stock/models/stock_move.py).

**StockMove** — 72 directly declared fields

`name`, `sequence`, `priority`, `date`, `date_deadline`, `company_id`, `product_id`, `never_product_template_attribute_value_ids`, `description_picking`, `product_qty`, `product_uom_qty`, `product_uom`, `product_uom_category_id`, `product_tmpl_id`, `location_id`, `location_dest_id`, `location_final_id`, `location_usage`, `location_dest_usage`, `partner_id`, `move_dest_ids`, `move_orig_ids`, `picking_id`, `state`, `picked`, `price_unit`, `origin`, `procure_method`, `scrapped`, `scrap_id`, `group_id`, `rule_id`, `propagate_cancel`, `delay_alert_date`, `picking_type_id`, `is_inventory`, `move_line_ids`, `origin_returned_move_id`, `returned_move_ids`, `availability`, `restrict_partner_id`, `route_ids`, `warehouse_id`, `has_tracking`, `quantity`, `show_operations`, `picking_code`, `show_details_visible`, `is_storable`, `additional`, `is_locked`, `is_initial_demand_editable`, `is_quantity_done_editable`, `reference`, `move_lines_count`, `package_level_id`, `picking_type_entire_packs`, `display_assign_serial`, `display_import_lot`, `next_serial`, `next_serial_count`, `orderpoint_id`, `forecast_availability`, `forecast_expected_date`, `lot_ids`, `reservation_date`, `product_packaging_id`, `product_packaging_qty`, `product_packaging_quantity`, `show_quant`, `show_lots_m2o`, `show_lots_text`

### odoo/odoo — stock_move_line.py

Ref: `18.0`; commit: `0589e24259d971b8331c1b2ed960264a0d072b40`. [Source definition](https://github.com/odoo/odoo/blob/0589e24259d971b8331c1b2ed960264a0d072b40/addons/stock/models/stock_move_line.py).

**StockMoveLine** — 42 directly declared fields

`picking_id`, `move_id`, `company_id`, `product_id`, `product_uom_id`, `product_uom_category_id`, `product_category_name`, `quantity`, `quantity_product_uom`, `picked`, `package_id`, `package_level_id`, `lot_id`, `lot_name`, `result_package_id`, `date`, `scheduled_date`, `owner_id`, `location_id`, `location_dest_id`, `location_usage`, `location_dest_usage`, `lots_visible`, `picking_partner_id`, `picking_code`, `picking_type_id`, `picking_type_use_create_lots`, `picking_type_use_existing_lots`, `picking_type_entire_packs`, `state`, `is_inventory`, `is_locked`, `consume_line_ids`, `produce_line_ids`, `reference`, `tracking`, `origin`, `description_picking`, `quant_id`, `product_packaging_qty`, `picking_location_id`, `picking_location_dest_id`

### odoo/odoo — stock_quant.py

Ref: `18.0`; commit: `0589e24259d971b8331c1b2ed960264a0d072b40`. [Source definition](https://github.com/odoo/odoo/blob/0589e24259d971b8331c1b2ed960264a0d072b40/addons/stock/models/stock_quant.py).

**StockQuant** — 29 directly declared fields

`product_id`, `product_tmpl_id`, `product_uom_id`, `is_favorite`, `company_id`, `location_id`, `warehouse_id`, `storage_category_id`, `cyclic_inventory_frequency`, `lot_id`, `lot_properties`, `sn_duplicated`, `package_id`, `owner_id`, `quantity`, `reserved_quantity`, `available_quantity`, `in_date`, `tracking`, `on_hand`, `product_categ_id`, `inventory_quantity`, `inventory_quantity_auto_apply`, `inventory_diff_quantity`, `inventory_date`, `last_count_date`, `inventory_quantity_set`, `is_outdated`, `user_id`

**QuantPackage** — 10 directly declared fields

`name`, `quant_ids`, `package_type_id`, `location_id`, `company_id`, `owner_id`, `package_use`, `shipping_weight`, `valid_sscc`, `pack_date`

### inventree/InvenTree — models.py

Ref: `master`; commit: `c1683db7146b17ba1369e0845f08f8c69dd4b1cb`. [Source definition](https://github.com/inventree/InvenTree/blob/c1683db7146b17ba1369e0845f08f8c69dd4b1cb/src/backend/InvenTree/stock/models.py).

**StockLocationType** — 3 directly declared fields

`name`, `description`, `icon`

**StockLocation** — 5 directly declared fields

`custom_icon`, `owner`, `structural`, `external`, `location_type`

**StockItem** — 21 directly declared fields

`parent`, `part`, `supplier_part`, `packaging`, `belongs_to`, `customer`, `serial`, `serial_int`, `batch`, `quantity`, `build`, `consumed_by`, `is_building`, `purchase_order`, `sales_order`, `expiry_date`, `stocktake_date`, `stocktake_user`, `creation_date`, `delete_on_deplete`, `owner`

**StockItemTestResult** — 11 directly declared fields

`stock_item`, `template`, `result`, `value`, `attachment`, `notes`, `user`, `test_station`, `started_datetime`, `finished_datetime`, `date`

### inventree/InvenTree — models.py

Ref: `master`; commit: `c1683db7146b17ba1369e0845f08f8c69dd4b1cb`. [Source definition](https://github.com/inventree/InvenTree/blob/c1683db7146b17ba1369e0845f08f8c69dd4b1cb/src/backend/InvenTree/company/models.py).

**Company** — 12 directly declared fields

`name`, `description`, `phone`, `email`, `contact`, `active`, `is_customer`, `is_supplier`, `is_manufacturer`, `is_internal`, `currency`, `tax_id`

**Contact** — 5 directly declared fields

`company`, `name`, `phone`, `email`, `role`

**Address** — 13 directly declared fields

`company`, `title`, `primary`, `line1`, `line2`, `postal_code`, `postal_city`, `province`, `country`, `phone`, `email`, `shipping_notes`, `internal_shipping_notes`

**ManufacturerPart** — 4 directly declared fields

`part`, `manufacturer`, `MPN`, `description`

**SupplierPart** — 14 directly declared fields

`part`, `supplier`, `SKU`, `active`, `primary`, `manufacturer_part`, `description`, `note`, `base_cost`, `packaging`, `pack_quantity`, `multiple`, `available`, `availability_updated`

**SupplierPriceBreak** — 1 directly declared fields

`part`

## Interpretation limits

- ERPNext metadata includes UI-only fields that the extractor filters by type; framework base fields such as document identity, parent linkage and modification metadata are not exhaustively listed.
- Odoo One2many/Many2many/computed/related fields may use other tables or no stored column; inspect individual definitions before copying a physical model.
- InvenTree inherited/mixin fields and dynamically contributed fields are omitted by this AST extractor. The absence of a field from this inventory is not proof it is absent from the actual database.
- This captures field declarations, not all keys, indexes, constraints, state transitions or application locking. Upstream concurrency implementation requires its own audit.
- Upstream schema names and architectural observations are research references; no application source code was incorporated. Review upstream licenses before copying implementation code.

## Reproduce

Run `python scripts/research_schemas.py`, then `python scripts/render_schema_research.py`. The first command fetches current branch heads and rewrites the evidence with new exact commit IDs; review resulting diffs. Network access to public GitHub is required. Existing evidence remains pinned until refreshed.

<!-- reading-sequence:start -->
[Previous: India compliance research](india-compliance-and-trade.md) | [Next: Decision register](../decisions/decision-register.md)
<!-- reading-sequence:end -->
