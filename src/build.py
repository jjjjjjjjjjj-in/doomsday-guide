"""作品データと記事からサイト一式を生成する。

使い方: python3 src/build.py  （リポジトリのルートに index.html などを書き出す）
"""
import html
import os
import shutil
import sys
from urllib.parse import quote

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)

from titles_a import TITLES_A  # noqa: E402
from titles_b import TITLES_B  # noqa: E402
from titles_c import TITLES_C  # noqa: E402
from articles import ARTICLES  # noqa: E402
from importance import IMPORTANCE, MUST_LINE  # noqa: E402
import ads  # noqa: E402
from trailers import TRAILERS  # noqa: E402

BASE_URL = "https://jjjjjjjjjjj-in.github.io/doomsday-guide/"
UPDATED = "2026-10-31"

TITLES = TITLES_A + TITLES_B + TITLES_C
for i, t in enumerate(TITLES, 1):
    t["order"] = i
    t["imp"] = IMPORTANCE[t["slug"]]
    t["goal"] = t["imp"] == "goal"
    t["must"] = isinstance(t["imp"], int) and t["imp"] >= MUST_LINE


def imp_class(t):
    imp = t["imp"]
    if t["goal"]:
        return "goal"
    if not isinstance(imp, int):
        return "ref"
    return "p10" if imp >= 10 else "p8" if imp >= 8 else "p5" if imp >= MUST_LINE else "p0"


def imp_text(t):
    if t["goal"]:
        return "目的の作品"
    return f"重要度 {t['imp']}/10" if isinstance(t["imp"], int) else t["imp"]

CAT_LABEL = {"xmen": "X-MEN", "infinity": "インフィニティ・サーガ", "nextgen": "次世代ヒーロー",
             "multiverse": "マルチバース", "spider": "スパイダーマン関連", "other": "その他", "goal": "目的の作品"}



def trailer_button(t):
    """確認済みの公式予告編があるときだけ、別タブで開くリンクを出す（チャンネル検索のリンクは出さない）"""
    entry = TRAILERS.get(t["slug"])
    label = "公式予告編を見る（YouTube）"
    if not entry:
        return ""
    url, channel = entry
    return (f'<p class="trailer"><a class="btn trailer-btn" href="{e(url)}" target="_blank" rel="noopener">{label}</a>'
            f'<span class="trailer-src">{e(channel)}</span></p>')


def ad_buttons(t):
    """作品ごとの広告ボタン（ads.py に値があるものだけ出す）"""
    if t["goal"]:
        return ""
    out = []
    if ads.DISNEY_PLUS and t["slug"] not in ads.NOT_ON_DISNEY_PLUS:
        out.append(f'<a class="btn ad" href="{e(ads.DISNEY_PLUS)}" target="_blank" rel="sponsored noopener">Disney+で観る</a>')
    if ads.AMAZON_TAG:
        url = f'https://www.amazon.co.jp/s?k={quote(t["title"] + " Blu-ray")}&tag={quote(ads.AMAZON_TAG)}'
        out.append(f'<a class="btn ad" href="{e(url)}" target="_blank" rel="sponsored noopener">Amazonで探す</a>')
    if ads.RAKUTEN_TOP:
        out.append(f'<a class="btn ad" href="{e(rakuten_url(t["title"] + " Blu-ray"))}" target="_blank" rel="sponsored noopener">楽天で探す</a>')
    return f'<span class="ad-links">{"".join(out)}<span class="pr">PR</span></span>' if out else ""


def rakuten_url(keyword):
    """もしも経由で楽天の検索結果に飛ぶリンク（どこでもリンクと同じ形式）"""
    inner = f"https://search.rakuten.co.jp/search/mall/{quote(keyword)}/"
    return f"{ads.RAKUTEN_TOP}&url={quote(inner, safe='')}"


def amazon_url(key):
    """検索キーワードか "/gp/..." のパスから、タグ付きのAmazonリンクを作る"""
    path = key if key.startswith("/") else f"/s?k={quote(key)}"
    sep = "&" if "?" in path else "?"
    return f"https://www.amazon.co.jp{path}{sep}tag={quote(ads.AMAZON_TAG)}"


def amazon_links(picks):
    return "".join(f'<a class="btn ad" href="{e(amazon_url(key))}" target="_blank" rel="sponsored noopener">{e(label)}</a>'
                   for label, key in picks)


def amazon_picks(heading="予習のおとも"):
    """「予習のおとも」パネル。AMAZON_TAG がないときは出さない"""
    if not ads.AMAZON_TAG:
        return ""
    items = [amazon_links(ads.AMAZON_PICKS)]
    if ads.RAKUTEN_TOP:
        items.append(f'<a class="btn ad" href="{e(ads.RAKUTEN_TOP)}" target="_blank" rel="sponsored noopener">楽天市場でお買い物</a>')
    return f"""<section class="panel">
  <h2>{e(heading)} <span class="pr">PR</span></h2>
  <div class="btns">{"".join(items)}</div>
</section>
"""


def article_picks(slug):
    picks = ads.ARTICLE_PICKS.get(slug)
    if not (ads.AMAZON_TAG and picks):
        return ""
    return f'<aside class="panel inline-picks"><h2>この記事に関連するアイテム <span class="pr">PR</span></h2><div class="btns">{amazon_links(picks)}</div></aside>'


def sticky_bar(prefix=""):
    if not (ads.AMAZON_TAG and ads.STICKY_BAR):
        return ""
    label, key = ads.STICKY_BAR
    return f"""<div class="sticky-ad" id="sticky-ad" hidden>
  <span class="pr">PR</span><a href="{e(amazon_url(key))}" target="_blank" rel="sponsored noopener">{e(label)}</a>
  <button type="button" id="sticky-ad-close" aria-label="広告を閉じる">×</button>
</div>
<script src="{prefix}assets/sticky.js"></script>
"""


def banner(slot):
    code = ads.BANNERS.get(slot, "")
    return f'<aside class="banner" aria-label="広告"><span class="pr">PR</span>{code}</aside>' if code else ""

e = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&family=JetBrains+Mono:wght@500&display=swap">')


def head(title, desc, path, prefix=""):
    url = BASE_URL + path
    adsense = (f'\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ads.ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
               if ads.ADSENSE_CLIENT else "")
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
<link rel="stylesheet" href="{prefix}assets/site.css">{adsense}
</head>
<body>
<div class="wrap">
"""


def footer(prefix=""):
    disclosure = '<p>※当サイトはアフィリエイト広告（PR）を利用しています。</p>\n' if ads.enabled() else ""
    if ads.AMAZON_TAG:
        disclosure += '<p>Amazonのアソシエイトとして、当サイトは適格販売により収入を得ています。</p>\n'
    return banner("bottom") + f"""<footer>
{disclosure}<p>キャスト情報はマーベル・スタジオ／ディズニーの公式発表に基づいています（最終確認 {UPDATED}）。噂や報道の段階の情報はその旨を明記しています。重要度は公開前の公式情報をもとにした運営者の判断による目安で、公開後の内容を保証するものではありません。</p>
<p>出典：<a href="https://thewaltdisneycompany.com/news/marvel-studios-avengers-doomsday-cast/" rel="noopener">Marvel Studios Announces 'Avengers: Doomsday' Cast</a>／<a href="https://marvel.disney.co.jp/movie/avengers-doomsday" rel="noopener">『アベンジャーズ／ドゥームズデイ』日本公式サイト</a></p>
<p>当サイトは個人が運営する非公式ファンサイトです。Marvel Studios、The Walt Disney Company、Sony Pictures、20th Century Studios とは関係ありません。作品名・キャラクター名は各権利者の商標です。</p>
<p><a href="{prefix}">トップ</a> ・ <a href="{prefix}articles/cast.html">キャストまとめ</a> ・ <a href="{prefix}articles/x-men.html">X-MEN</a> ・ <a href="{prefix}articles/infinity-saga.html">インフィニティ・サーガ</a> ・ <a href="{prefix}articles/next-generation.html">次世代ヒーロー</a> ・ <a href="{prefix}articles/multiverse.html">マルチバース</a></p>
</footer>
</div>
"""


def row(t, anchor=True):
    """anchor=False のときは id を付けない（同じ作品が2つのリストに出るため）"""
    detail = ""
    if not t["goal"]:
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
      {trailer_button(t)}
      {ad_buttons(t)}
    </div>
  </details>"""
    return f"""<li class="row{' must' if t['must'] else ''}{' goal' if t['goal'] else ''}"{f' id="{t["slug"]}"' if anchor else ''} data-slug="{t["slug"]}" data-order="{t["order"]}">
  <label class="check"><input type="checkbox" data-watch="{t["slug"]}" aria-label="{e(t["title"])}を観た"><span class="box" aria-hidden="true"></span></label>
  <div class="main">
    <span class="meta"><span>視聴順 {t["order"]:02d}</span><span>作中 {e(t["era"])}</span><span>{e(t["year"])}年・{e(t["kind"])}</span></span>
    <h3 class="title">{e(t["title"])}</h3>
    <p class="desc">{e(t["line"])}</p>
  </div>
  <span class="pill {imp_class(t)}">{e(imp_text(t))}</span>{detail}
</li>"""


def build_index():
    must_total = sum(1 for t in TITLES if t["must"])
    total = len(TITLES) - 1
    desc = (f"『アベンジャーズ／ドゥームズデイ』の前に観るべきMCU作品を、10点満点の重要度つきで視聴順に整理。"
            f"重要度5以上の{must_total}本は必ず観たい作品。全{total}本の各作品にあらすじ・ドゥームズデイとの関連性・ポストクレジットの解説つき。")
    articles = "".join(f'<li><a href="articles/{a["slug"]}.html">{e(a["title"])}</a></li>' for a in ARTICLES)
    # ① に出る作品は ① に id を付け、② では ① に出ない作品だけに id を付ける（記事からのリンク先）
    must_rows = "".join(row(t) for t in TITLES if t["must"] or t["goal"])
    all_rows = "".join(row(t, anchor=not (t["must"] or t["goal"])) for t in TITLES)

    return head("ドゥームズデイ予習ガイド｜観る順番と重要度つき全作品リスト", desc, "") + f"""
<header class="hero">
  <p class="eyebrow">Unofficial Watch Guide · {total} titles</p>
  <h1>DOOMSDAY<small><span class="nb">アベンジャーズ／</span><span class="nb">ドゥームズデイ</span> <span class="nb">予習ガイド</span></small></h1>
  <p class="lead">マーベルが好きで、ちゃんと理解してから映画館に行きたい人のためのガイドです。全作品に10点満点の重要度をつけました。<strong>重要度5以上の{must_total}本は、必ず観てほしい作品</strong>です。各作品の「詳しく見る」で、あらすじや他作品とのつながり、観なかった場合に分からなくなることも確認できます。</p>
</header>

<section class="stats" aria-label="公開までの日数と視聴の進み具合">
  <div class="stat">
    <div class="stat-label">公開まで（2026年12月18日 日米同時公開）</div>
    <div class="stat-num" id="countdown">--<span>日</span></div>
  </div>
  <div class="stat">
    <div class="stat-label">必ず観るべき作品（重要度5以上）</div>
    <div class="stat-num" id="progress-must">0<span>/ {must_total}本</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-must"></i></div>
  </div>
  <div class="stat">
    <div class="stat-label">全作品</div>
    <div class="stat-num" id="progress-all">0<span>/ {total}本</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-all"></i></div>
  </div>
</section>
{banner("top")}
{amazon_picks()}<section class="panel">
  <h2>印刷用チェックリスト（PDF）</h2>
  <div class="btns">
    <a class="btn primary" href="doomsday-checklist-must.pdf" download>① 必ず観るべき作品（重要度5以上・{must_total}本）</a>
    <a class="btn" href="doomsday-checklist-all.pdf" download>② 全作品（{total}本）</a>
  </div>
</section>

<section class="panel">
  <h2>解説記事</h2>
  <ul class="article-list">{articles}</ul>
</section>

{banner("middle")}
<section class="tier-section">
  <header><h2>チェックリスト</h2><p>どちらのリストも物語の視聴順に並んでいます。『ロキ』シーズン1は『エンドゲーム』の直後に観るのがおすすめです。チェックは①と②で共通です。</p></header>
  <div class="controls">
    <a class="chip" href="#list-must">① 必ず観るべき（{must_total}本）</a>
    <a class="chip" href="#list-all">② 全作品（{total}本）</a>
    <label class="toggle"><input type="checkbox" id="hide-done"> 観た作品を隠す</label>
  </div>
  <div class="legend" aria-label="重要度の見方">
    <span><span class="pill p10">10</span>物語の柱</span>
    <span><span class="pill p8">8〜9</span>とても重要</span>
    <span><span class="pill p5">5〜7</span>観ておくべき</span>
    <span><span class="pill p0">4以下</span>余裕があれば</span>
    <span><span class="pill ref">参考</span>別の宇宙・番外</span>
  </div>
</section>

<section class="tier-section" id="list-must">
  <header><h2><span class="step">①</span>必ず観るべき作品<span class="count">重要度5以上・{must_total}本</span></h2><p>ドゥームズデイをちゃんと楽しむために、必ず観てほしい作品です。</p></header>
  <ol class="list">{must_rows}</ol>
</section>

{amazon_picks("①を観終わったら：予習のおとも")}
<section class="tier-section" id="list-all">
  <header><h2><span class="step">②</span>全作品<span class="count">{total}本</span></h2><p>重要度4以下や参考作品も含めた全作品です。時間がある人はこちらで。</p></header>
  <ol class="list">{all_rows}</ol>
</section>
""" + footer() + sticky_bar() + '<script src="assets/app.js"></script>\n</body>\n</html>\n'


def inject_article_picks(a):
    """記事の2つ目の見出しの前に関連アイテムを差し込む（見出しが1つ以下なら最後に置く）"""
    body, box = a["body"], article_picks(a["slug"])
    first = body.find("<h2>")
    second = body.find("<h2>", first + 1) if first >= 0 else -1
    return body[:second] + box + body[second:] if second > 0 else body + box


def build_article(a):
    others = "".join(f'<li><a href="{o["slug"]}.html">{e(o["title"])}</a></li>' for o in ARTICLES if o["slug"] != a["slug"])
    return head(a["title"] + "｜ドゥームズデイ予習ガイド", a["desc"], f'articles/{a["slug"]}.html', prefix="../") + f"""
<nav class="crumb"><a href="../">ドゥームズデイ予習ガイド</a> ＞ 解説記事</nav>
<article class="article">
  <h1>{e(a["title"])}</h1>
  <p class="updated">最終更新 {a["updated"]}</p>
  {inject_article_picks(a)}
  <p><a class="btn primary" href="../">チェックリストに戻る</a></p>
</article>
""" + amazon_picks() + f"""<section class="panel"><h2>ほかの解説記事</h2><ul class="article-list">{others}</ul></section>
""" + footer(prefix="../") + sticky_bar(prefix="../") + "</body>\n</html>\n"


def build_print(items, title, subtitle):
    """PDF用のHTML（Chromiumで印刷する）。元のPDFと同じ列構成"""
    rows_html = "".join(
        f'<tr class="{imp_class(t)}"><td class="cb">□</td><td class="no">{t["order"]:02d}</td>'
        f'<td class="sm">{e(t["era"])}</td>'
        f'<td><b>{e(t["title"])}</b><br><span class="sm">{e(t["line"])}</span></td>'
        f'<td><span class="pl {imp_class(t)}">{e(imp_text(t).replace("重要度 ", ""))}</span></td><td class="sm">{e(t["year"])}</td></tr>'
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
tr:nth-child(even) td {{ background: #f1f4f9; }}
.cb {{ font-size: 13pt; width: 14pt; }}
.no {{ font-weight: bold; width: 18pt; color: #556a88; }}
.sm {{ font-size: 8pt; color: #3c4f6b; }}
.pl {{ display: inline-block; font-size: 8pt; font-weight: bold; padding: 1pt 6pt; border-radius: 8pt; color: #fff; background: #7b8aa1; white-space: nowrap; }}
.pl.p10 {{ background: #c8192f; }} .pl.p8 {{ background: #c99500; }} .pl.p5 {{ background: #1d4a80; }}
.pl.ref {{ background: #fff; color: #556a88; border: .6pt solid #9aa9be; }} .pl.goal {{ background: #061629; }}
.foot {{ margin-top: 8pt; font-size: 7.5pt; color: #556a88; }}
</style></head><body>
<div class="band"><h1>DOOMSDAY</h1><p class="sub">アベンジャーズ／ドゥームズデイ 予習チェックリスト　{e(title)}</p></div>
<p class="note">{e(subtitle)} No.は物語の視聴順です。重要度は10点満点で、5以上は必ず観てほしい作品。『ロキ』S1は『エンドゲーム』の直後に観るのがおすすめです。</p>
<table><thead><tr><th>確認</th><th>No.</th><th>作中年代</th><th>作品・概要</th><th>重要度</th><th>公開年</th></tr></thead><tbody>{rows_html}</tbody></table>
<p class="foot">2026年12月18日 日米同時公開。キャスト情報は公式発表に基づく（{UPDATED}時点）。非公式ファンガイド：{BASE_URL}　Marvel Studios、The Walt Disney Company 等とは関係ありません。</p>
</body></html>"""


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "articles"), exist_ok=True)
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(ROOT, "assets", "site.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(ROOT, "assets", "app.js"))
    shutil.copy(os.path.join(SRC, "sticky.js"), os.path.join(ROOT, "assets", "sticky.js"))

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
    must = [t for t in TITLES if t["must"] or t["goal"]]
    with open(os.path.join(SRC, "print", "must.html"), "w", encoding="utf-8") as f:
        f.write(build_print(must, "① 必ず観るべき作品", f"重要度5以上の{len(must) - 1}本。"))
    with open(os.path.join(SRC, "print", "all.html"), "w", encoding="utf-8") as f:
        f.write(build_print(TITLES, "② 全作品", f"全{len(TITLES) - 1}本。トビー版スパイダーマンやヴェノムなどの参考作品も含みます。"))
    print(f"built: {len(TITLES)} titles, {len(ARTICLES)} articles, must {len(must) - 1} titles")


if __name__ == "__main__":
    main()
