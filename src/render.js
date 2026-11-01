// PDF 2種と OG 画像を書き出す。build.py の後に実行: node src/render.js
const { chromium } = require("playwright");
const path = require("path");

const SRC = __dirname;
const ROOT = path.dirname(SRC);

const OG_HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
body { margin: 0; width: 1200px; height: 630px; background: #061629; color: #eef2f8; font-family: "IPAGothic", sans-serif; display: grid; align-content: center; padding: 0 90px; box-sizing: border-box; }
.band { border-left: 14px solid #c8192f; padding-left: 36px; }
.eyebrow { color: #e5b21a; font-size: 26px; letter-spacing: .2em; margin: 0 0 12px; }
h1 { font-size: 150px; margin: 0; line-height: 1; letter-spacing: .04em; font-weight: bold; }
p { font-size: 46px; margin: 18px 0 0; font-weight: bold; }
.sub { font-size: 30px; color: #93a6c2; font-weight: normal; margin-top: 22px; }
</style></head><body><div class="band">
<div class="eyebrow">UNOFFICIAL WATCH GUIDE</div>
<h1>DOOMSDAY</h1>
<p>アベンジャーズ／ドゥームズデイ 予習ガイド</p>
<p class="sub">観る順番・重要度つき全作品チェックリスト</p>
</div></body></html>`;

const esc = (x) => String(x).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function filmOg(o) {
  const t = Object.assign({ main: "#1d3a6b", deep: "#0b1a33", accent: "#e5b21a", soft: "#dbe6f5" }, o.theme);
  const ja = o.lang === "ja";
  const big = ja ? o.title : o.title.toUpperCase();
  const size = Math.min(132, Math.floor(900 / (big.length * (ja ? 1 : 0.62))));
  return `<!doctype html><html><head><meta charset="utf-8"><style>
body { margin: 0; width: 1200px; height: 630px; overflow: hidden; color: #fff; font-family: "IPAGothic", sans-serif;
  background: radial-gradient(circle at 88% 50%, ${t.main} 0, ${t.deep} 55%, #12060a 100%); position: relative; }
.ring { position: absolute; right: -60px; top: 75px; width: 480px; height: 480px; border-radius: 50%;
  border: 18px solid ${t.accent}; opacity: .22; }
.ring.r2 { right: 40px; top: 175px; width: 280px; height: 280px; border-width: 10px; opacity: .3; }
.box { position: absolute; left: 90px; top: 0; bottom: 0; display: grid; align-content: center; border-left: 14px solid ${t.accent}; padding-left: 40px; width: 960px; }
.eyebrow { color: ${t.accent}; font-size: 26px; letter-spacing: .2em; margin: 0 0 16px; font-weight: bold; }
h1 { font-size: ${size}px; white-space: nowrap; margin: 0; line-height: 1.05; font-weight: bold; letter-spacing: .02em; }
p { font-size: 50px; margin: 20px 0 0; font-weight: bold; }
.sub { font-size: 30px; color: ${t.soft}; font-weight: normal; margin-top: 18px; }
</style></head><body><div class="ring"></div><div class="ring r2"></div><div class="box">
<div class="eyebrow">${o.index ? "UNOFFICIAL FAN GUIDE" : (ja ? "MCU作品ガイド" : "MCU FILM GUIDE") + " · " + esc(o.year)}</div>
<h1>${esc(big)}</h1>
<p>${o.index ? (ja ? "作品ごとの完全ガイド" : "One complete guide per film") : (ja ? "完全ガイド" : "Complete Guide")}</p>
<p class="sub">${ja ? "あらすじ・相関図・用語をやさしく解説" : "Story, character map and key terms, explained simply"}</p>
</div></body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, out] of [["must", "doomsday-checklist-must.pdf"], ["all", "doomsday-checklist-all.pdf"],
                             ["en-must", "en/doomsday-checklist-must.pdf"], ["en-all", "en/doomsday-checklist-all.pdf"]]) {
    await page.goto("file://" + path.join(SRC, "print", `${name}.html`));
    await page.pdf({ path: path.join(ROOT, out), format: "A4", printBackground: true, preferCSSPageSize: true });
    console.log("pdf:", out);
  }
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(OG_HTML);
  await page.screenshot({ path: path.join(ROOT, "og.png") });
  console.log("og.png");
  // 作品ガイドの共有画像（作品ごと・日英）。ドゥームズデイの看板は出さない
  const fs = require("fs");
  for (const lang of ["ja", "en"]) {
    const f = path.join(SRC, "print", `og-films-${lang}.json`);
    if (!fs.existsSync(f)) continue;
    for (const o of JSON.parse(fs.readFileSync(f, "utf8"))) {
      fs.mkdirSync(path.dirname(path.join(ROOT, o.out)), { recursive: true });
      await page.setContent(filmOg(o));
      await page.screenshot({ path: path.join(ROOT, o.out) });
      console.log(o.out);
    }
  }
  await browser.close();
})();
