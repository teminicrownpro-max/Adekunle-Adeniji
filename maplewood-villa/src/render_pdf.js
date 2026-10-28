// Render ../print.html to ../Maplewood-Villa.pdf (17 x 11 in, three sheets) and PNG previews.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1632, height: 1056 } });
  await page.goto('file://' + path.join(root, 'print.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(root, 'Maplewood-Villa.pdf'), width: '17in', height: '11in', printBackground: true, preferCSSPageSize: true });
  if (process.argv[2]) {
    const sheets = await page.$$('.page');
    for (let i = 0; i < sheets.length; i++) await sheets[i].screenshot({ path: path.join(process.argv[2], `sheet-${i + 1}.png`) });
  }
  await browser.close();
})();
