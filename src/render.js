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
<p class="sub">観る順番・必須作品・優先度つきチェックリスト</p>
</div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, out] of [["essential", "doomsday-checklist-essential.pdf"], ["all", "doomsday-checklist-all.pdf"]]) {
    await page.goto("file://" + path.join(SRC, "print", `${name}.html`));
    await page.pdf({ path: path.join(ROOT, out), format: "A4", printBackground: true, preferCSSPageSize: true });
    console.log("pdf:", out);
  }
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(OG_HTML);
  await page.screenshot({ path: path.join(ROOT, "og.png") });
  console.log("og.png");
  await browser.close();
})();
