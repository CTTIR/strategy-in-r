const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.env.FOOTER_PATH || 'style/after-body.html', 'utf8');
const script = [...source.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('.sidebar-downloads'));
async function render(available, reject = false) {
  let ready;
  const inserted = [];
  const anchor = { parentNode: { insertBefore: element => inserted.push(element) } };
  const item = { textContent: 'View source', href: 'https://github.com/CTTIR/strategy-in-r/blob/main/27-self-play-alphazero.Rmd', closest: () => anchor };
  const node = () => ({ children: [], appendChild(child) { this.children.push(child); } });
  vm.runInNewContext(script, {
    URL, window: { location: { href: 'https://example.test/sec-self-play.html', pathname: '/sec-self-play.html' } },
    document: { addEventListener: (_event, callback) => { ready = callback; }, querySelector: () => null, querySelectorAll: () => [item], createElement: node },
    fetch: async (href, options) => { assert.equal(options.method, 'HEAD'); if (reject) throw Error('offline'); return { ok: available.includes(href) }; },
  });
  await ready();
  const list = inserted.find(e => e.className === 'sidebar-downloads');
  return list ? list.children.map(e => e.children[0].href) : [];
}
test('absent optional artifacts do not produce broken download links', async () => {
  assert.deepEqual(await render([]), []);
});
test('chapter download follows the source filename rather than the HTML anchor', async () => {
  const files = ['strategy-in-r.pdf', 'strategy-in-r.epub', 'pdf-chapters/27-self-play-alphazero.pdf'];
  assert.deepEqual(await render(files), files);
});
test('partial format builds expose only their available artifacts', async () => {
  assert.deepEqual(await render(['strategy-in-r.epub']), ['strategy-in-r.epub']);
});
test('unreachable optional downloads leave reading available', async () => {
  assert.deepEqual(await render([], true), []);
});
