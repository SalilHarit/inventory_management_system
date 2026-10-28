"""Render proposed names from design documents; does not introspect or change PostgreSQL."""
import json
import re
from pathlib import Path
from document_navigation import update_document

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ['docs/design/database-schema.md', 'docs/design/compliance-and-trade.md']

def split_columns(value):
    result, current, depth = [], [], 0
    for char in value:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if char == ',' and depth == 0:
            result.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        result.append(''.join(current).strip())
    return result

def field(name, declaration, source, nullability='required by draft convention'):
    return dict(name=name, declaration=declaration, source=source, nullability=nullability)

tables = []
for path in INPUTS:
    section = ''
    for line in (ROOT / path).read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            section = line[3:]
        if not re.match(r'^\| [a-z][a-z_]* \|', line):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != 3:
            raise ValueError(line)
        name, declaration, rules = cells
        columns = []
        if name != 'currency':
            columns += [field('id', 'uuid PK', 'common convention'),
                        field('created_at', 'timestamptz', 'common convention'),
                        field('created_by', 'uuid FK actor', 'common convention',
                              'bootstrap actor exception only' if name == 'actor' else 'required by draft convention')]
            if name not in ('organization', 'actor'):
                columns.append(field('org_id', 'uuid FK organization', 'common convention'))
        for spec in split_columns(declaration):
            raw_name = spec.split()[0]
            col_name = raw_name.rstrip('?')
            if not re.fullmatch('[a-z][a-z0-9_]*', col_name):
                raise ValueError((name, spec))
            if any(c['name'] == col_name for c in columns):
                # The addendum repeats created_at on evidence_export.
                continue
            nullable = 'nullable in draft' if '?' in spec else (
                'not specified; review required' if path.endswith('compliance-and-trade.md')
                else 'required by draft convention')
            columns.append(field(col_name, spec[len(raw_name):].strip() or 'type not specified in source draft', path, nullable))
        if name == 'stock_bucket':
            columns.append(field('provenance_segment_id', 'uuid FK provenance_segment', INPUTS[1],
                                 'required for tracked trade; general policy under review'))
            rules += ' Trade addendum extends bucket identity with provenance_segment_id.'
        assert len({c['name'] for c in columns}) == len(columns)
        tables.append(dict(name=name, source=path, section=section, columns=columns, rules=rules,
                           status='proposed; not migrated',
                           mutable_metadata='updated_at timestamptz, updated_by uuid FK actor, version bigint apply to mutable master/draft records; per-table assignment needs review'))

assert len({t['name'] for t in tables}) == len(tables)
data = dict(status='proposal audit, not deployed schema', date='2026-10-28', tables=tables,
            deferred_structures=['declaration_line_allocation', 'hold events and partial hold allocations',
                                 'many-input provenance genealogy', 'audit findings and review scopes',
                                 'role permissions and site scopes', 'valuation layers, FX and landed costs',
                                 'retention policies and legal holds'])
output = ROOT / 'docs/design/schema-audit.json'
output.write_text(json.dumps(data, indent=2), encoding='utf-8')

lines = ['# Proposed table and column audit', '',
         '[Documentation index](../README.md) | [Project home](../../README.md) | [Table discussions](table-discussions.md)', '',
         'Generated 2026-10-28 from the base schema and trade addendum. This consolidates names for discussion; it is not SQL, an approved final schema or a deployed database inventory.', '',
         f"**{len(tables)} proposed tables; {sum(len(t['columns']) for t in tables)} explicitly listed column positions including expanded identity/audit columns.** Mutable metadata is listed separately below and not included in that count.", '',
         '[Machine-readable inventory](schema-audit.json) · [Base dictionary](database-schema.md) · [Trade addendum](compliance-and-trade.md) · [Table discussion queue](table-discussions.md)', '',
         '## Read this before auditing', '',
         '- Every table below expands id, created_at, created_by and org_id where the draft requires them. Global currency uses code as its primary key and has no organization/audit columns under the current convention.',
         '- Mutable master/draft records also need updated_at, updated_by and version. Their exact per-table assignment is NOT settled; audit this before DDL. Existing explicitly declared version columns are included.',
         '- A question mark in a source declaration means optional. The trade addendum has incomplete type/nullability declarations; missing detail is labeled rather than silently invented.',
         '- Common created_by versus event-specific actor_id/reviewer_id/posted_by fields can overlap. Review their distinct recording/action/approval meaning; do not remove attribution blindly.',
         '- Sources remain proposals. Future migrations and the generated live schema snapshot will establish the implemented truth.', '',
         '## Table index', '', '| # | Table | Group | Listed columns |', '| --- | --- | --- | --- |']
for i,t in enumerate(tables,1):
    lines.append(f"| {i} | [{t['name']}](#{t['name']}) | {'Trade / compliance' if t['source']==INPUTS[1] else t['section']} | {len(t['columns'])} |")
lines += ['', '## Open audit findings', '',
          '1. Stock identity must include provenance_segment_id; the base table alone is superseded on that point by the trade addendum.',
          '2. document.storage_key/sha256/original_name overlap immutable document_version content. Decide which fields identify a logical document versus a file version; file metadata should not drift independently.',
          '3. organization_actor roles do not yet define permissions/site scopes. Do not call the current identity tables a complete authorization system.',
          '4. establishment.address and audit_review.scope are underspecified; decide normalized address fields and relational review scope before implementation.',
          '5. customs_declaration_line currently lists shipment_line_id, but the addendum requires many-to-many allocation support. declaration_line_allocation is not yet column-specified.',
          '6. inventory_hold lacks an explicit event/allocation schema for release and partial quantities. The current row list alone cannot implement the stated hold behavior.',
          '7. Item-classification approvals and permit versions must preserve historic facts; mutable row references alone are insufficient.',
          '8. purchase_order_line requires supplier-code/description snapshots in prose but their final names/types are not specified. Add them during table review.',
          '9. Provenance receipt-to-segment-to-bucket references form a creation dependency cycle. Resolve deferral/draft construction and constraints before DDL.',
          '10. A global actor external_subject needs issuer/provider scoping if multiple identity providers are supported.',
          '11. Core stock quantities, reservations, business permissions and compliance constraints require reviewed posting functions and tests in addition to column definitions.',
          '12. Suppliers/customers need contact/address and relevant registration facts for document workflows. The current party table is intentionally incomplete.', '',
          '## Detailed inventory', '']
for t in tables:
    lines += [f"### {t['name']}", '',
              f"Source: [{Path(t['source']).name}]({Path(t['source']).name}). Status: proposed.", '',
              '| Column | Declared type / reference | Nullability |', '| --- | --- | --- |']
    for c in t['columns']:
        lines.append(f"| `{c['name']}` | {c['declaration']} | {c['nullability']} |")
    lines += ['', f"Rules to review: {t['rules']}", '']
lines += ['## Deferred structures without audited columns', '',
          *[f'- {name}' for name in data['deferred_structures']], '',
          'These are known design work, not implemented tables. Do not infer complete compliance, permissions or accounting coverage from this inventory.', '',
          '## Regenerate', '',
          'Run `python scripts/build_schema_audit.py` after editing the two source dictionaries. Review the generated diff. No database credentials or server are used.', '']
(ROOT / 'docs/design/schema-audit.md').write_text('\n'.join(lines), encoding='utf-8')
update_document(ROOT / 'docs/design/schema-audit.md')
print(f"Generated {len(tables)} tables / {sum(len(t['columns']) for t in tables)} listed column positions")
