"""Maintain the shared reading order at the top and bottom of Markdown files."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEQUENCE = [
    ('README.md', 'Project home'),
    ('docs/README.md', 'Documentation index'),
    ('docs/product-goal.md', 'Product goal'),
    ('docs/research/stakeholders-and-operational-workflows.md', 'Stakeholders and workflows'),
    ('docs/research/india-compliance-and-trade.md', 'India compliance research'),
    ('docs/research/existing-system-schemas.md', 'Existing-system schema research'),
    ('docs/decisions/decision-register.md', 'Decision register'),
    ('docs/decisions/adr/README.md', 'Database decision records'),
    ('docs/decisions/adr/0001-schema-evolution.md', 'ADR 0001: schema evolution'),
    ('docs/decisions/adr/0002-physical-entry-and-financial-evidence.md', 'ADR 0002: bill-independent entry'),
    ('docs/design/table-discussions.md', 'Table discussions'),
    ('docs/design/database-schema.md', 'Database schema proposal'),
    ('docs/design/schema-audit.md', 'Table and column audit'),
    ('docs/design/posting-and-integration.md', 'Posting and ERP integration'),
    ('docs/design/compliance-and-trade.md', 'Compliance and trade design'),
    ('db/README.md', 'Migration workflow'),
    ('docs/contribution-provenance.md', 'Contribution provenance'),
]

START = '<!-- reading-sequence:start -->'
END = '<!-- reading-sequence:end -->'

def strip_existing(text):
    while START in text:
        start = text.index(START)
        end = text.index(END, start) + len(END)
        text = text[:start] + text[end:]
    return text

def update_document(path):
    path = Path(path).resolve()
    index = next((i for i, (name, _) in enumerate(SEQUENCE) if (ROOT / name).resolve() == path), None)
    if index is None:
        raise ValueError(f'Document not in reading sequence: {path}')
    links = []
    for label, neighbor in [('Previous', index - 1), ('Next', index + 1)]:
        if 0 <= neighbor < len(SEQUENCE):
            destination, title = SEQUENCE[neighbor]
            relative = Path(os.path.relpath(ROOT / destination, path.parent)).as_posix()
            links.append(f'[{label}: {title}]({relative})')
    block = f'{START}\n' + ' | '.join(links) + f'\n{END}'
    content = strip_existing(path.read_text(encoding='utf-8')).strip()
    heading, rest = content.split('\n', 1)
    path.write_text(f'{heading}\n\n{block}\n\n{rest.strip()}\n\n{block}\n', encoding='utf-8')

if __name__ == '__main__':
    for name, _ in SEQUENCE:
        update_document(ROOT / name)
    print(f'Updated previous and next links on {len(SEQUENCE)} documents')
