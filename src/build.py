"""作品データと記事からサイト一式を生成する。

使い方: python3 src/build.py  （リポジトリのルートに index.html などを書き出す）
"""
import html
import os
import shutil
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)

from titles_a import TITLES_A  # noqa: E402
from titles_b import TITLES_B  # noqa: E402
from titles_c import TITLES_C  # noqa: E402
from articles import ARTICLES  # noqa: E402

BASE_URL = "https://jjjjjjjjjjj-in.github.io/doomsday-guide/"
UPDATED = "2026-10-31"

TITLES = TITLES_A + TITLES_B + TITLES_C
for i, t in enumerate(TITLES, 1):
    t["order"] = i

TIER_LABEL = {"must": "必須級", "rec": "推奨", "opt": "任意", "low": "低優先度", "goal": "ゴール"}
CAT_LABEL = {"xmen": "X-MEN", "infinity": "インフィニティ・サーガ", "nextgen": "次世代ヒーロー",
             "multiverse": "マルチバース", "spider": "スパイダーマン関連", "other": "その他", "goal": "目的の作品"}

AFFILIATE = {}  # 例: {"endgame": "https://..."}  URLを入れた作品に「配信をチェック」ボタンが出る

e = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&family=JetBrains+Mono:wght@500&display=swap">')


def head(title, desc, path, prefix=""):
    url = BASE_URL + path
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ドゥームズデイ予習ガイド">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}og.png">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
<div class="wrap">
"""


def footer(prefix=""):
    disclosure = '<p>※当サイトはアフィリエイト広告（PR）を利用しています。</p>\n' if AFFILIATE else ""
    return f"""<footer>
{disclosure}<p>キャスト情報はマーベル・スタジオ／ディズニーの公式発表に基づいています（最終確認 {UPDATED}）。噂や報道の段階の情報はその旨を明記しています。優先度は公開前の公式情報から判断した目安で、公開後の内容を保証するものではありません。</p>
<p>出典：<a href="https://thewaltdisneycompany.com/news/marvel-studios-avengers-doomsday-cast/" rel="noopener">Marvel Studios Announces 'Avengers: Doomsday' Cast</a>／<a href="https://marvel.disney.co.jp/movie/avengers-doomsday" rel="noopener">『アベンジャーズ／ドゥームズデイ』日本公式サイト</a></p>
<p>当サイトは個人が運営する非公式ファンサイトです。Marvel Studios、The Walt Disney Company、Sony Pictures、20th Century Studios とは関係ありません。作品名・キャラクター名は各権利者の商標です。</p>
<p><a href="{prefix}">トップ</a> ・ <a href="{prefix}articles/cast.html">キャストまとめ</a> ・ <a href="{prefix}articles/x-men.html">X-MEN</a> ・ <a href="{prefix}articles/infinity-saga.html">インフィニティ・サーガ</a> ・ <a href="{prefix}articles/next-generation.html">次世代ヒーロー</a> ・ <a href="{prefix}articles/multiverse.html">マルチバース</a></p>
</footer>
</div>
"""


def row(t):
    tier = t["tier"]
    tags = "".join(f'<span class="tag">{e(CAT_LABEL[c])}</span>' for c in t["cats"] if c != "goal")
    if t["cast"]:
        tags += f'<span class="tag cast">出演：{e("、".join(t["cast"]))}</span>'
    aff = AFFILIATE.get(t["slug"])
    aff_html = f'<a class="btn" href="{e(aff)}" target="_blank" rel="sponsored noopener">配信をチェック</a>' if aff else ""
    detail = ""
    if tier != "goal":
        events = "".join(f"<li>{e(x)}</li>" for x in t["events"])
        detail = f"""
  <details>
    <summary>詳しく見る（あらすじ・関連性・ポストクレジット）</summary>
    <div class="detail">
      <p class="spoiler">※ネタバレを含みます</p>
      <dl>
        <div><dt>あらすじ</dt><dd>{e(t["story"])}</dd></div>
        <div><dt>重要な出来事</dt><dd><ul>{events}</ul></dd></div>
        <div><dt>登場人物</dt><dd>{e(t["chars"])}</dd></div>
        <div><dt>他作品との関係</dt><dd>{e(t["links"])}</dd></div>
        <div><dt>ドゥームズデイとの関連性</dt><dd>{e(t["dd"])}</dd></div>
        <div><dt>観るメリット</dt><dd>{e(t["merit"])}</dd></div>
        <div><dt>観なかった場合</dt><dd>{e(t["skip"])}</dd></div>
        <div><dt>ポストクレジット</dt><dd>{e(t["post"])}</dd></div>
      </dl>
      {aff_html}
    </div>
  </details>"""
    return f"""<li class="row {tier}" id="{t["slug"]}" data-slug="{t["slug"]}" data-order="{t["order"]}">
  <label class="check"><input type="checkbox" data-watch="{t["slug"]}" aria-label="{e(t["title"])}を観た"><span class="box" aria-hidden="true"></span></label>
  <div class="main">
    <span class="meta"><span>視聴順 {t["order"]:02d}</span><span>作中 {e(t["era"])}</span><span>{e(t["year"])}年・{e(t["kind"])}</span></span>
    <h3 class="title">{e(t["title"])}</h3>
    <p class="desc">{e(t["line"])}</p>
    <span class="tags">{tags}</span>
  </div>
  <span class="pill {tier}">{TIER_LABEL[tier]}</span>{detail}
</li>"""


def section(step, title, intro, items, sub=None):
    if sub:
        body = "".join(f'<h3>{e(label)}</h3><ol class="list">{"".join(row(t) for t in group)}</ol>' for label, group in sub)
    else:
        body = f'<ol class="list">{"".join(row(t) for t in items)}</ol>'
    return f"""<section class="tier-section">
  <header><h2><span class="step">{step}</span>{e(title)}<span class="count">{len(items)}本</span></h2><p>{intro}</p></header>
  {body}
</section>"""


def build_index():
    def primary(t):
        return t["cats"][0]
    must = [t for t in TITLES if t["tier"] == "must" and primary(t) != "xmen"]
    rec = [t for t in TITLES if t["tier"] == "rec" and primary(t) != "xmen"]
    xmen = [t for t in TITLES if primary(t) == "xmen"]
    opt = [t for t in TITLES if t["tier"] == "opt" and primary(t) != "xmen"]
    low = [t for t in TITLES if t["tier"] == "low" and primary(t) != "xmen"]
    goal = [t for t in TITLES if t["tier"] == "goal"]
    must_total = sum(1 for t in TITLES if t["tier"] == "must")
    x_must = [t["title"] for t in xmen if t["tier"] == "must"]

    desc = (f"『アベンジャーズ／ドゥームズデイ』の前に観るべきMCU・X-MEN作品を、公式キャストをもとに必須級・推奨・任意・低優先度に分類。"
            f"最低限の{must_total}本から全{len(TITLES) - 1}本まで、視聴順と各作品のあらすじ・関連性・ポストクレジットを解説した非公式ガイド。")
    sections = "\n".join([
        section("1", "最低限観るべき作品", f"ドゥームズデイの公式キャストや物語に直接つながる作品です。時間がない人はまずここから。X-MENの必須級2本（{e('・'.join(x_must))}）はセクション3にあります。", must),
        section("2", "理解を深める推奨作品", "キャラクターの背景や世界観が分かる作品です。ソー、アイアンマン、キャプテン・アメリカの単独作もここに入れています。", rec),
        section("3", "X-MENシリーズ（FOX版）", "ドゥームズデイに戻ってくる旧X-MENを理解するための作品です。優先度はそれぞれのラベルで確認できます。", xmen),
        section("4", "時間があれば観たい作品", "観なくてもドゥームズデイの理解に大きな支障はない作品です。「低優先度」は、現時点で関連が確認されていない、またはとても薄い作品で、関係がないと断定しているわけではありません。",
                opt + low, sub=[("任意", opt), ("低優先度", low)]),
        f'<section class="tier-section"><ol class="list">{"".join(row(t) for t in goal)}</ol></section>',
    ])
    articles = "".join(f'<li><a href="articles/{a["slug"]}.html">{e(a["title"])}</a></li>' for a in ARTICLES)

    out = head("ドゥームズデイ予習ガイド｜観る順番と必須作品", desc, "") + f"""
<header class="hero">
  <p class="eyebrow">Unofficial Watch Guide · {len(TITLES) - 1} titles</p>
  <h1>DOOMSDAY<small>アベンジャーズ／ドゥームズデイ 予習ガイド</small></h1>
  <p class="lead">MCUの全作品を観る必要はありません。公式キャストをもとに、観るべき作品を「必須級・推奨・任意・低優先度」に分けました。時間がない人は最低限の{must_total}本から。各作品の「詳しく見る」で、観なかった場合に何が分からなくなるかも確認できます。</p>
</header>

<section class="stats" aria-label="公開までの日数と視聴の進み具合">
  <div class="stat">
    <div class="stat-label">公開まで（2026年12月18日 日米同時公開）</div>
    <div class="stat-num" id="countdown">--<span>日</span></div>
  </div>
  <div class="stat">
    <div class="stat-label">最低限ルート（必須級）</div>
    <div class="stat-num" id="progress-must">0<span>/ {must_total}本</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-must"></i></div>
  </div>
  <div class="stat">
    <div class="stat-label">全作品</div>
    <div class="stat-num" id="progress-all">0<span>/ {len(TITLES) - 1}本</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-all"></i></div>
  </div>
</section>

<section class="panel">
  <h2>印刷用チェックリスト（PDF）</h2>
  <div class="btns">
    <a class="btn primary" href="doomsday-checklist-essential.pdf" download>① 必要性が高い作品だけ（必須級＋推奨）</a>
    <a class="btn" href="doomsday-checklist-all.pdf" download>② 時間がある人向け 全作品版</a>
  </div>
</section>

<section class="panel">
  <h2>解説記事</h2>
  <ul class="article-list">{articles}</ul>
</section>

<div class="controls" role="group" aria-label="並べ方">
  <button class="chip" data-view="priority" aria-pressed="true">優先度別</button>
  <button class="chip" data-view="order" aria-pressed="false">視聴順で全部</button>
  <label class="toggle"><input type="checkbox" id="hide-done"> 観た作品を隠す</label>
</div>
<div class="legend" aria-label="優先度の見方">
  <span><span class="pill must">必須級</span>理解に直接必要</span>
  <span><span class="pill rec">推奨</span>背景が分かる</span>
  <span><span class="pill opt">任意</span>観なくても支障は小さい</span>
  <span><span class="pill low">低優先度</span>現時点で関連が薄い・未確認</span>
</div>
<p class="callout">どのセクションも、作品は物語の視聴順に並んでいます。「視聴順で全部」に切り替えると、優先度に関係なく全作品を時系列で確認できます。『ロキ』シーズン1は『エンドゲーム』の直後に観るのがおすすめです。</p>

<div id="priority-view">
{sections}
</div>
<section id="order-view" class="tier-section" hidden>
  <header><h2>視聴順（全作品）</h2><p>優先度のラベルを見ながら、必要なものだけ選んで観てください。</p></header>
  <ol class="list" id="order-list"></ol>
</section>
""" + footer() + '<script src="assets/app.js"></script>\n</body>\n</html>\n'
    return out


def build_article(a):
    others = "".join(f'<li><a href="{o["slug"]}.html">{e(o["title"])}</a></li>' for o in ARTICLES if o["slug"] != a["slug"])
    return head(a["title"] + "｜ドゥームズデイ予習ガイド", a["desc"], f'articles/{a["slug"]}.html', prefix="../") + f"""
<nav class="crumb"><a href="../">ドゥームズデイ予習ガイド</a> ＞ 解説記事</nav>
<article class="article">
  <h1>{e(a["title"])}</h1>
  <p class="updated">最終更新 {a["updated"]}</p>
  {a["body"]}
  <p><a class="btn primary" href="../">チェックリストに戻る</a></p>
</article>
<section class="panel"><h2>ほかの解説記事</h2><ul class="article-list">{others}</ul></section>
""" + footer(prefix="../") + "</body>\n</html>\n"


def build_print(items, title, subtitle):
    """PDF用のHTML（Chromiumで印刷する）"""
    rows_html = "".join(
        f'<tr class="{t["tier"]}"><td class="cb">□</td><td class="no">{t["order"]:02d}</td>'
        f'<td><b>{e(t["title"])}</b><br><span class="sm">{e(t["line"])}</span></td>'
        f'<td class="sm">{e(t["era"])}<br>{e(t["year"])}</td><td><span class="pl {t["tier"]}">{TIER_LABEL[t["tier"]]}</span></td></tr>'
        for t in items)
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 14mm 12mm; }}
body {{ font-family: "IPAGothic", "IPAPGothic", sans-serif; color: #0b1d36; font-size: 10pt; margin: 0; }}
h1 {{ margin: 0; font-size: 26pt; letter-spacing: .04em; color: #061629; }}
.sub {{ margin: 2pt 0 8pt; font-size: 11pt; font-weight: bold; }}
.band {{ border-left: 5pt solid #c8192f; padding-left: 8pt; margin-bottom: 8pt; }}
.note {{ font-size: 8.5pt; color: #3c4f6b; margin: 0 0 8pt; }}
table {{ width: 100%; border-collapse: collapse; }}
thead th {{ background: #061629; color: #fff; font-size: 8.5pt; padding: 4pt; text-align: left; }}
td {{ padding: 4pt; border-bottom: .6pt solid #d5deea; vertical-align: top; }}
tr {{ page-break-inside: avoid; }}
tr.must td {{ background: #fbeef0; }}
.cb {{ font-size: 13pt; width: 14pt; }}
.no {{ font-weight: bold; width: 18pt; color: #556a88; }}
.sm {{ font-size: 8pt; color: #3c4f6b; }}
.pl {{ display: inline-block; font-size: 8pt; font-weight: bold; padding: 1pt 6pt; border-radius: 8pt; color: #fff; background: #7b8aa1; white-space: nowrap; }}
.pl.must {{ background: #c8192f; }} .pl.rec {{ background: #c99500; }} .pl.opt {{ background: #1d4a80; }}
.pl.low {{ background: #fff; color: #556a88; border: .6pt solid #9aa9be; }} .pl.goal {{ background: #061629; }}
.foot {{ margin-top: 8pt; font-size: 7.5pt; color: #556a88; }}
</style></head><body>
<div class="band"><h1>DOOMSDAY</h1><p class="sub">アベンジャーズ／ドゥームズデイ 予習チェックリスト　{e(title)}</p></div>
<p class="note">{e(subtitle)} 番号は物語の視聴順です。優先度：必須級＝理解に直接必要／推奨＝背景が分かる／任意＝観なくても支障は小さい／低優先度＝現時点で関連が薄い・未確認。</p>
<table><thead><tr><th></th><th>No.</th><th>作品</th><th>作中年代・公開</th><th>優先度</th></tr></thead><tbody>{rows_html}</tbody></table>
<p class="foot">2026年12月18日 日米同時公開。キャスト情報は公式発表に基づく（{UPDATED}時点）。非公式ファンガイド：{BASE_URL}　Marvel Studios、The Walt Disney Company 等とは関係ありません。</p>
</body></html>"""


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "articles"), exist_ok=True)
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(ROOT, "assets", "site.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(ROOT, "assets", "app.js"))

    def write(path, text):
        with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
            f.write(text)

    write("index.html", build_index())
    for a in ARTICLES:
        write(f'articles/{a["slug"]}.html', build_article(a))

    pages = [""] + [f'articles/{a["slug"]}.html' for a in ARTICLES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{BASE_URL}{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")

    # PDF用HTMLは src/print に書き出し、render.js でPDF化する
    os.makedirs(os.path.join(SRC, "print"), exist_ok=True)
    essential = [t for t in TITLES if t["tier"] in ("must", "rec", "goal")]
    with open(os.path.join(SRC, "print", "essential.html"), "w", encoding="utf-8") as f:
        f.write(build_print(essential, "① 必要性が高い作品", f"必須級と推奨の{len(essential) - 1}本。ソー、アイアンマン、キャプテン・アメリカの単独作も含みます。"))
    with open(os.path.join(SRC, "print", "all.html"), "w", encoding="utf-8") as f:
        f.write(build_print(TITLES, "② 時間がある人向け 全作品版", f"全{len(TITLES) - 1}本。トビー版スパイダーマンやヴェノムなど、任意・低優先度の作品も含みます。"))
    print(f"built: {len(TITLES)} titles, {len(ARTICLES)} articles, essential PDF {len(essential) - 1} titles")


if __name__ == "__main__":
    main()
