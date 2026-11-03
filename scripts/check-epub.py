"""Check EPUB XML and internal references without modifying the archive."""
from pathlib import Path
import argparse, json, posixpath, urllib.parse, zipfile
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('epub', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
issues = []
references = 0
with zipfile.ZipFile(args.epub) as archive:
    names = set(archive.namelist())
    if archive.testzip() is not None:
        issues.append('ZIP checksum error')
    if archive.read('mimetype') != b'application/epub+zip':
        issues.append('Invalid mimetype')
    docs = {}
    for name in names:
        if name.endswith(('.xhtml', '.opf', '.ncx', '.xml')):
            try:
                docs[name] = ET.fromstring(archive.read(name))
            except ET.ParseError as error:
                issues.append(f'{name}: {error}')
    ids = {name: {e.attrib['id'] for e in root.iter() if 'id' in e.attrib}
           for name, root in docs.items()}
    for name, root in docs.items():
        all_ids = [e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        if len(all_ids) != len(ids[name]):
            issues.append(f'{name}: duplicate IDs')
        for element in root.iter():
            for attribute in ('href', 'src', 'full-path'):
                if attribute not in element.attrib:
                    continue
                url = urllib.parse.urlsplit(element.attrib[attribute])
                if url.scheme or url.netloc:
                    continue
                references += 1
                # Container full-path is relative to the archive root.
                directory = '' if attribute == 'full-path' else posixpath.dirname(name)
                target = (posixpath.normpath(posixpath.join(directory,
                          urllib.parse.unquote(url.path))) if url.path else name)
                if target not in names:
                    issues.append(f'{name}: missing {target}')
                elif url.fragment and target in ids and urllib.parse.unquote(url.fragment) not in ids[target]:
                    issues.append(f'{name}: missing {target}#{url.fragment}')
    count = sum(name.endswith('.xhtml') for name in names)
    if count == 0:
        issues.append('No XHTML documents')
result = {'xhtml_documents': count, 'local_references': references, 'issues': issues}
args.output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(bool(issues))
