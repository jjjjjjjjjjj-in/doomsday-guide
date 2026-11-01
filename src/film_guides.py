# 作品ガイドは、2026-11-01 から作品ごとの独立したサイトになった（別リポジトリ jjjjjjjjjjj-in.github.io の /<slug>/）。
# このサイトからはリンクを貼るだけ。新しい作品ガイドができたらここに1件足す。
# 以前の /films/<slug>.html と /characters/<slug>.html は、新しいアドレスへ転送するページだけを書き出す。
TOP_URL = "https://jjjjjjjjjjj-in.github.io/"

GUIDES = {
    # slug: (日本語ページ, 英語ページ)
    "captain-america-first-avenger": ("https://jjjjjjjjjjj-in.github.io/captain-america-first-avenger/", "https://jjjjjjjjjjj-in.github.io/captain-america-first-avenger/en/"),
    "captain-marvel": ("https://jjjjjjjjjjj-in.github.io/captain-marvel/", "https://jjjjjjjjjjj-in.github.io/captain-marvel/en/"),
    "iron-man": ("https://jjjjjjjjjjj-in.github.io/iron-man/", "https://jjjjjjjjjjj-in.github.io/iron-man/en/"),
}


def redirect_page(target, title, lang="ja"):
    import html
    e = html.escape
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{e(target)}">
<meta http-equiv="refresh" content="0; url={e(target)}">
</head><body><p><a href="{e(target)}">{e(title)}</a></p></body></html>
"""


def write_redirects(write, lang):
    """古いアドレスを新しいサイトへ転送する（サイトマップには入れない）"""
    base = "en/" if lang == "en" else ""
    i = 1 if lang == "en" else 0
    for slug, urls in GUIDES.items():
        write(f"{base}films/{slug}.html", redirect_page(urls[i], urls[i], lang))
        write(f"{base}characters/{slug}.html", redirect_page(urls[i] + "#map", urls[i], lang))
    write(f"{base}films/index.html", redirect_page(TOP_URL, TOP_URL, lang))
    write(f"{base}characters/index.html", redirect_page(TOP_URL, TOP_URL, lang))
