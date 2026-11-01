// Renders scene.html to transparent PNG frames.
// usage: node render_overlay.js <outDir> <fps> <startFrame> <endFrame(excl)>
//        node render_overlay.js <outDir> times 1.2 3.4 ...   (stills, named by time)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [outDir, mode, ...rest] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1.5 });
  await page.goto('file://' + path.resolve(__dirname, 'scene.html') + (process.env.LANG_CUT ? '?lang=' + process.env.LANG_CUT : ''));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const shoot = async (t, file) => {
    await page.evaluate((t) => window.renderAt(t), t);
    await page.screenshot({ path: file, omitBackground: true });
  };
  if (mode === 'times') {
    for (const t of rest.map(Number)) await shoot(t, path.join(outDir, `t_${t.toFixed(2)}.png`));
  } else {
    const fps = Number(mode), a = Number(rest[0]), b = Number(rest[1]);
    for (let i = a; i < b; i++) await shoot(i / fps, path.join(outDir, `f_${String(i).padStart(5, '0')}.png`));
  }
  await browser.close();
})();
