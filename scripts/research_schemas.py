"""Capture public upstream schema field names at exact commits; no application code copied."""
import ast
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {
    'frappe/erpnext': ('develop', [
        'erpnext/stock/doctype/item/item.json',
        'erpnext/stock/doctype/bin/bin.json',
        'erpnext/stock/doctype/stock_ledger_entry/stock_ledger_entry.json',
        'erpnext/stock/doctype/stock_entry/stock_entry.json',
        'erpnext/stock/doctype/stock_entry_detail/stock_entry_detail.json',
        'erpnext/stock/doctype/batch/batch.json',
        'erpnext/stock/doctype/item_supplier/item_supplier.json']),
    'odoo/odoo': ('18.0', [
        'addons/stock/models/stock_move.py',
        'addons/stock/models/stock_move_line.py',
        'addons/stock/models/stock_quant.py']),
    'inventree/InvenTree': ('master', [
        'src/backend/InvenTree/stock/models.py',
        'src/backend/InvenTree/company/models.py'])
}

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'IMS-schema-research'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode()

records = []
for repo, (branch, paths) in SOURCES.items():
    sha = json.loads(get(f'https://api.github.com/repos/{repo}/commits/{branch}'))['sha']
    for path in paths:
        raw = get(f'https://raw.githubusercontent.com/{repo}/{sha}/{path}')
        models = {}
        if path.endswith('.json'):
            doc = json.loads(raw)
            models[doc.get('name', pathlib.Path(path).stem)] = [
                {'name': f['fieldname'], 'type': f['fieldtype'], 'target': f.get('options'),
                 'required': bool(f.get('reqd'))}
                for f in doc['fields'] if f.get('fieldname') and f['fieldtype'] not in
                ('Section Break', 'Column Break', 'Tab Break', 'HTML', 'Button')]
        else:
            tree = ast.parse(raw)
            for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
                fields = []
                for node in cls.body:
                    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                        fun = ast.unparse(node.value.func)
                        if fun.startswith(('fields.', 'models.')):
                            fields.extend({'name': ast.unparse(t), 'type': fun,
                                           'target': ast.literal_eval(node.value.args[0])
                                           if node.value.args and isinstance(node.value.args[0], ast.Constant) else None}
                                          for t in node.targets)
                if fields:
                    models[cls.name] = fields
        records.append({'repository': repo, 'ref': branch, 'commit': sha, 'path': path,
                        'url': f'https://github.com/{repo}/blob/{sha}/{path}', 'models': models})
        print(repo, path, sum(map(len, models.values())), 'fields')

output = ROOT / 'docs/research/upstream-schema-fields.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({'retrieved_at': datetime.now(timezone.utc).isoformat(),
                              'method': 'Static field declarations only; not a live database dump. Inherited/framework fields and runtime constraints may be absent.',
                              'sources': records}, indent=2), encoding='utf-8')
