# 作品ガイドは、2026-11-01 から作品ごとの独立したサイトになった（別リポジトリ jjjjjjjjjjj-in.github.io の /<slug>/）。
# このサイトからはリンクを貼るだけ。新しい作品ガイドができたらここに1件足す。
# 以前の /films/<slug>.html と /characters/<slug>.html は、新しいアドレスへ転送するページだけを書き出す。
TOP_URL = "https://mocchima.com/marvel/"  # 作品ガイドの一覧（もっちぃまのトップへは案内しない。運営者の希望、2026-11-02）

GUIDES = {
    # slug: (日本語ページ, 英語ページ)
    "captain-america-first-avenger": ("https://mocchima.com/captain-america-first-avenger/", "https://mocchima.com/captain-america-first-avenger/en/"),
    "captain-marvel": ("https://mocchima.com/captain-marvel/", "https://mocchima.com/captain-marvel/en/"),
    "iron-man": ("https://mocchima.com/iron-man/", "https://mocchima.com/iron-man/en/"),
    "iron-man-2": ("https://mocchima.com/iron-man-2/", "https://mocchima.com/iron-man-2/en/"),
    "incredible-hulk": ("https://mocchima.com/incredible-hulk/", "https://mocchima.com/incredible-hulk/en/"),
    "thor": ("https://mocchima.com/thor/", "https://mocchima.com/thor/en/"),
    "avengers": ("https://mocchima.com/avengers/", "https://mocchima.com/avengers/en/"),
    "thor-dark-world": ("https://mocchima.com/thor-dark-world/", "https://mocchima.com/thor-dark-world/en/"),
    "iron-man-3": ("https://mocchima.com/iron-man-3/", "https://mocchima.com/iron-man-3/en/"),
    "winter-soldier": ("https://mocchima.com/winter-soldier/", "https://mocchima.com/winter-soldier/en/"),
    "guardians-of-the-galaxy": ("https://mocchima.com/guardians-of-the-galaxy/", "https://mocchima.com/guardians-of-the-galaxy/en/"),
    "guardians-vol2": ("https://mocchima.com/guardians-vol2/", "https://mocchima.com/guardians-vol2/en/"),
    "i-am-groot-1": ("https://mocchima.com/i-am-groot-1/", "https://mocchima.com/i-am-groot-1/en/"),
    # シーズン2はシーズン1のガイドにつなぐ（運営者の希望、2026-11-02）
    "i-am-groot-2": ("https://mocchima.com/i-am-groot-1/", "https://mocchima.com/i-am-groot-1/en/"),
    "age-of-ultron": ("https://mocchima.com/age-of-ultron/", "https://mocchima.com/age-of-ultron/en/"),
    "ant-man": ("https://mocchima.com/ant-man/", "https://mocchima.com/ant-man/en/"),
    "civil-war": ("https://mocchima.com/civil-war/", "https://mocchima.com/civil-war/en/"),
    "black-panther": ("https://mocchima.com/black-panther/", "https://mocchima.com/black-panther/en/"),
    "spider-man-homecoming": ("https://mocchima.com/spider-man-homecoming/", "https://mocchima.com/spider-man-homecoming/en/"),
    "doctor-strange": ("https://mocchima.com/doctor-strange/", "https://mocchima.com/doctor-strange/en/"),
    "thor-ragnarok": ("https://mocchima.com/thor-ragnarok/", "https://mocchima.com/thor-ragnarok/en/"),
    "wakanda-forever": ("https://mocchima.com/wakanda-forever/", "https://mocchima.com/wakanda-forever/en/"),
    "ant-man-and-the-wasp": ("https://mocchima.com/ant-man-and-the-wasp/", "https://mocchima.com/ant-man-and-the-wasp/en/"),
    "infinity-war": ("https://mocchima.com/infinity-war/", "https://mocchima.com/infinity-war/en/"),
    "endgame": ("https://mocchima.com/endgame/", "https://mocchima.com/endgame/en/"),
    "loki-s1": ("https://mocchima.com/loki-s1/", "https://mocchima.com/loki-s1/en/"),
    "loki-s2": ("https://mocchima.com/loki-s2/", "https://mocchima.com/loki-s2/en/"),
    "wandavision": ("https://mocchima.com/wandavision/", "https://mocchima.com/wandavision/en/"),
    "shang-chi": ("https://mocchima.com/shang-chi/", "https://mocchima.com/shang-chi/en/"),
    "falcon-and-winter-soldier": ("https://mocchima.com/falcon-and-winter-soldier/", "https://mocchima.com/falcon-and-winter-soldier/en/"),
    "spider-man-far-from-home": ("https://mocchima.com/spider-man-far-from-home/", "https://mocchima.com/spider-man-far-from-home/en/"),
    "spider-man-no-way-home": ("https://mocchima.com/spider-man-no-way-home/", "https://mocchima.com/spider-man-no-way-home/en/"),
    "multiverse-of-madness": ("https://mocchima.com/multiverse-of-madness/", "https://mocchima.com/multiverse-of-madness/en/"),
    "love-and-thunder": ("https://mocchima.com/love-and-thunder/", "https://mocchima.com/love-and-thunder/en/"),
    "quantumania": ("https://mocchima.com/quantumania/", "https://mocchima.com/quantumania/en/"),
    "guardians-vol3": ("https://mocchima.com/guardians-vol3/", "https://mocchima.com/guardians-vol3/en/"),
    "x-men": ("https://mocchima.com/x-men/", "https://mocchima.com/x-men/en/"),
    "x2": ("https://mocchima.com/x2/", "https://mocchima.com/x2/en/"),
    "x-men-last-stand": ("https://mocchima.com/x-men-last-stand/", "https://mocchima.com/x-men-last-stand/en/"),
    "x-men-days-of-future-past": ("https://mocchima.com/x-men-days-of-future-past/", "https://mocchima.com/x-men-days-of-future-past/en/"),
    "x-men-apocalypse": ("https://mocchima.com/x-men-apocalypse/", "https://mocchima.com/x-men-apocalypse/en/"),
    "x-men-dark-phoenix": ("https://mocchima.com/x-men-dark-phoenix/", "https://mocchima.com/x-men-dark-phoenix/en/"),
    "deadpool-and-wolverine": ("https://mocchima.com/deadpool-and-wolverine/", "https://mocchima.com/deadpool-and-wolverine/en/"),
    "agatha-all-along": ("https://mocchima.com/agatha-all-along/", "https://mocchima.com/agatha-all-along/en/"),
    "brave-new-world": ("https://mocchima.com/brave-new-world/", "https://mocchima.com/brave-new-world/en/"),
    "fantastic-four-first-steps": ("https://mocchima.com/fantastic-four-first-steps/", "https://mocchima.com/fantastic-four-first-steps/en/"),
    "thunderbolts": ("https://mocchima.com/thunderbolts/", "https://mocchima.com/thunderbolts/en/"),
    "spider-man-2002": ("https://mocchima.com/spider-man-2002/", "https://mocchima.com/spider-man-2002/en/"),
    "spider-man-2-2004": ("https://mocchima.com/spider-man-2-2004/", "https://mocchima.com/spider-man-2-2004/en/"),
    "spider-man-3-2007": ("https://mocchima.com/spider-man-3-2007/", "https://mocchima.com/spider-man-3-2007/en/"),
    "venom": ("https://mocchima.com/venom/", "https://mocchima.com/venom/en/"),
    "venom-carnage": ("https://mocchima.com/venom-carnage/", "https://mocchima.com/venom-carnage/en/"),
    "venom-last-dance": ("https://mocchima.com/venom-last-dance/", "https://mocchima.com/venom-last-dance/en/"),
    "black-widow": ("https://mocchima.com/black-widow/", "https://mocchima.com/black-widow/en/"),
    "eternals": ("https://mocchima.com/eternals/", "https://mocchima.com/eternals/en/"),
    "hawkeye": ("https://mocchima.com/hawkeye/", "https://mocchima.com/hawkeye/en/"),
    "moon-knight": ("https://mocchima.com/moon-knight/", "https://mocchima.com/moon-knight/en/"),
    "echo": ("https://mocchima.com/echo/", "https://mocchima.com/echo/en/"),
    "she-hulk": ("https://mocchima.com/she-hulk/", "https://mocchima.com/she-hulk/en/"),
    "ms-marvel": ("https://mocchima.com/ms-marvel/", "https://mocchima.com/ms-marvel/en/"),
    "werewolf-by-night": ("https://mocchima.com/werewolf-by-night/", "https://mocchima.com/werewolf-by-night/en/"),
    "guardians-holiday-special": ("https://mocchima.com/guardians-holiday-special/", "https://mocchima.com/guardians-holiday-special/en/"),
    "secret-invasion": ("https://mocchima.com/secret-invasion/", "https://mocchima.com/secret-invasion/en/"),
    "the-marvels": ("https://mocchima.com/the-marvels/", "https://mocchima.com/the-marvels/en/"),
    "logan": ("https://mocchima.com/logan/", "https://mocchima.com/logan/en/"),
    "daredevil-born-again-s1": ("https://mocchima.com/daredevil-born-again-s1/", "https://mocchima.com/daredevil-born-again-s1/en/"),
    "ironheart": ("https://mocchima.com/ironheart/", "https://mocchima.com/ironheart/en/"),
    "visionquest": ("https://mocchima.com/visionquest/", "https://mocchima.com/visionquest/en/"),
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

# くわしいあらすじページ（/<slug>/story/）がない作品。アイ・アム・グルートは短編なので作っていない。
NO_STORY = {"i-am-groot-1", "i-am-groot-2"}
