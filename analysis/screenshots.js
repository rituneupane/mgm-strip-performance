// Headless Chrome screenshots of every dashboard tab at 1280px and 390px, animations off.
// Also asserts no horizontal overflow. Usage: node analysis/screenshots.js  (needs puppeteer-core; set NODE_PATH)
const p = require('puppeteer-core'); const path = require('path');
const ROOT = path.resolve(__dirname, '..'); const url = 'file://' + ROOT + '/docs/index.html';
const tabs = ['ov', 'co', 'st', 'op'], names = { ov: 'overview', co: 'company', st: 'strengths', op: 'opportunities' };
(async () => {
  const b = await p.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--font-render-hinting=none'] });
  const out = []; require('fs').mkdirSync(ROOT + '/screenshots', { recursive: true });
  for (const [w, scale, tag] of [[1280, 1, 'desktop'], [390, 2, 'mobile']]) {
    for (const t of tabs) {
      const pg = await b.newPage();
      await pg.setViewport({ width: w, height: 900, deviceScaleFactor: scale });
      await pg.evaluateOnNewDocument(() => { let C; Object.defineProperty(window, 'Chart', { configurable: true, get() { return C }, set(v) { C = v; try { v.defaults.animation = false; v.defaults.animations = false; v.defaults.transitions.active.animation.duration = 0 } catch (e) { } } }) });
      await pg.goto(url, { waitUntil: 'networkidle0' });
      await pg.evaluate(t => document.querySelector(`#tabs button[data-t="${t}"]`).click(), t);
      await new Promise(r => setTimeout(r, 700));
      const m = await pg.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth, h: document.documentElement.scrollHeight,
        wide: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > window.innerWidth + 1 && getComputedStyle(e).display !== 'none').map(e => e.tagName + '.' + e.className + '#' + e.id).slice(0, 5) }));
      await pg.setViewport({ width: w, height: m.h, deviceScaleFactor: scale }); await new Promise(r => setTimeout(r, 500));
      const f = `${ROOT}/screenshots/${tag}_${names[t]}.png`;
      await pg.screenshot({ path: f, fullPage: true });
      out.push({ f: path.basename(f), w, scrollWidth: m.sw, overflow: m.sw > m.iw, wide: m.wide, height: m.h }); await pg.close();
    }
  }
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
