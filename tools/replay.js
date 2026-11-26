// Offline replay: load app.html, inject the user's saved scan + scoreboard reads + ESPN game, run placement, print per-play table.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const d = JSON.parse(fs.readFileSync(process.argv[2] || 'play-clipper-debug.json', 'utf8'));
  const b = await chromium.launch(); const pg = await b.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.route('**/*', r => { const u = new URL(r.request().url()); if (u.hostname === 'app.local') { const f = path.join(require('path').resolve(__dirname, '..'), u.pathname.slice(1)); return fs.existsSync(f) ? r.fulfill({ path: f }) : r.fulfill({ status: 404, body: '' }); } if (/espn\.com/.test(u.hostname)) return r.fulfill({ contentType: 'application/json', body: '{"events":[]}' }); return r.fulfill({ status: 404, body: '' }); });
  await pg.goto('http://app.local/app.html'); await pg.waitForTimeout(800);
  const out = await pg.evaluate((d) => {
    const C = window.__clipper; C.reset = () => {}; C.runBug = () => {};
    C.state.game = d.game; C.state.duration = d.duration; C.samples = d.scan.samples; C.done = true; C.fileKey = d.fileKey;
    C._ss = C.samples.slice().sort((a, b) => a.t - b.t);
    const B2 = d.bug2; C.bug = B2.bug;
    C.bugOn = false; const base = C.detectGame();
    C.sbSnap = B2.sb; C.sbLong = B2.sbLong || {}; C.snapFix = B2.fix || {}; C.bugSnap = B2.snap || {}; C.kickSnap = B2.kick || {}; C.flagSnap = B2.flag || {}; C.tabM = B2.tabM || {};
    C.bugOn = true; const rawF = C.detectGame(); const fin = C.guardBug(rawF);
    const np = Object.fromEntries(fin.map(c => [c.id, c.snap]));
    const m = (a) => new Map(a.map(c => [c.id, c]));
    return { starts: fin.map(c => [c.id, c.start, c.snap]), raw: rawF.map(c => [c.id, c.snap, c.est]), base: [...m(base)].map(([k, c]) => [k, c.snap, c.est]), fin: [...m(fin)].map(([k, c]) => [k, c.snap, c.est, !!c.guarded, !!c.rescued]), np };
  }, d);
  fs.writeFileSync(process.argv[3] || 'replay-out.json', JSON.stringify(out)); console.log('ok', errs.slice(0, 5).join(' | '));
  await b.close();
})();
