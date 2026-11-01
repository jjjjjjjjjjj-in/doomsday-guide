"""作品別キャラクター相関図のページを書き出す（日本語は /characters/、英語は /en/characters/）。build.py の main() から呼ばれる。

データは relations.py。作品を足すと、相関図のページ・一覧・視聴順ガイドからのリンクが自動で増える。
"""
import json
import os
import re
import shutil

from relations import RELATION_MAPS, LINK_TYPES, IMAGES

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

# 今後追加する予定の作品（一覧ページに「準備中」として出す）
PLANNED = [
    ("アベンジャーズ", "The Avengers"), ("キャプテン・アメリカ", "Captain America"), ("マイティ・ソー", "Thor"),
    ("ロキ", "Loki"), ("ファンタスティック・フォー", "The Fantastic Four"), ("X-MEN", "X-Men"),
]

TEXT = {
    "ja": dict(
        menu="キャラクター相関図", aria="キャラクター相関図", actor="俳優", relations="関係のある人物", photo="写真",
        placeholder="顔写真は準備中です（利用許諾を確認できた画像だけを載せます）。",
        hint="ドラッグで移動、ピンチ（PCはホイール）で拡大・縮小。人物をタップすると説明が開きます。",
        fit="全体表示", zoom_in="拡大", zoom_out="縮小", close="閉じる", filter="線の種類（押すと表示・非表示）",
        list="登場人物の一覧", lead_role="中心人物", main_role="主要人物", sub_role="脇役",
        spoiler="※人物の説明には、映画の結末に関わるネタバレを含みます。",
        photo_note="※著作権の関係で、映画の場面写真やポスターなど、映画に出てくる姿の写真は使えません。顔写真はすべて、自由に使ってよい許可のある俳優本人の写真です（見つからなかった人物は頭文字のアイコン）。",
        credits="画像について",
        credits_intro="顔写真は、Wikimedia Commons にある俳優本人の写真（自由に使えるライセンスのもの）を、正方形に切り抜いて縮小し、使っています。写真のない人物は仮のアイコン（名前の頭文字）です。",
        credits_item="{name}／{actor}：撮影 {author}",
        credits_none="この相関図の顔アイコンは、今はすべて仮のアイコン（名前の頭文字）です。俳優の写真や映画の画像は、利用許諾を確認できたものだけを、出典とライセンスを明記して載せます。",
        back="視聴順ガイドでこの作品を見る", index="相関図の一覧", home="ドゥームズデイ予習ガイド",
        index_title="MCU 作品別キャラクター相関図",
        index_desc="MCUの映画ごとに、主人公を中心に登場人物の関係を図にしました。顔アイコンをタップすると、人物の説明が読めます。",
        planned="準備中", open="相関図を見る",
    ),
    "en": dict(
        menu="Character maps", aria="Character relationship map", actor="Actor", relations="Connections", photo="Photo",
        placeholder="Photo coming soon (we only use images whose license we have confirmed).",
        hint="Drag to move, pinch (or scroll on a computer) to zoom. Tap a person to read about them.",
        fit="Fit all", zoom_in="Zoom in", zoom_out="Zoom out", close="Close", filter="Line types (tap to show or hide)",
        list="All characters", lead_role="Center", main_role="Main", sub_role="Supporting",
        spoiler="The character notes contain spoilers, including the ending.",
        photo_note="Because of copyright, we can't use stills, posters or any other images of the characters as they appear in the film. All face photos are freely licensed photos of the actors themselves (people without one are shown with initials).",
        credits="About the images",
        credits_intro="Face photos are freely licensed photos of the actors from Wikimedia Commons, cropped to a square and resized. People without a photo are shown with a placeholder (initials).",
        credits_item="{name} — {actor}: photo by {author}",
        credits_none="All face icons on this map are placeholders (initials) for now. We will only add actor photos or film images whose license we have confirmed, with the source and license shown.",
        back="See this title in the watch guide", index="All character maps", home="Doomsday Watch Guide",
        index_title="MCU Character Relationship Maps",
        index_desc="For each MCU film, a map of who's who, with the hero at the center. Tap a face icon to read about that character.",
        planned="Coming soon", open="Open the map",
    ),
}


def initials(name_en):
    words = re.findall(r"[A-Za-z][A-Za-z.\-]*", re.sub(r'"[^"]*"', "", name_en))
    if len(words) == 1:
        return words[0].replace(".", "")[:1].upper()
    return (words[0][0] + words[-1][0]).upper()


def localized_people(m, lang):
    out = []
    for p in m["people"]:
        g = (lambda k: p.get(f"{k}_en", p[k])) if lang == "en" else (lambda k: p[k])
        name = g("name")
        q = dict(id=p["id"], role=p["role"], side=p["side"], tone=p.get("tone", "gold"), badge=g("badge") if "badge" in p else "",
                 name=name, short=re.sub(r"（.*?）", "", name),
                 actor=g("actor"), group=g("group"), desc=g("desc"), initials=p.get("initials") or initials(p["name_en"]))
        for k in ("x", "y", "ring", "angle"):
            if k in p:
                q[k] = p[k]
        img = IMAGES.get(p["id"])
        if img:
            q["img"] = "{prefix}assets/chars/" + img["file"]
            q["credit"] = {k: img[k] for k in ("author", "license", "license_url", "source_url")}
        out.append(q)
    return out


def page_data(slug, lang, prefix):
    m = RELATION_MAPS[slug]
    t = TEXT[lang]
    people = localized_people(m, lang)
    for p in people:
        if "img" in p:
            p["img"] = p["img"].format(prefix=prefix)
    pick = lambda l, k: (l.get(k + "_en", l.get(k)) if lang == "en" else l.get(k))
    links = [dict(a=l["a"], b=l["b"], type=l["type"], **{k: pick(l, k) for k in ("label", "ab", "ba") if k in l},
                  **{k: l[k] for k in ("bend", "at") if k in l}) for l in m["links"]]
    groups = [dict(x=g["x"], y=g["y"], label=g.get("label_en", g["label"]) if lang == "en" else g["label"]) for g in m.get("groups", [])]
    center = next(p["id"] for p in m["people"] if p["role"] == "lead")
    text = dict(aria=t["aria"], actor=t["actor"], relations=t["relations"], photo=t["photo"], placeholder=t["placeholder"],
                types={k: v[1 if lang == "en" else 0] for k, v in LINK_TYPES.items()})
    return people, dict(center=center, people=people, links=links, groups=groups, text=text)


def map_section(slug, lang, e, prefix):
    """相関図の部分（凡例・図・人物の一覧・画像の出典）。作品ガイドのページに埋め込む"""
    t = TEXT[lang]
    m = RELATION_MAPS[slug]
    people, data = page_data(slug, lang, prefix)
    legend = "".join(f'<button type="button" class="rm-type" data-rm-type="{k}" aria-pressed="true"><i class="rm-swatch t-{k}"></i>{e(v[1 if lang == "en" else 0])}</button>'
                     for k, v in LINK_TYPES.items() if any(l["type"] == k for l in m["links"]))
    role_label = {"lead": t["lead_role"], "main": t["main_role"], "sub": t["sub_role"]}
    roster = "".join(
        f'<li class="r-{p["role"]}"><a href="#relmap" data-rm-open="{p["id"]}">'
        + (f'<img src="{e(p["img"])}" alt="" width="48" height="48">' if p.get("img") else f'<span class="rm-ph-html tone-{p["tone"]} r-{p["role"]}">{e(p["initials"])}</span>')
        + f'<span><b>{e(p["name"])}</b><small>{e(role_label[p["role"]])} ・ {e(p["actor"])}</small><small>{e(p["group"])}</small></span></a></li>'
        for p in sorted(people, key=lambda p: ["lead", "main", "sub"].index(p["role"])))
    used = [(p, IMAGES[p["id"]]) for p in m["people"] if p["id"] in IMAGES]
    def credit_li(p, i):
        g = (lambda k: p.get(f"{k}_en", p[k])) if lang == "en" else (lambda k: p[k])
        text = e(t["credits_item"].format(name=g("name"), actor=g("actor"), author="\0")).split("\0")
        return (f'<li>{text[0]}<a href="{e(i["source_url"])}" target="_blank" rel="noopener">{e(i["author"])}</a>{text[1]}'
                f' / <a href="{e(i["license_url"])}" target="_blank" rel="noopener">{e(i["license"])}</a></li>')
    credits = (f"<p class=\"muted-note\">{e(t['credits_intro'])}</p><ul>" + "".join(credit_li(p, i) for p, i in used) + "</ul>"
               if used else f"<p class=\"muted-note\">{e(t['credits_none'])}</p>")
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    lead = m["lead_en"] if lang == "en" else m["lead"]
    html = f"""<p>{e(lead)}</p>
<p class="muted-note">{e(t["photo_note"])}</p>
<div class="relmap-wrap">
  <div class="rm-legend" role="group" aria-label="{e(t['filter'])}">{legend}</div>
  <div class="relmap" id="relmap">
    <div class="rm-tools">
      <button type="button" id="rm-zoom-in" aria-label="{e(t['zoom_in'])}">＋</button>
      <button type="button" id="rm-zoom-out" aria-label="{e(t['zoom_out'])}">－</button>
      <button type="button" id="rm-fit">{e(t['fit'])}</button>
    </div>
    <aside class="rm-sheet" id="rm-sheet" hidden aria-labelledby="rm-sheet-title">
      <button type="button" class="rm-close" id="rm-close" aria-label="{e(t['close'])}">×</button>
      <div class="rm-sheet-body" id="rm-sheet-body"></div>
    </aside>
  </div>
  <p class="rm-hint">{e(t['hint'])}</p>
</div>
<h3>{e(t['list'])}</h3>
<ul class="rm-roster">{roster}</ul>
<details class="rm-credits"><summary>{e(t['credits'])}</summary>{credits}</details>"""
    scripts = f"""<script type="application/json" id="relmap-data">{data_json}</script>
<script src="{prefix}assets/relmap.js"></script>
"""
    actors = [p["actor"] for p in people if not p["actor"].startswith(("（", "("))]
    return html, scripts, actors


def build_map_page(slug, title, lang, head, footer, e):
    """以前の相関図だけのページ。作品ガイドのページに移ったので、そちらへ案内する"""
    t = TEXT[lang]
    target = f"../films/{slug}.html#map"
    page_title = (f"{title} Character Map | {t['home']}" if lang == "en" else f"『{title}』キャラクター相関図｜{t['home']}")
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(page_title)}</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={e(target)}">
</head><body><p><a href="{e(target)}">{e(page_title)}</a></p></body></html>
"""


def build_index_page(titles_by_slug, lang, head, footer, e):
    t = TEXT[lang]
    prefix = "../../" if lang == "en" else "../"
    path = f"{'en/' if lang == 'en' else ''}characters/"
    cards = "".join(
        f'<li><a class="btn primary" href="../films/{s}.html#map">{e(titles_by_slug[s]["title"])}（{e(titles_by_slug[s]["year"])}）</a></li>' if lang == "ja"
        else f'<li><a class="btn primary" href="../films/{s}.html#map">{e(titles_by_slug[s]["title"])} ({e(titles_by_slug[s]["year"])})</a></li>'
        for s in RELATION_MAPS)
    planned = "".join(f'<li><span class="btn soon" aria-disabled="true">{e(en if lang == "en" else ja)}<small class="rm-soon">{e(t["planned"])}</small></span></li>' for ja, en in PLANNED)
    title = f"{t['index_title']}｜{t['home']}" if lang == "ja" else f"{t['index_title']} | {t['home']}"
    return head(title, t["index_desc"], path, prefix=prefix, lang=lang) + f"""
<nav class="crumb"><a href="../">{e(t['home'])}</a> ＞ {e(t['menu'])}</nav>
<article class="article">
  <h1>{e(t['index_title'])}</h1>
  <p>{e(t['index_desc'])}</p>
</article>
<section class="panel">
  <h2>{e(t['open'])}</h2>
  <ul class="rm-maps">{cards}</ul>
</section>
<section class="panel">
  <h2>{e(t['planned'])}</h2>
  <ul class="rm-maps">{planned}</ul>
</section>
""" + footer + "</body>\n</html>\n"


def copy_assets():
    shutil.copy(os.path.join(SRC, "relmap.js"), os.path.join(ROOT, "assets", "relmap.js"))
    if IMAGES:
        os.makedirs(os.path.join(ROOT, "assets", "chars"), exist_ok=True)
        for img in IMAGES.values():
            shutil.copy(os.path.join(SRC, "chars", img["file"]), os.path.join(ROOT, "assets", "chars", img["file"]))


def write_pages(write, titles_by_slug, lang, head, footer, e):
    """ページを書き出し、サイトマップ用の (パス, 更新日) を返す"""
    base = "en/characters" if lang == "en" else "characters"
    os.makedirs(os.path.join(ROOT, base), exist_ok=True)
    write(f"{base}/index.html", build_index_page(titles_by_slug, lang, head, footer, e))
    pages = [(f"{base}/", max(m["updated"] for m in RELATION_MAPS.values()))]
    for slug, m in RELATION_MAPS.items():
        write(f"{base}/{slug}.html", build_map_page(slug, titles_by_slug[slug]["title"], lang, head, footer, e))
    return pages
