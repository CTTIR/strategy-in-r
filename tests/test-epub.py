"""Exercise real Pandoc conversion of HTML-only tables and inline images."""
from pathlib import Path
import subprocess, tempfile, zipfile, xml.etree.ElementTree as ET
import base64, sys
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    d=Path(td)
    (d/'pixel.png').write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aS1EAAAAASUVORK5CYII='))
    source='''# Content

<a href="https://example.com"><img alt width="1" src="pixel.png"></a>

<a href="#destination">Next chapter</a>

<div id="result"><table><thead><tr><th style>Measure</th><th>Value</th></tr></thead><tbody><tr><td>Score</td><td>0.5</td></tr></tbody></table></div>

# Destination {#destination}

Reached.
'''
    (d/'input.md').write_text(source)
    args=['pandoc','input.md','-t','epub3','-o','out.epub','--lua-filter='+str(root/'scripts/epub-html.lua')]
    if '--no-filter' in sys.argv: args = args[:-1]
    subprocess.run(args,cwd=d,check=True,capture_output=True)
    with zipfile.ZipFile(d/'out.epub') as z:
        chapters=[ET.fromstring(z.read(n)) for n in z.namelist() if n.endswith('.xhtml')]
    ns={'x':'http://www.w3.org/1999/xhtml'}
    assert any(x.findall('.//x:img',ns) for x in chapters)
    assert any(a.get('href') == 'ch002.xhtml#destination' for x in chapters for a in x.findall('.//x:a',ns))
    assert any(x.findall('.//x:table',ns) for x in chapters)
    assert any('Score' in ''.join(x.itertext()) and '0.5' in ''.join(x.itertext()) for x in chapters)
    assert any(x.findall('.//x:div[@id="result"]',ns) for x in chapters)
    before=subprocess.check_output(['pandoc','input.md','-t','html4'],cwd=d)
    after=subprocess.check_output(['pandoc','input.md','-t','html4','--lua-filter='+str(root/'scripts/epub-html.lua')],cwd=d)
    assert before==after
print('EPUB XML, table values/identity, image preservation and unchanged HTML passed')
