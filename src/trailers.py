# 予告編へのリンク。
# TRAILERS: 公式チャンネルが公開していて、作品と一致することを確認できた動画だけを登録する（作品slug: (URL, チャンネル名)）。
#   今の作業環境からは YouTube に接続できず確認できないため、空のまま。
# TRAILER_SEARCH: 動画を確認できない作品は、公式チャンネルの中を作品名で検索するページへのリンクにする。
#   推測した動画URLは使わない。動画やサムネイルは埋め込まず、普通の外部リンクにする。
from urllib.parse import quote

TRAILERS = {}

CHANNELS = {
    "marvel": ("Marvel Entertainment 公式チャンネル", "https://www.youtube.com/@marvel"),
    "sony": ("Sony Pictures Entertainment 公式チャンネル", "https://www.youtube.com/@SonyPictures"),
    "fox": ("20th Century Studios 公式チャンネル", "https://www.youtube.com/@20thCenturyStudios"),
}

# 作品slug: (チャンネル, 検索する英語タイトル)
TRAILER_SEARCH = {
    "captain-america-first-avenger": ("marvel", "Captain America: The First Avenger trailer"),
    "captain-marvel": ("marvel", "Captain Marvel trailer"),
    "iron-man": ("marvel", "Iron Man trailer"),
    "iron-man-2": ("marvel", "Iron Man 2 trailer"),
    "incredible-hulk": ("marvel", "The Incredible Hulk trailer"),
    "thor": ("marvel", "Thor trailer"),
    "avengers": ("marvel", "The Avengers trailer"),
    "thor-dark-world": ("marvel", "Thor: The Dark World trailer"),
    "iron-man-3": ("marvel", "Iron Man 3 trailer"),
    "winter-soldier": ("marvel", "Captain America: The Winter Soldier trailer"),
    "guardians-of-the-galaxy": ("marvel", "Guardians of the Galaxy trailer"),
    "guardians-vol2": ("marvel", "Guardians of the Galaxy Vol. 2 trailer"),
    "i-am-groot-1": ("marvel", "I Am Groot trailer"),
    "i-am-groot-2": ("marvel", "I Am Groot Season 2 trailer"),
    "age-of-ultron": ("marvel", "Avengers: Age of Ultron trailer"),
    "ant-man": ("marvel", "Ant-Man trailer"),
    "civil-war": ("marvel", "Captain America: Civil War trailer"),
    "black-widow": ("marvel", "Black Widow trailer"),
    "black-panther": ("marvel", "Black Panther trailer"),
    "spider-man-homecoming": ("sony", "Spider-Man: Homecoming trailer"),
    "doctor-strange": ("marvel", "Doctor Strange trailer"),
    "thor-ragnarok": ("marvel", "Thor: Ragnarok trailer"),
    "ant-man-and-the-wasp": ("marvel", "Ant-Man and the Wasp trailer"),
    "infinity-war": ("marvel", "Avengers: Infinity War trailer"),
    "endgame": ("marvel", "Avengers: Endgame trailer"),
    "loki-s1": ("marvel", "Loki trailer"),
    "loki-s2": ("marvel", "Loki Season 2 trailer"),
    "wandavision": ("marvel", "WandaVision trailer"),
    "shang-chi": ("marvel", "Shang-Chi and the Legend of the Ten Rings trailer"),
    "falcon-and-winter-soldier": ("marvel", "The Falcon and the Winter Soldier trailer"),
    "spider-man-far-from-home": ("sony", "Spider-Man: Far From Home trailer"),
    "venom": ("sony", "Venom trailer"),
    "venom-carnage": ("sony", "Venom: Let There Be Carnage trailer"),
    "spider-man-no-way-home": ("sony", "Spider-Man: No Way Home trailer"),
    "eternals": ("marvel", "Eternals trailer"),
    "multiverse-of-madness": ("marvel", "Doctor Strange in the Multiverse of Madness trailer"),
    "hawkeye": ("marvel", "Hawkeye trailer"),
    "moon-knight": ("marvel", "Moon Knight trailer"),
    "wakanda-forever": ("marvel", "Black Panther: Wakanda Forever trailer"),
    "echo": ("marvel", "Echo trailer"),
    "she-hulk": ("marvel", "She-Hulk: Attorney at Law trailer"),
    "ms-marvel": ("marvel", "Ms. Marvel trailer"),
    "love-and-thunder": ("marvel", "Thor: Love and Thunder trailer"),
    "werewolf-by-night": ("marvel", "Werewolf by Night trailer"),
    "guardians-holiday-special": ("marvel", "The Guardians of the Galaxy Holiday Special trailer"),
    "quantumania": ("marvel", "Ant-Man and the Wasp: Quantumania trailer"),
    "guardians-vol3": ("marvel", "Guardians of the Galaxy Vol. 3 trailer"),
    "secret-invasion": ("marvel", "Secret Invasion trailer"),
    "the-marvels": ("marvel", "The Marvels trailer"),
    "venom-last-dance": ("sony", "Venom: The Last Dance trailer"),
    "x-men": ("fox", "X-Men 2000 trailer"),
    "x2": ("fox", "X2 X-Men United trailer"),
    "x-men-last-stand": ("fox", "X-Men: The Last Stand trailer"),
    "x-men-days-of-future-past": ("fox", "X-Men: Days of Future Past trailer"),
    "logan": ("fox", "Logan trailer"),
    "deadpool-and-wolverine": ("marvel", "Deadpool & Wolverine trailer"),
    "agatha-all-along": ("marvel", "Agatha All Along trailer"),
    "daredevil-born-again-s1": ("marvel", "Daredevil: Born Again trailer"),
    "brave-new-world": ("marvel", "Captain America: Brave New World trailer"),
    "fantastic-four-first-steps": ("marvel", "The Fantastic Four: First Steps trailer"),
    "thunderbolts": ("marvel", "Thunderbolts* trailer"),
    "ironheart": ("marvel", "Ironheart trailer"),
    "spider-man-brand-new-day": ("sony", "Spider-Man: Brand New Day trailer"),
    "visionquest": ("marvel", "VisionQuest trailer"),
    "spider-man-2002": ("sony", "Spider-Man 2002 trailer"),
    "spider-man-2-2004": ("sony", "Spider-Man 2 2004 trailer"),
    "spider-man-3-2007": ("sony", "Spider-Man 3 trailer"),
    "avengers-doomsday": ("marvel", "Avengers: Doomsday trailer"),
}


def search_link(slug):
    """公式チャンネル内の検索ページ (URL, チャンネル名)。登録がなければ None"""
    entry = TRAILER_SEARCH.get(slug)
    if not entry:
        return None
    name, base = CHANNELS[entry[0]]
    return f"{base}/search?query={quote(entry[1])}", name
