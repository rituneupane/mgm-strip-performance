// Renders the share images from the dashboard (animations off):
//   images/report.png           full Overview page at 1280px (2x)
//   images/company.png, images/strengths.png, images/opportunities.png   other tabs (2x)
//   cover.png (and an optional copy path in argv[2])  1200x750 thumbnail of the whole Overview page
// Usage: NODE_PATH=<node_modules> node analysis/social.js [extra_cover_path]
const p = require('puppeteer-core'); const path = require('path'); const fs = require('fs');
const ROOT = path.resolve(__dirname, '..'); const URL = 'file://' + ROOT + '/docs/index.html';
const noAnim = () => { let C; Object.defineProperty(window, 'Chart', { configurable: true, get() { return C }, set(v) { C = v; try { v.defaults.animation = false; v.defaults.animations = false } catch (e) { } } }) };
async function open(b, w, scale, tab) {
  const pg = await b.newPage(); await pg.setViewport({ width: w, height: 800, deviceScaleFactor: scale });
  await pg.evaluateOnNewDocument(noAnim); await pg.goto(URL, { waitUntil: 'networkidle0' });
  await pg.evaluate(t => document.querySelector(`#tabs button[data-t="${t}"]`).click(), tab);
  await pg.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 800));
  const h = await pg.evaluate(() => document.documentElement.scrollHeight);
  await pg.setViewport({ width: w, height: h, deviceScaleFactor: scale }); await new Promise(r => setTimeout(r, 600));
  return [pg, h];
}
(async () => {
  const b = await p.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--font-render-hinting=none', '--allow-file-access-from-files'] });
  fs.mkdirSync(ROOT + '/images', { recursive: true });
  for (const [tab, name] of [['ov', 'report'], ['co', 'company'], ['st', 'strengths'], ['op', 'opportunities']]) {
    const [pg, h] = await open(b, 1280, 2, tab);
    await pg.screenshot({ path: `${ROOT}/images/${name}.png`, fullPage: true }); console.log(`images/${name}.png`, 2560, h * 2); await pg.close();
  }
  // Cover: whole Overview page at 1380px wide (about 1.6:1), scaled to fit 1200x750 on the page background.
  const [pg, h] = await open(b, 1380, 2, 'ov');
  const shot = (await pg.screenshot({ fullPage: true, encoding: 'base64' })); await pg.close();
  const cv = await b.newPage(); await cv.setViewport({ width: 1200, height: 750, deviceScaleFactor: 1 });
  const s = Math.min(1200 / 1380, 750 / h);
  await cv.setContent(`<html><body style="margin:0;width:1200px;height:750px;background:#FAF8F4;display:flex;align-items:center;justify-content:center;overflow:hidden">
    <img src="data:image/png;base64,${shot}" style="width:${Math.round(1380 * s)}px;height:${Math.round(h * s)}px;display:block"></body></html>`, { waitUntil: 'load' });
  const outs = [ROOT + '/cover.png'].concat(process.argv[2] ? [process.argv[2]] : []);
  for (const o of outs) { await cv.screenshot({ path: o, clip: { x: 0, y: 0, width: 1200, height: 750 } }); console.log(o, 'scale', s.toFixed(3), 'page', 1380, h); }
  await b.close();
})();
