// Combine the generated SVG sheets into one vector PDF (ARCH D, 36" x 24") and PNG previews.
// Usage: node render.cjs <svg_dir> <out_pdf> <png_dir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [svgDir, outPdf, pngDir] = process.argv.slice(2);
  const files = fs.readdirSync(svgDir).filter((f) => f.endsWith('.svg')).sort();
  const sheets = files.map((f) => fs.readFileSync(path.join(svgDir, f), 'utf8'));
  const browser = await chromium.launch();

  const page = await browser.newPage();
  const css = '@page{size:36in 24in;margin:0}html,body{margin:0;padding:0;background:#fff}' +
    'svg{display:block;width:36in;height:24in;break-after:page}';
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head>` +
    `<body>${sheets.join('\n')}</body></html>`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: outPdf, width: '36in', height: '24in', printBackground: true, preferCSSPageSize: true });

  fs.mkdirSync(pngDir, { recursive: true });
  const W = 3000, H = 2000;
  const shot = await browser.newPage({ viewport: { width: W, height: H } });
  for (let i = 0; i < files.length; i++) {
    const svg = sheets[i].replace('width="36in" height="24in"', `width="${W}" height="${H}"`);
    await shot.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}</style></head><body>${svg}</body></html>`, { waitUntil: 'load' });
    await shot.evaluate(() => document.fonts.ready);
    await shot.screenshot({ path: path.join(pngDir, files[i].replace('.svg', '.png')) });
  }
  await browser.close();
  console.log(`wrote ${outPdf} and ${files.length} previews`);
})();
