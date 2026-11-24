// Prints ebook.html to a PDF with Chromium (Playwright).
//   node render_pdf.js ebook.html out.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: output, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF written:', output);
})();
