"""作品ガイドのページ（/films/<slug>.html と /en/films/<slug>.html）を書き出す。build.py と build_en.py から呼ばれる。

1ページで「3行まとめ・観る前に・相関図・あらすじ・用語集・分かりにくいQ&A・小ネタ・おまけ映像・次に観る作品」が分かる。
データは films.py（文章）と relations.py（相関図）。
"""
import os

import ads
from films import FILM_GUIDES
from relations import RELATION_MAPS
import relmap_build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEXT = {
    "ja": dict(
        brand="MCU作品ガイド", menu="作品ガイド", guide="完全ガイド",
        tagline="映画だけでは分かりにくいところを、あらすじ・相関図・用語でやさしく解説します。",
        year="公開", runtime="上映時間", order="視聴順", imp="重要度", era="作中の時代",
        toc="このページの内容", s_summary="この作品を3行で", s_before="観る前に知っておくと分かりやすいこと", s_map="キャラクター相関図",
        s_story="あらすじ", s_glossary="用語集", s_confusing="ここが分かりにくい！Q&A", s_points="見逃しやすいポイント・小ネタ",
        s_ending="ラストとおまけ映像", s_dd="ドゥームズデイとのつながり", s_next="次に観るとよい作品",
        nospoil="ネタバレなし", spoil="ネタバレあり",
        story_open="あらすじを読む（結末までのネタバレを含みます）",
        confusing_note="結末に関わる内容を含みます。",
        post="エンドクレジットの後のおまけ映像",
        watched="この作品を観た（視聴順ガイドのチェックと共通）",
        shop="この作品をもっと楽しむ", back="視聴順ガイドに戻る", list="作品ガイドの一覧",
        trailer="公式予告編を見る（YouTube）", order_fmt="{:02d}番目",
        desc_fmt="『{title}』を映画だけでは分かりにくい人向けに解説。ネタバレなしの観る前のポイント、顔アイコンつき相関図、章ごとのあらすじ、用語集、分かりにくい場面のQ&A、おまけ映像まで。",
        title_fmt="『{title}』完全ガイド｜あらすじ・相関図・用語をやさしく解説",
        index_title="MCU作品ガイド", index_desc="映画だけではすんなり理解しづらい人のために、作品ごとにあらすじ・相関図・用語・分かりにくい場面をまとめています。",
        planned="準備中",
    ),
    "en": dict(
        brand="MCU Film Guides", menu="Film guides", guide="Complete Guide",
        tagline="The parts that are hard to follow from the film alone, explained with a story summary, a character map and key terms.",
        year="Released", runtime="Runtime", order="Watch order", imp="Importance", era="Set in",
        toc="On this page", s_summary="The film in three lines", s_before="Good to know before watching", s_map="Character map",
        s_story="Story", s_glossary="Key terms", s_confusing="Confusing parts, explained", s_points="Easy-to-miss details",
        s_ending="The ending and post-credits", s_dd="The Doomsday connection", s_next="What to watch next",
        nospoil="No spoilers", spoil="Spoilers",
        story_open="Read the story (spoilers up to the ending)",
        confusing_note="Contains spoilers about the ending.",
        post="After the end credits",
        watched="I've watched this (shared with the watch guide checklist)",
        shop="More from this film", back="Back to the watch guide", list="All film guides",
        trailer="Watch the official trailer (YouTube)", order_fmt="No. {:02d}",
        desc_fmt="A guide to {title} for anyone who finds it hard to follow: spoiler-free tips, a character map with face icons, a chapter-by-chapter story, key terms, the confusing parts explained, and the post-credits scene.",
        title_fmt="{title} Complete Guide: Story, Character Map and Key Terms Explained",
        index_title="MCU Film Guides", index_desc="For anyone who finds the films hard to follow: the story, a character map, key terms and the confusing parts, film by film.",
        planned="Coming soon",
    ),
}


PRIVACY_URL = "https://jjjjjjjjjjj-in.github.io/privacy.html"


def film_footer(lang, e):
    """作品ガイド専用のフッター（ドゥームズデイ予習ガイドとは別のページとして見せる）"""
    if lang == "en":
        disc = '<p>This site contains affiliate links (ads).</p>\n' if ads.enabled() else ""
        if ads.AMAZON_TAG or getattr(ads, "AMAZON_TAG_US", ""):
            disc += '<p>As an Amazon Associate, this site earns from qualifying purchases.</p>\n'
        return f"""<footer>
{disc}<p>For how this site uses analytics (Google Analytics) and ads, see the <a href="{PRIVACY_URL}#en">privacy policy</a>.</p>
<p>This is an unofficial fan site run by an individual. It is not affiliated with Marvel Studios, The Walt Disney Company, Sony Pictures or 20th Century Studios. Titles and character names are trademarks of their respective owners.</p>
<p><a href="./">MCU Film Guides</a></p>
</footer>
</div>
"""
    disc = '<p>※当サイトはアフィリエイト広告（PR）を利用しています。</p>\n' if ads.enabled() else ""
    if ads.AMAZON_TAG:
        disc += '<p>Amazonのアソシエイトとして、当サイトは適格販売により収入を得ています。</p>\n'
    return f"""<footer>
{disc}<p>アクセス解析（Googleアナリティクス）と広告の仕組みについては<a href="{PRIVACY_URL}">プライバシーポリシー</a>をご覧ください。</p>
<p>当サイトは個人が運営する非公式ファンサイトです。Marvel Studios、The Walt Disney Company、Sony Pictures、20th Century Studios とは関係ありません。作品名・キャラクター名は各権利者の商標です。</p>
<p><a href="./">MCU作品ガイド</a></p>
</footer>
</div>
"""


def L(item, lang, i_ja, i_en):
    return item[i_en] if lang == "en" else item[i_ja]


def shop_panel(g, lang, e, shop_url_fn, rakuten_fn):
    """作品に関連する商品（PR）。Amazon と、日本語版は楽天も"""
    if not ads.AMAZON_TAG:
        return ""
    t = TEXT[lang]
    btns = []
    for label, kw, label_en in g.get("shop", []):
        btns.append(f'<a class="btn ad" href="{e(shop_url_fn(kw if lang == "ja" else label_en))}" target="_blank" rel="sponsored noopener">{e(label_en if lang == "en" else label)}</a>')
        if lang == "ja" and ads.RAKUTEN_TOP:
            btns.append(f'<a class="btn ad" href="{e(rakuten_fn(kw))}" target="_blank" rel="sponsored noopener">{e(label)}（楽天）</a>')
    return f'<aside class="panel"><h2>{e(t["shop"])} <span class="pr">PR</span></h2><div class="btns">{"".join(btns)}</div></aside>'


def build_page(slug, title_rec, titles, lang, head, footer, e, shop_url_fn, rakuten_fn, imp_text, trailer_html):
    t = TEXT[lang]
    g = FILM_GUIDES[slug]
    prefix = "../../" if lang == "en" else "../"
    tr = title_rec
    title = tr["title"]
    path = f"{'en/' if lang == 'en' else ''}films/{slug}.html"
    h1 = f"{title}" if lang == "en" else f"『{title}』"

    summary = "".join(f"<li>{e(x)}</li>" for x in (g["summary_en"] if lang == "en" else g["summary"]))
    before = "".join(f'<div class="fg-card"><h3>{e(h)}</h3><p>{e(b)}</p></div>' for h, b in (g["before_en"] if lang == "en" else g["before"]))
    glossary = "".join(f"<div><dt>{e(L(x, lang, 0, 2))}</dt><dd>{e(L(x, lang, 1, 3))}</dd></div>" for x in g["glossary"])
    story = "".join(f'<section class="fg-chapter"><h3>{e(L(x, lang, 0, 2))}</h3><p>{e(L(x, lang, 1, 3))}</p></section>' for x in g["story"])
    confusing = "".join(f'<details class="fg-qa"><summary>{e(L(x, lang, 0, 2))}</summary><p>{e(L(x, lang, 1, 3))}</p></details>' for x in g["confusing"])
    points = "".join(f'<div class="fg-card"><h3>{e(L(x, lang, 0, 2))}</h3><p>{e(L(x, lang, 1, 3))}</p></div>' for x in g["points"])
    by_slug = {x["slug"]: x for x in titles}
    nexts = "".join(
        (f'<li><a href="{s}.html">' if s in FILM_GUIDES else '<li><div class="fg-next-item">')
        + f'<b>{e(by_slug[s]["title"])}</b><small>{e(why_en if lang == "en" else why)}</small>'
        + ('</a></li>' if s in FILM_GUIDES else '</div></li>')
        for s, why, why_en in g["next"] if s in by_slug)

    has_map = slug in RELATION_MAPS
    map_html, map_scripts, actors = relmap_build.map_section(slug, lang, e, prefix) if has_map else ("", "", [])
    sections = [("before", t["s_before"])] + ([("map", t["s_map"])] if has_map else []) + [
        ("story", t["s_story"]), ("glossary", t["s_glossary"]), ("confusing", t["s_confusing"]), ("points", t["s_points"]),
        ("ending", t["s_ending"]), ("next", t["s_next"])]
    toc = "".join(f'<a class="chip" href="#{k}">{e(v)}</a>' for k, v in sections)
    facts = [(t["year"], tr["year"]), (t["runtime"], g["runtime_en"] if lang == "en" else g["runtime"]),
             (t["era"], tr["era"])]
    facts_html = "".join(f"<div><dt>{e(k)}</dt><dd>{e(str(v))}</dd></div>" for k, v in facts)
    shop = shop_panel(g, lang, e, shop_url_fn, rakuten_fn)

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": t["title_fmt"].format(title=title), "description": t["desc_fmt"].format(title=title),
             "inLanguage": lang, "dateModified": g["updated"], "datePublished": g["updated"],
             "about": {"@type": "Movie", "name": title, "datePublished": tr["year"], "actor": [{"@type": "Person", "name": a} for a in actors[:6]]}},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": L(x, lang, 0, 2),
                                                 "acceptedAnswer": {"@type": "Answer", "text": L(x, lang, 1, 3)}} for x in g["confusing"]]},
        ],
    }
    watched_script = """<script>
(function(){var K="doomsday-watched-v2",b=document.getElementById("fg-watched");if(!b)return;var s=[];
try{s=JSON.parse(localStorage.getItem(K)||"[]")}catch(e){}b.checked=s.indexOf(b.dataset.slug)>=0;
b.addEventListener("change",function(){var i=s.indexOf(b.dataset.slug);if(b.checked&&i<0)s.push(b.dataset.slug);if(!b.checked&&i>=0)s.splice(i,1);
try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}});})();
</script>
"""
    th = g.get("theme")
    theme_css = (f"<style>:root{{--green:{th['deep']};--navy:{th['main']};--gold-bright:{th['accent']};--green-soft:{th['soft']};"
                 f"--navy-soft:{th['soft']};--gold:{th['accent']};--gold-ink:{th['main']};--link:{th['main']};}}</style>\n") if th else ""
    og = f"{'en/' if lang == 'en' else ''}films/og/{slug}.png"
    return head(t["title_fmt"].format(title=title), t["desc_fmt"].format(title=title), path, prefix=prefix, schema=schema, lang=lang,
                og_image=og, site_name=t["brand"]) + theme_css + f"""
<nav class="crumb"><a href="./">{e(t['brand'])}</a> ＞ {e(title)}</nav>
<header class="fg-hero">
  <p class="eyebrow">{e(t['menu'])} · {e(tr['year'])}</p>
  <h1>{e(h1)}<small>{e(t['guide'])}</small></h1>
  <p class="lead">{e(t['tagline'])}</p>
  <dl class="fg-facts">{facts_html}</dl>
  {trailer_html}
</header>
<nav class="fg-toc" aria-label="{e(t['toc'])}">{toc}</nav>

<section class="fg-sec" id="before"><h2>{e(t['s_before'])}<span class="tag-ok">{e(t['nospoil'])}</span></h2>
  <div class="fg-cards">{before}</div>
</section>
""" + (f"""
<section class="fg-sec" id="map"><h2>{e(t['s_map'])}<span class="tag-warn">{e(t['spoil'])}</span></h2>
  {map_html}
</section>
""" if has_map else "") + f"""
<section class="fg-sec" id="story"><h2>{e(t['s_story'])}<span class="tag-warn">{e(t['spoil'])}</span></h2>
  <details class="fg-spoiler"><summary>{e(t['story_open'])}</summary>{story}</details>
</section>

{shop}

<section class="fg-sec" id="glossary"><h2>{e(t['s_glossary'])}</h2>
  <dl class="fg-glossary">{glossary}</dl>
</section>

<section class="fg-sec" id="confusing"><h2>{e(t['s_confusing'])}<span class="tag-warn">{e(t['spoil'])}</span></h2>
  <p class="fg-note">{e(t['confusing_note'])}</p>
  {confusing}
</section>

<section class="fg-sec" id="points"><h2>{e(t['s_points'])}</h2>
  <div class="fg-cards">{points}</div>
</section>

<section class="fg-sec" id="ending"><h2>{e(t['s_ending'])}<span class="tag-warn">{e(t['spoil'])}</span></h2>
  <details class="fg-spoiler"><summary>{e(t['post'])}</summary><p>{e(tr['post'])}</p></details>
</section>

<section class="fg-sec" id="next"><h2>{e(t['s_next'])}</h2>
  <ul class="fg-next">{nexts}</ul>
</section>

<section class="panel">
  <div class="btns"><a class="btn primary" href="./">{e(t['list'])}</a></div>
</section>
{map_scripts}""" + film_footer(lang, e) + "</body>\n</html>\n"


def build_index(titles, lang, head, footer, e):
    t = TEXT[lang]
    prefix = "../../" if lang == "en" else "../"
    path = f"{'en/' if lang == 'en' else ''}films/"
    by_slug = {x["slug"]: x for x in titles}
    cards = "".join(f'<li><a class="btn primary" href="{s}.html">{e(by_slug[s]["title"])} ({e(by_slug[s]["year"])})</a></li>' for s in FILM_GUIDES)
    planned = "".join(f'<li><span class="btn soon" aria-disabled="true">{e(en if lang == "en" else ja)}<small class="rm-soon">{e(t["planned"])}</small></span></li>'
                      for ja, en in relmap_build.PLANNED)
    title = t["index_title"]
    return head(title, t["index_desc"], path, prefix=prefix, lang=lang, site_name=t["brand"],
                og_image=f"{'en/' if lang == 'en' else ''}films/og/index.png") + f"""
<nav class="crumb">{e(t['brand'])}</nav>
<article class="article">
  <h1>{e(t['index_title'])}</h1>
  <p>{e(t['index_desc'])}</p>
</article>
<section class="panel"><h2>{e(t['menu'])}</h2><ul class="rm-maps">{cards}</ul></section>
<section class="panel"><h2>{e(t['planned'])}</h2><ul class="rm-maps">{planned}</ul></section>
""" + film_footer(lang, e) + "</body>\n</html>\n"


def write_pages(write, titles, lang, head, footer, e, shop_url_fn, rakuten_fn, imp_text, trailer_fn):
    base = "en/films" if lang == "en" else "films"
    os.makedirs(os.path.join(ROOT, base), exist_ok=True)
    write(f"{base}/index.html", build_index(titles, lang, head, footer, e))
    by_slug = {x["slug"]: x for x in titles}
    pages = [(f"{base}/", max(g["updated"] for g in FILM_GUIDES.values()))]
    # 共有用の画像（films/og/<slug>.png）を render.js で作るためのデータ
    import json
    og = [dict(slug=slug, lang=lang, title=by_slug[slug]["title"], year=by_slug[slug]["year"], theme=g.get("theme") or {},
               out=f"{base}/og/{slug}.png") for slug, g in FILM_GUIDES.items()]
    og.append(dict(slug="index", lang=lang, index=True, title=TEXT[lang]["brand"], year="", theme={}, out=f"{base}/og/index.png"))
    with open(os.path.join(ROOT, "src", "print", f"og-films-{lang}.json"), "w", encoding="utf-8") as f:
        json.dump(og, f, ensure_ascii=False, indent=1)
    for slug, g in FILM_GUIDES.items():
        write(f"{base}/{slug}.html", build_page(slug, by_slug[slug], titles, lang, head, footer, e, shop_url_fn, rakuten_fn, imp_text, trailer_fn(by_slug[slug])))
        pages.append((f"{base}/{slug}.html", g["updated"]))
    return pages
