// Render the SVG sheets to a 4-page 11x17 PDF and PNG previews.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const dir = __dirname;
  const svgs = fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @page { size: 17in 11in; margin: 0 } body { margin: 0 }
    .p { width: 431.8mm; height: 279.4mm; page-break-after: always; overflow: hidden }
    .p:last-child { page-break-after: auto } svg { display: block }</style></head><body>` +
    svgs.map(f => `<div class="p">${fs.readFileSync(path.join(dir, f), 'utf8')}</div>`).join('') +
    `</body></html>`;
  await page.setContent(html);
  await page.pdf({ path: path.join(dir, 'Subarea1-drawings-11x17.pdf'), width: '17in', height: '11in',
                   printBackground: true, preferCSSPageSize: true });
  const prev = process.argv[2] || 'preview';
  fs.mkdirSync(path.resolve(dir, prev), { recursive: true });
  for (const f of svgs) {
    const p2 = await browser.newPage({ viewport: { width: 1632, height: 1056 }, deviceScaleFactor: +(process.argv[3] || 1) });
    await p2.setContent(`<html><body style="margin:0">${fs.readFileSync(path.join(dir, f), 'utf8')
      .replace(/width="431.8mm" height="279.4mm"/, 'width="1632" height="1056"')}</body></html>`);
    await p2.screenshot({ path: path.resolve(dir, prev, f.replace('.svg', '.png')) });
    await p2.close();
  }
  await browser.close();
  console.log('done', svgs);
})();
