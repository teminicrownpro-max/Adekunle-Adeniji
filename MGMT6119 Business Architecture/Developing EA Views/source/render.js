// Usage: node render.js in.svg out.png [scale]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [inp, out, scaleArg] = process.argv.slice(2);
  const svg = fs.readFileSync(inp, 'utf8');
  const m = svg.match(/viewBox="0 0 (\d+) (\d+)"/);
  const w = +m[1], h = +m[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: +(scaleArg || 2) });
  await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}svg{display:block}</style></head><body>${svg}</body></html>`);
  await page.waitForTimeout(300);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h } });
  await browser.close();
})();
