# 広告の設定。ここに値を入れて build.py を実行すると、サイト全体に自動で反映される。
# どれか1つでも入っていれば、ページ下に「PR」表記が自動で出る。

# Disney+ の広告リンク（ASPで発行されたURL）。Disney+で配信されている作品すべてに「Disney+で観る」ボタンが出る
DISNEY_PLUS = ""

# Amazonアソシエイトのトラッキングタグ（例: "yourname-22"）。全作品に「Amazonで探す」ボタンが出る
AMAZON_TAG = "doomsdayguide-22"

# ASPのバナー広告コード（HTMLをそのまま貼る）。top=進み具合の下、middle=リストの上、bottom=ページの最後
BANNERS = {"top": "", "middle": "", "bottom": ""}

# Google AdSense のサイト運営者ID（例: "ca-pub-1234567890"）。独自ドメインが必要
ADSENSE_CLIENT = ""

# 「予習のおとも」に並べるAmazonの商品（表示名, 検索キーワード）。検索キーワードの代わりに "/gp/..." のパスも使える
# Amazonは、リンクから24時間以内に買われた商品なら、紹介した商品以外でも報酬の対象になる
AMAZON_PICKS = [
    ("Fire TV Stick（Disney+をテレビの大画面で）", "Fire TV Stick"),
    ("マーベルのレゴ", "レゴ マーベル"),
    ("マーベルのTシャツ", "マーベル Tシャツ"),
    ("アベンジャーズのフィギュア", "アベンジャーズ フィギュア"),
    ("マーベルのマグカップ・雑貨", "マーベル グッズ"),
    ("家で映画館気分：ポップコーン", "ポップコーン"),
    ("アメコミ（日本語版）", "マーベル アメコミ 邦訳"),
    ("Amazonタイムセール", "/gp/goldbox"),
    ("Amazon売れ筋ランキング", "/gp/bestsellers"),
]

# 記事の途中に出す関連アイテム（記事slug: [(表示名, 検索キーワード)]）
ARTICLE_PICKS = {
    "cast": [("アベンジャーズのフィギュア", "アベンジャーズ フィギュア"), ("ドクター・ドゥームのグッズ", "ドクター・ドゥーム")],
    "x-men": [("X-MENのフィギュア", "X-MEN フィギュア"), ("X-MEN 旧3部作のBlu-ray", "X-MEN ブルーレイ")],
    "infinity-saga": [("インフィニティ・ガントレットのグッズ", "インフィニティ ガントレット"), ("マーベルのレゴ", "レゴ マーベル")],
    "next-generation": [("キャプテン・アメリカの盾グッズ", "キャプテンアメリカ 盾"), ("ブラックパンサーのグッズ", "ブラックパンサー グッズ")],
    "multiverse": [("ロキのグッズ", "ロキ マーベル グッズ"), ("デッドプールのグッズ", "デッドプール グッズ")],
}

# 画面下に固定する小さなバー（表示名, 検索キーワードまたは "/gp/..."）。空文字なら出さない
STICKY_BAR = ("今日のAmazonタイムセールを見る", "/gp/goldbox")

# Disney+（日本）で通常配信されていない作品（ソニー系のスパイダーマン・ヴェノム関連）
NOT_ON_DISNEY_PLUS = {
    "spider-man-homecoming", "spider-man-far-from-home", "spider-man-no-way-home", "spider-man-brand-new-day",
    "venom", "venom-carnage", "venom-last-dance",
    "spider-man-2002", "spider-man-2-2004", "spider-man-3-2007",
    "avengers-doomsday",
}


def enabled():
    return bool(DISNEY_PLUS or AMAZON_TAG or ADSENSE_CLIENT or any(BANNERS.values()))
