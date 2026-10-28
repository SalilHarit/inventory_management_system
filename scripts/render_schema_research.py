"""Render the captured field inventory as a source-linked research document."""
import json
from pathlib import Path
from document_navigation import update_document

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'docs/research/upstream-schema-fields.json').read_text(encoding='utf-8'))
lines = ['# Existing inventory systems: tables and columns', '',
         '[Documentation index](../README.md) | [Project home](../../README.md) | [Schema proposal](../design/database-schema.md)', '',
         'Research date: 2026-10-28. Sources are pinned to exact commits below. These are static framework model/DocType declarations, not live database introspection. Fields may be computed, related, virtual or inherited; therefore not every name is a physical SQL column. Field types and reference targets are preserved in [machine-readable evidence](upstream-schema-fields.json).', '',
         'ERPNext develop and InvenTree master are development snapshots; Odoo uses its 18.0 branch. These are not equivalent release baselines. No performance or concurrency claims are inferred merely from field names.', '',
         '## Findings and design implications', '',
         '| System | Observed structure | Implication for our proposal |',
         '| --- | --- | --- |',
         '| ERPNext | Item, Item Supplier, Stock Entry / Detail, Stock Ledger Entry, Bin, Batch | Separate catalog, operational header/lines, history and balance projection. Item supplier codes are first-class child records. |',
         '| Odoo | StockMove, StockMoveLine, StockQuant and QuantPackage | Distinguish demand/planning from actual operations; stock identity includes product, location, lot, package and owner. |',
         '| InvenTree | StockItem, supplier/manufacturer parts, stock locations and test results | Track provenance, supplier packaging and technical/quality results independently. |', '',
         'These systems already support many sophisticated features. Our opportunity is accessible, coherent workflows; this research does not support claiming lots, reservations or supplier aliases are absent throughout the market.', '',
         '## Source field inventory', '']
for source in data['sources']:
    lines += [f"### {source['repository']} — {Path(source['path']).name}", '',
              f"Ref: `{source['ref']}`; commit: `{source['commit']}`. [Source definition]({source['url']}).", '']
    for model, fields in source['models'].items():
        lines += [f"**{model}** — {len(fields)} directly declared fields", '',
                  ', '.join(f"`{field['name']}`" for field in fields), '']
lines += ['## Interpretation limits', '',
          '- ERPNext metadata includes UI-only fields that the extractor filters by type; framework base fields such as document identity, parent linkage and modification metadata are not exhaustively listed.',
          '- Odoo One2many/Many2many/computed/related fields may use other tables or no stored column; inspect individual definitions before copying a physical model.',
          '- InvenTree inherited/mixin fields and dynamically contributed fields are omitted by this AST extractor. The absence of a field from this inventory is not proof it is absent from the actual database.',
          '- This captures field declarations, not all keys, indexes, constraints, state transitions or application locking. Upstream concurrency implementation requires its own audit.',
          '- Upstream schema names and architectural observations are research references; no application source code was incorporated. Review upstream licenses before copying implementation code.', '',
          '## Reproduce', '',
          'Run `python scripts/research_schemas.py`, then `python scripts/render_schema_research.py`. The first command fetches current branch heads and rewrites the evidence with new exact commit IDs; review resulting diffs. Network access to public GitHub is required. Existing evidence remains pinned until refreshed.', '']
(root / 'docs/research/existing-system-schemas.md').write_text('\n'.join(lines), encoding='utf-8')
update_document(root / 'docs/research/existing-system-schemas.md')
print('Rendered', len(data['sources']), 'source files;', sum(len(f) for s in data['sources'] for f in s['models'].values()), 'direct fields')
