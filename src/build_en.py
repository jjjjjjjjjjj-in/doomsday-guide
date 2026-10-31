"""英語版のページを /en/ に書き出す。build.py の main() から呼ばれる。

作品の並び・重要度・予告編・広告は日本語版と同じものを使い、文章だけ src/en/ の英語データに差し替える。
"""
import os
import sys
from urllib.parse import quote

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SRC, "en"))

import build as ja  # noqa: E402
import ads  # noqa: E402
from build import (BASE_URL, UPDATED, TITLES, TRAILERS, MUST_LINE, imp_class, jsonld,  # noqa: E402,F401
                   amazon_url, rakuten_url, banner, e, head)
from titles_en_a import TITLES_EN_A  # noqa: E402
from titles_en_b import TITLES_EN_B  # noqa: E402
from titles_en_c import TITLES_EN_C  # noqa: E402
from articles_en import ARTICLES_EN  # noqa: E402

SITE_NAME = ja.SITE_NAMES["en"]
EN = {**TITLES_EN_A, **TITLES_EN_B, **TITLES_EN_C}

# 日本語版の広告ラベル → 英語のラベル（検索キーワードは日本語版と同じ）
PICK_LABELS = {
    "Fire TV Stick（Disney+をテレビの大画面で）": "Fire TV Stick (watch Disney+ on the big screen)",
    "マーベルのレゴ": "Marvel LEGO",
    "マーベルのTシャツ": "Marvel T-shirts",
    "アベンジャーズのフィギュア": "Avengers figures",
    "マーベルのマグカップ・雑貨": "Marvel mugs and goods",
    "家で映画館気分：ポップコーン": "Movie night at home: popcorn",
    "アメコミ（日本語版）": "Marvel comics (Japanese editions)",
    "Amazonタイムセール": "Amazon deals",
    "Amazon売れ筋ランキング": "Amazon best sellers",
    "ドクター・ドゥームのグッズ": "Doctor Doom goods",
    "X-MENのフィギュア": "X-Men figures",
    "X-MEN 旧3部作のBlu-ray": "Original X-Men trilogy on Blu-ray",
    "インフィニティ・ガントレットのグッズ": "Infinity Gauntlet goods",
    "キャプテン・アメリカの盾グッズ": "Captain America shield goods",
    "ブラックパンサーのグッズ": "Black Panther goods",
    "ロキのグッズ": "Loki goods",
    "デッドプールのグッズ": "Deadpool goods",
}


US = bool(ads.AMAZON_TAG_US)  # アメリカのAmazonのタグがあれば、英語版の広告は amazon.com だけにする


def shop_url(key):
    """英語版の Amazon リンク（US タグがあれば amazon.com、なければ日本語版と同じ amazon.co.jp）"""
    if not US:
        return amazon_url(key)
    path = key if key.startswith("/") else f"/s?k={quote(key)}"
    sep = "&" if "?" in path else "?"
    return f"https://www.amazon.com{path}{sep}tag={quote(ads.AMAZON_TAG_US)}"


def t_en(t):
    """日本語版の作品データに英語の文章を重ねたもの"""
    return {**t, **EN[t["slug"]]}


def imp_text(t):
    if t["goal"]:
        return "The goal"
    if isinstance(t["imp"], int):
        return f"Importance {t['imp']}/10"
    return {"参考": "Reference", "未評価": "Not rated"}.get(t["imp"], t["imp"])


def trailer_button(t):
    entry = TRAILERS.get(t["slug"])
    if not entry:
        return ""
    url, channel = entry
    channel = channel.replace(" 公式チャンネル", " (official channel)")
    return (f'<p class="trailer"><a class="btn trailer-btn" href="{e(url)}" target="_blank" rel="noopener">Watch the official trailer (YouTube)</a>'
            f'<span class="trailer-src">{e(channel)}</span></p>')


def ad_buttons(t):
    if t["goal"]:
        return ""
    out = []
    if ads.DISNEY_PLUS and t["slug"] not in ads.NOT_ON_DISNEY_PLUS:
        out.append(f'<a class="btn ad" href="{e(ads.DISNEY_PLUS)}" target="_blank" rel="sponsored noopener">Watch on Disney+</a>')
    if US or ads.AMAZON_TAG:
        out.append(f'<a class="btn ad" href="{e(shop_url(t["title"] + " Blu-ray"))}" target="_blank" rel="sponsored noopener">{"Search on Amazon" if US else "Search on Amazon.co.jp"}</a>')
    if ads.RAKUTEN_TOP and not US:
        out.append(f'<a class="btn ad" href="{e(rakuten_url(t["title"] + " Blu-ray"))}" target="_blank" rel="sponsored noopener">Search on Rakuten</a>')
    return f'<span class="ad-links">{"".join(out)}<span class="pr">Ad</span></span>' if out else ""


def amazon_links(picks):
    return "".join(f'<a class="btn ad" href="{e(shop_url(key))}" target="_blank" rel="sponsored noopener">{e(PICK_LABELS.get(label, label))}</a>'
                   for label, key in picks)


def amazon_picks(heading="Movie night extras"):
    if not (US or ads.AMAZON_TAG):
        return ""
    items = [amazon_links(ads.AMAZON_PICKS_US if US else ads.AMAZON_PICKS)]
    if ads.RAKUTEN_TOP and not US:
        items.append(f'<a class="btn ad" href="{e(ads.RAKUTEN_TOP)}" target="_blank" rel="sponsored noopener">Shop on Rakuten</a>')
    return f"""<section class="panel">
  <h2>{e(heading)} <span class="pr">Ad</span></h2>
  <div class="btns">{"".join(items)}</div>
</section>
"""


def article_picks(slug):
    picks = (ads.ARTICLE_PICKS_US if US else ads.ARTICLE_PICKS).get(slug)
    if not ((US or ads.AMAZON_TAG) and picks):
        return ""
    return f'<aside class="panel inline-picks"><h2>Related items <span class="pr">Ad</span></h2><div class="btns">{amazon_links(picks)}</div></aside>'


def sticky_bar(prefix):
    if not ((US or ads.AMAZON_TAG) and ads.STICKY_BAR):
        return ""
    _, key = ads.STICKY_BAR
    return f"""<div class="sticky-ad" id="sticky-ad" hidden>
  <span class="pr">Ad</span><a href="{e(shop_url(key))}" target="_blank" rel="sponsored noopener">See today's Amazon deals</a>
  <button type="button" id="sticky-ad-close" aria-label="Close ad">×</button>
</div>
<script src="{prefix}assets/sticky.js"></script>
"""


def footer(prefix, ja_link):
    """prefix は /en/ のトップへの相対パス、ja_link は同じ内容の日本語ページ"""
    disclosure = '<p>This site contains affiliate links (ads).</p>\n' if ads.enabled() else ""
    if US or ads.AMAZON_TAG:
        disclosure += '<p>As an Amazon Associate, this site earns from qualifying purchases.</p>\n'
    return banner("bottom") + f"""<footer>
{disclosure}<p>Cast information is based on official announcements from Marvel Studios and Disney (last checked {UPDATED}). Reported or rumored information is labeled as such. Importance ratings are the site owner's estimates based on official information before release and do not guarantee anything about the film.</p>
<p>Sources: <a href="https://thewaltdisneycompany.com/news/marvel-studios-avengers-doomsday-cast/" rel="noopener">Marvel Studios Announces 'Avengers: Doomsday' Cast</a> / <a href="https://marvel.disney.co.jp/movie/avengers-doomsday" rel="noopener">Avengers: Doomsday official site (Japan)</a></p>
<p>For how this site uses analytics (Google Analytics) and ads, see the <a href="{ja.PRIVACY_URL}#en">privacy policy</a>.</p>
<p>This is an unofficial fan site run by an individual. It is not affiliated with Marvel Studios, The Walt Disney Company, Sony Pictures or 20th Century Studios. Titles and character names are trademarks of their respective owners.</p>
<p><a href="{prefix}">Home</a> · <a href="{prefix}articles/cast.html">Cast</a> · <a href="{prefix}articles/x-men.html">X-Men</a> · <a href="{prefix}articles/infinity-saga.html">Infinity Saga</a> · <a href="{prefix}articles/next-generation.html">Next generation</a> · <a href="{prefix}articles/multiverse.html">Multiverse</a> · <a href="{ja_link}" hreflang="ja" lang="ja">日本語</a></p>
</footer>
</div>
"""


def row(t, anchor=True):
    detail = ""
    if not t["goal"]:
        events = "".join(f"<li>{e(x)}</li>" for x in t["events"])
        detail = f"""
  <details>
    <summary>More details (story, connections, post-credits)</summary>
    <div class="detail">
      <p class="spoiler">Contains spoilers</p>
      <dl>
        <div><dt>Story</dt><dd>{e(t["story"])}</dd></div>
        <div><dt>Key events</dt><dd><ul>{events}</ul></dd></div>
        <div><dt>Characters</dt><dd>{e(t["chars"])}</dd></div>
        <div><dt>Connections to other titles</dt><dd>{e(t["links"])}</dd></div>
        <div><dt>Connection to Doomsday</dt><dd>{e(t["dd"])}</dd></div>
        <div><dt>Why watch it</dt><dd>{e(t["merit"])}</dd></div>
        <div><dt>If you skip it</dt><dd>{e(t["skip"])}</dd></div>
        <div><dt>Post-credits</dt><dd>{e(t["post"])}</dd></div>
      </dl>
      {trailer_button(t)}
      {ad_buttons(t)}
    </div>
  </details>"""
    return f"""<li class="row{' must' if t['must'] else ''}{' goal' if t['goal'] else ''}"{f' id="{t["slug"]}"' if anchor else ''} data-slug="{t["slug"]}" data-order="{t["order"]}">
  <label class="check"><input type="checkbox" data-watch="{t["slug"]}" aria-label="Watched {e(t["title"])}"><span class="box" aria-hidden="true"></span></label>
  <div class="main">
    <span class="meta"><span>Order {t["order"]:02d}</span><span>Set in {e(t["era"])}</span><span>{e(t["year"])} · {e(t["kind"])}</span></span>
    <h3 class="title">{e(t["title"])}</h3>
    <p class="desc">{e(t["line"])}</p>{trailer_button(t) if t["goal"] else ""}
  </div>
  <span class="pill {imp_class(t)}">{e(imp_text(t))}</span>{detail}
</li>"""


def build_index(titles):
    must_total = sum(1 for t in titles if t["must"])
    total = len(titles) - 1
    desc = (f"What to watch before Avengers: Doomsday. Every MCU and related title in story order with a 10-point importance rating. "
            f"The {must_total} titles rated 5 or higher are must-watches. All {total} titles come with a story summary, the connection to Doomsday and post-credits notes.")
    articles = "".join(f'<li><a href="articles/{a["slug"]}.html">{e(a["title"])}</a></li>' for a in ARTICLES_EN)
    must_rows = "".join(row(t) for t in titles if t["must"] or t["goal"])
    all_rows = "".join(row(t, anchor=not (t["must"] or t["goal"])) for t in titles)
    top = [t for t in titles if t["imp"] == 10 and not t["goal"]]
    x_must = [t for t in titles if "xmen" in t["cats"] and t["must"]]
    faq = [
        ("Do I need to watch every Marvel title before Doomsday?",
         f"No. This guide marks the {must_total} titles rated 5 or higher as must-watches. If you are short on time, start with the titles rated 10."),
        ("Where should I start?",
         "Start from number 01 on the checklist, Captain America: The First Avenger, and go in order. The list follows the story's timeline, so the connections are easier to follow."),
        ("Which titles matter most?",
         "The titles rated 10: " + ", ".join(t["title"] for t in top) + "."),
        ("Should I watch the X-Men films too?",
         "The classic X-Men return in Doomsday, so we recommend " + ", ".join(t["title"] for t in x_must) + ". See the X-Men article for details."),
        ("When does Avengers: Doomsday come out?",
         "December 18, 2026 (Friday), in the US and Japan."),
    ]
    faq_html = "".join(f'<div class="faq-item"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in faq)
    url = BASE_URL + "en/"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": SITE_NAME, "url": url, "inLanguage": "en"},
            {"@type": "ItemList", "name": f"Must-watch titles before Doomsday (importance 5+, {must_total} titles)",
             "itemListOrder": "https://schema.org/ItemListOrderAscending", "numberOfItems": must_total,
             "itemListElement": [{"@type": "ListItem", "position": i, "name": t["title"], "url": f'{url}#{t["slug"]}'}
                                 for i, t in enumerate([t for t in titles if t["must"]], 1)]},
        ],
    }
    return head(f"Avengers: Doomsday Watch Order | {must_total} Must-Watch MCU Titles and Importance Ratings", desc, "en/",
                prefix="../", schema=schema, lang="en") + f"""
<header class="hero">
  <p class="eyebrow">Unofficial Watch Guide · {total} titles</p>
  <h1>DOOMSDAY<small><span class="nb">Avengers: Doomsday</span> <span class="nb">Watch Guide</span></small></h1>
  <p class="lead">A guide for Marvel fans who want to understand the story properly before heading to the theater. Every title has a 10-point importance rating. <strong>The {must_total} titles rated 5 or higher are the ones you should not miss.</strong> Open "More details" on any title to see the story, how it connects to other titles, and what you might miss if you skip it.</p>
  <p class="updated-on">Last updated {UPDATED} · <a href="../" hreflang="ja" lang="ja">日本語</a></p>
</header>

<section class="stats" aria-label="Days until release and your progress">
  <div class="stat">
    <div class="stat-label">Days until release (December 18, 2026)</div>
    <div class="stat-num" id="countdown">--<span>days</span></div>
  </div>
  <div class="stat">
    <div class="stat-label">Must-watch titles (importance 5+)</div>
    <div class="stat-num" id="progress-must">0<span>/ {must_total}</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-must"></i></div>
  </div>
  <div class="stat">
    <div class="stat-label">All titles</div>
    <div class="stat-num" id="progress-all">0<span>/ {total}</span></div>
    <div class="bar" aria-hidden="true"><i id="bar-all"></i></div>
  </div>
</section>
{banner("top")}
{amazon_picks()}<section class="panel">
  <h2>Printable checklists (PDF)</h2>
  <div class="btns">
    <a class="btn primary" href="doomsday-checklist-must.pdf" download>① Must-watch titles (importance 5+, {must_total})</a>
    <a class="btn" href="doomsday-checklist-all.pdf" download>② All titles ({total})</a>
  </div>
</section>

<section class="panel">
  <h2>Articles</h2>
  <ul class="article-list">{articles}</ul>
</section>

{banner("middle")}
<section class="tier-section">
  <header><h2>Checklist</h2><p>Both lists follow the story's viewing order. We recommend watching Loki Season 1 right after Endgame. Your checks are shared between ① and ②.</p></header>
  <div class="controls">
    <a class="chip" href="#list-must">① Must-watch ({must_total})</a>
    <a class="chip" href="#list-all">② All titles ({total})</a>
    <label class="toggle"><input type="checkbox" id="hide-done"> Hide watched titles</label>
  </div>
  <div class="legend" aria-label="How to read the importance ratings">
    <span><span class="pill p10">10</span>Pillar of the story</span>
    <span><span class="pill p8">8-9</span>Very important</span>
    <span><span class="pill p5">5-7</span>Should watch</span>
    <span><span class="pill p0">4 or less</span>If you have time</span>
    <span><span class="pill ref">Reference</span>Other universes and extras</span>
  </div>
</section>

<section class="tier-section" id="list-must">
  <header><h2><span class="step">①</span>Must-watch titles<span class="count">importance 5+ · {must_total}</span></h2><p>The titles to watch so you can fully enjoy Doomsday.</p></header>
  <ol class="list">{must_rows}</ol>
</section>

{amazon_picks("Done with ①? Movie night extras")}
<section class="tier-section" id="list-all">
  <header><h2><span class="step">②</span>All titles<span class="count">{total}</span></h2><p>Every title, including those rated 4 or lower and reference titles. For when you have more time.</p></header>
  <ol class="list">{all_rows}</ol>
</section>

<section class="tier-section faq" id="faq">
  <header><h2>FAQ</h2></header>
  {faq_html}
</section>
""" + footer("./", "../") + sticky_bar("../") + '<script src="../assets/app.js"></script>\n</body>\n</html>\n'


def build_article(a):
    others = "".join(f'<li><a href="{o["slug"]}.html">{e(o["title"])}</a></li>' for o in ARTICLES_EN if o["slug"] != a["slug"])
    url = f'{BASE_URL}en/articles/{a["slug"]}.html'
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": a["title"], "description": a["desc"], "inLanguage": "en",
             "datePublished": a["updated"], "dateModified": a["updated"], "mainEntityOfPage": url,
             "image": f"{BASE_URL}og.png",
             "author": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "en/"},
             "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "en/"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": BASE_URL + "en/"},
                {"@type": "ListItem", "position": 2, "name": a["title"], "item": url}]},
        ],
    }
    body, box = a["body"], article_picks(a["slug"])
    first = body.find("<h2>")
    second = body.find("<h2>", first + 1) if first >= 0 else -1
    body = body[:second] + box + body[second:] if second > 0 else body + box
    return head(f'{a["title"]} | {SITE_NAME}', a["desc"], f'en/articles/{a["slug"]}.html', prefix="../../", schema=schema, lang="en") + f"""
<nav class="crumb"><a href="../">{SITE_NAME}</a> &gt; Articles · <a href="../../articles/{a["slug"]}.html" hreflang="ja" lang="ja">日本語</a></nav>
<article class="article">
  <h1>{e(a["title"])}</h1>
  <p class="updated">Last updated {a["updated"]}</p>
  {body}
  <p><a class="btn primary" href="../">Back to the checklist</a></p>
</article>
""" + amazon_picks() + f"""<section class="panel"><h2>More articles</h2><ul class="article-list">{others}</ul></section>
""" + footer("../", f'../../articles/{a["slug"]}.html') + sticky_bar("../../") + "</body>\n</html>\n"


def build_print(items, title, subtitle):
    """英語版PDF用のHTML（日本語版と同じ見た目）"""
    page = ja.build_print(items, title, subtitle)
    swaps = [
        ('<html lang="ja">', '<html lang="en">'),
        ("アベンジャーズ／ドゥームズデイ 予習チェックリスト　", "Avengers: Doomsday Watch Checklist · "),
        ("No.は物語の視聴順です。重要度は10点満点で、5以上は必ず観てほしい作品。『ロキ』S1は『エンドゲーム』の直後に観るのがおすすめです。",
         "No. is the story's viewing order. Importance is out of 10; titles rated 5 or higher are must-watches. Watch Loki Season 1 right after Endgame."),
        ('">Importance ', '">'),
        ("<th>確認</th><th>No.</th><th>作中年代</th><th>作品・概要</th><th>重要度</th><th>公開年</th>",
         "<th>✓</th><th>No.</th><th>Set in</th><th>Title</th><th>Importance</th><th>Released</th>"),
        ("2026年12月18日 日米同時公開。キャスト情報は公式発表に基づく（", "In theaters December 18, 2026. Cast information is based on official announcements (as of "),
        ("時点）。非公式ファンガイド：", "). Unofficial fan guide: "),
        ("en/　Marvel Studios、The Walt Disney Company 等とは関係ありません。", "en/ — not affiliated with Marvel Studios, The Walt Disney Company or others."),
    ]
    for a, b in swaps:
        page = page.replace(a, b)
    return page


def write_all(write):
    """英語版を書き出し、サイトマップ用の (パス, 更新日) を返す"""
    titles = [t_en(t) for t in TITLES]
    os.makedirs(os.path.join(ja.ROOT, "en", "articles"), exist_ok=True)
    write("en/index.html", build_index(titles))
    for a in ARTICLES_EN:
        write(f'en/articles/{a["slug"]}.html', build_article(a))

    # PDF の素は src/print/en-*.html（render.js が en/ に書き出す）
    must = [t for t in titles if t["must"] or t["goal"]]
    old_imp_text = ja.imp_text
    ja.imp_text = imp_text  # 日本語版の印刷テンプレートを英語の重要度表示で使う
    try:
        with open(os.path.join(SRC, "print", "en-must.html"), "w", encoding="utf-8") as f:
            f.write(build_print(must, "① Must-watch titles", f"The {len(must) - 1} titles rated 5 or higher."))
        with open(os.path.join(SRC, "print", "en-all.html"), "w", encoding="utf-8") as f:
            f.write(build_print(titles, "② All titles", f"All {len(titles) - 1} titles, including reference titles such as Tobey Maguire's Spider-Man and Venom."))
    finally:
        ja.imp_text = old_imp_text
    return [("en/", UPDATED)] + [(f'en/articles/{a["slug"]}.html', a["updated"]) for a in ARTICLES_EN]
