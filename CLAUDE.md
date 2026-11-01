# ドゥームズデイ予習ガイド

『アベンジャーズ／ドゥームズデイ』（2026年12月18日 日米同時公開）の予習用の非公式ファンサイト。GitHub Pages（main ブランチのルート）で公開: https://jjjjjjjjjjj-in.github.io/doomsday-guide/

運営者は日本語で、技術に詳しくない。返答は日本語で、短く、専門用語を避ける。

## ビルド
- 生成物（index.html, articles/, assets/, PDF, og.png, sitemap.xml, robots.txt）は手で編集しない。`src/` を編集してから次を実行する:
  - `python3 src/build.py`
  - `node src/render.js`（PDF 2種と og.png。Playwright と IPAGothic フォントを使う）
- コミット作成者は Claude <noreply@anthropic.com>。

## src の中身
- `titles_a.py` / `titles_b.py` / `titles_c.py`: 全70作品（視聴順）。あらすじ・関連性・ポストクレジットなど。
- `importance.py`: 10点満点の重要度。5以上が「① 必ず観るべき」。点数は運営者が決める。勝手に変えない。
- `articles.py`: 解説記事5本。
- `ads.py`: 広告設定（Amazon タグ doomsdayguide-22、英語版の amazon.com タグ doomsdaygui08-20、もしも経由の楽天 a_id=5875908 など）。「PR」表記とAmazonの表記は自動で出る。`FEATURED` は「予習のおとも」の一番上に枠付きで出すおすすめ商品（今はマーベル公式の年表の本。オープンチャットで欲しい人が多かった、2026-11-02）。誤クリックを誘う広告は入れない。
- `trailers.py`: 予告編リンク。
- `film_guides.py`: 作品ガイドへのリンク先。作品ガイド（あらすじ・相関図・用語）は 2026-11-01 から作品ごとの独立したサイトになり、別リポジトリ jjjjjjjjjjj-in.github.io の /<slug>/ に移した（運営者の希望で、ドゥームズデイとは別に考える）。このサイトはリンクを貼るだけ。作り方・ルール（顔写真・相関図・文章）はそちらの CLAUDE.md と src/mcu/ を見る。新しい作品ガイドができたら GUIDES に1件足す。以前の /films/・/characters/ のページは新しいアドレスへの転送だけを書き出す（サイトマップには入れない）。
- トップと記事のページには、上に「目次」の帯（`build.py` の site_toc。押すとその場所・ページへ飛ぶ。スクロールしても上に残る）を出す。トップの「作品ガイド」欄は押すと開く形（運営者の希望、2026-11-02）。
- `build.py` の `GOOGLE_SITE_VERIFICATION`: Google Search Console の確認コード。`GA_MEASUREMENT_ID`: Google アナリティクス（全サイト共通 G-KDFL8GPPRZ）。フッターから共通のプライバシーポリシー（https://jjjjjjjjjjj-in.github.io/privacy.html）にリンクする。
- `site.css` / `app.js` / `sticky.js`: 見た目と動き。白背景、タイトルは濃いグリーン、見出しは紺。
- 英語版の広告は `ads.py` の `AMAZON_TAG_US`（アメリカのAmazonアソシエイト）を入れると amazon.com に切り替わる。
- 英語版は /en/ に出力する。`build_en.py` が `src/en/`（`titles_en_*.py` の作品の英文、`articles_en.py` の記事）を使い、並び・重要度・予告編・広告は日本語版と共通。日本語の作品や記事を直したら、英語版の同じ項目も合わせて直す。

## 時系列（視聴順）の参考
運営者は、ロキ シーズン2までの時系列が書かれたマーベル・スタジオ公式の年表の本（The Marvel Cinematic Universe: An Official Timeline）を基本の参考にしている。運営者から聞いた本の順番（2026-11-02）: アントマン → ドクター・ストレンジ（事故より前）→ シビル・ウォー／ストレンジの修行 → ストレンジの最後の戦い → ブラック・ウィドウ → ブラックパンサー → ホームカミング。視聴順ではストレンジを最後の戦いの時期に合わせ、シビル・ウォーの次に置いた。並びを直すときは、作品ガイド（別リポジトリ）の WATCH_ORDER と「次に観る作品」の文も合わせて直す。

## キャスト情報のルール
公式発表と噂を必ず分ける。運営者自身の予想は「【運営者の予想】」と明記する（例: 旧X-MENは『アポカリプス』『ダーク・フェニックス』の世界から来るという予想）。ヒュー・ジャックマン、トビー・マグワイアは2026-10-31時点で噂の段階。

## 公式予告編のリンク（2026-10-31 に61作品を確認・登録済み）
未確認: アイアンマン、アイアンマン2、インクレディブル・ハルク、X-MEN（2000）、X-MEN：ファイナル ディシジョン、X-MEN：フューチャー&パスト、スパイダーマン2（2004）、X-MEN：アポカリプス、X-MEN：ダーク・フェニックス（2作は後から追加。未確認）。公式チャンネルで予告編が見つからなかった。追加するときも次の手順を守る。
`src/trailers.py` の `TRAILERS` に、確認できた動画だけを登録する。登録した作品だけに「公式予告編を見る（YouTube）」ボタンが出る。未登録の作品にはボタンを出さない（運営者の希望で、公式チャンネル内の検索リンクは使わない）。
- 映画会社・配給会社の公式チャンネル（Marvel Entertainment @marvel、Sony Pictures @SonyPictures、20th Century Studios @20thCenturyStudios、日本の公式チャンネルなど）の動画だけ。
- 各候補を `https://www.youtube.com/oembed?format=json&url=<動画URL>` で取得し、author_name（チャンネル）と title（作品名）が一致するものだけ採用する。確認できない作品は登録しない。推測したURLは使わない。
- 先に `CHANNELS` の3つのチャンネルURLが本物か、チャンネルページで確認する。
- 動画やサムネイルは埋め込まない。別タブで開く普通のリンクにする。
- 追加したらビルドして push し、確認できた作品と、できなかった作品を運営者に報告する。
