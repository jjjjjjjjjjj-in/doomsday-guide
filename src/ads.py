# 広告の設定。ここに値を入れて build.py を実行すると、サイト全体に自動で反映される。
# どれか1つでも入っていれば、ページ下に「PR」表記が自動で出る。

# Disney+ の広告リンク（ASPで発行されたURL）。Disney+で配信されている作品すべてに「Disney+で観る」ボタンが出る
DISNEY_PLUS = ""

# Amazonアソシエイトのトラッキングタグ（例: "yourname-22"）。全作品に「Amazonで探す」ボタンが出る
AMAZON_TAG = ""

# ASPのバナー広告コード（HTMLをそのまま貼る）。top=進み具合の下、middle=リストの上、bottom=ページの最後
BANNERS = {"top": "", "middle": "", "bottom": ""}

# Google AdSense のサイト運営者ID（例: "ca-pub-1234567890"）。独自ドメインが必要
ADSENSE_CLIENT = ""

# Disney+（日本）で通常配信されていない作品（ソニー系のスパイダーマン・ヴェノム関連）
NOT_ON_DISNEY_PLUS = {
    "spider-man-homecoming", "spider-man-far-from-home", "spider-man-no-way-home", "spider-man-brand-new-day",
    "venom", "venom-carnage", "venom-last-dance",
    "spider-man-2002", "spider-man-2-2004", "spider-man-3-2007",
    "avengers-doomsday",
}


def enabled():
    return bool(DISNEY_PLUS or AMAZON_TAG or ADSENSE_CLIENT or any(BANNERS.values()))
