// usage: node render.js <outdir> <html> <pdf> [png] [landscape|portrait]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [outdir, htmlName, pdfName, pngName, orient = 'landscape'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const land = orient === 'landscape';
  const page = await browser.newPage({ viewport: land ? { width: 1056, height: 816 } : { width: 816, height: 1056 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(outdir, htmlName));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.resolve(outdir, pdfName), width: land ? '11in' : '8.5in', height: land ? '8.5in' : '11in', printBackground: true, preferCSSPageSize: true });
  if (pngName && pngName !== '-') await page.screenshot({ path: path.resolve(outdir, pngName), fullPage: true });
  await browser.close();
})();
