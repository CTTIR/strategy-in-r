#!/usr/bin/env python3
"""Fail on unresolved section references or citations in the book sources."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
names = re.findall(r"^\s+- (.+\.qmd)$", (root/'_quarto.yml').read_text(), re.M)
texts = [(root/name).read_text() for name in names]
labels = set(re.findall(r"\{#(sec-[\w-]+)", '\n'.join(texts)))
keys = set(re.findall(r"@\w+\{([^,]+),", (root/'references.bib').read_text()))
missing = []
for name,text in zip(names,texts):
    # Code can use @ as an operator or in strings; inspect prose only.
    prose = re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.M|re.S)
    prose = re.sub(r"`[^`]*`", "", prose)
    for ref in re.findall(r"(?<![\w.])@([A-Za-z][\w-]*)", prose):
        if ref.startswith('sec-') and ref not in labels:
            missing.append(f"{name}: missing section {ref}")
        elif not ref.startswith(('sec-','fig-','tbl-','eq-')) and ref not in keys:
            missing.append(f"{name}: missing citation {ref}")
print(f"Checked {len(names)} inputs, {len(labels)} section labels, {len(keys)} bibliography entries")
if missing:
    raise SystemExit('\n'.join(missing))

# A chapter must choose YAML title or H1, not both (otherwise it is numbered twice).
for path in Path('.').rglob('*.qmd'):
    text=path.read_text()
    if re.search(r'^title:',text,re.M) and re.search(r'^# ',text,re.M):
        raise SystemExit(f'Duplicate chapter title: {path}')
