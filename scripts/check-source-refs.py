#!/usr/bin/env python3
"""Check the configured Bookdown inputs, citations and cross-references."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
names = re.findall(r'^\s+-\s+["\']?([^"\'\n]+\.Rmd)["\']?\s*$',
                   (root / '_bookdown.yml').read_text(), re.M)
if not names or len(names) != len(set(names)):
    raise SystemExit('Expected a nonempty, unique Bookdown input list')
texts = [(root / name).read_text() for name in names]
all_text = '\n'.join(texts)
if len(re.findall(r'^# \(APPENDIX\)', all_text, re.M)) != 1:
    raise SystemExit('Expected one configured appendix marker')
for name, text in zip(names, texts):
    if not name.startswith('part-') and re.search(r'^# \((?:PART|APPENDIX)\)', text, re.M):
        raise SystemExit(f'{name}: duplicate part marker; use the dedicated Part input')
labels = set(re.findall(r'\{#([\w:-]+)', all_text))
labels.update(re.findall(r'\\#(eq:[\w-]+)', all_text))
for chunk in re.findall(r'^```\{r,?\s*([^,}\s]+)', all_text, re.M):
    labels.update(('fig:' + chunk, 'tab:' + chunk))
bibs = re.findall(r'bibliography:\s*\[([^\]]+)\]', texts[0])
if len(bibs) != 1:
    raise SystemExit('Expected the configured bibliography list in index.Rmd')
keys = set()
for name in bibs[0].split(','):
    keys.update(re.findall(r'@\w+\{([^,]+),', (root / name.strip(' \"\'')).read_text()))
missing = []
for name, text in zip(names, texts):
    prose = re.sub(r'^```.*?^```[^\n]*$', '', text, flags=re.M | re.S)
    prose = re.sub(r'`[^`]*`', '', prose)
    for ref in re.findall(r'\\@ref\(([^)]+)\)', prose):
        if ref not in labels:
            missing.append(f'{name}: missing cross-reference {ref}')
    for ref in re.findall(r'(?<![\\\w.])@([A-Za-z][\w-]*)', prose):
        if ref not in keys:
            missing.append(f'{name}: missing citation {ref}')
    if re.search(r'^title:', text, re.M) and re.search(r'^# .+\{#', text, re.M):
        missing.append(f'{name}: duplicate YAML and numbered chapter titles')
print(f'Checked {len(names)} inputs, {len(labels)} labels, {len(keys)} bibliography entries')
if missing:
    raise SystemExit('\n'.join(missing))
