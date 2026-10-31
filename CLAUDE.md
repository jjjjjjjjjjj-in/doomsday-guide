# ドゥームズデイ予習ガイド

『アベンジャーズ／ドゥームズデイ』（2026年12月18日 日米同時公開）の予習用の非公式ファンサイト。GitHub Pages（main ブランチのルート）で公開: https://jjjjjjjjjjj-in.github.io/doomsday-guide/

運営者は日本語で、技術に詳しくない。返答は日本語で、短く、専門用語を避ける。

## ビルド
- 生成物（index.html, articles/, assets/, PDF, og.png, sitemap.xml, robots.txt）は手で編集しない。`src/` を編集してから次を実行する:
  - `python3 src/build.py`
  - `node src/render.js`（PDF 2種と og.png。Playwright と IPAGothic フォントを使う）
- コミット作成者は Claude <noreply@anthropic.com>。

## src の中身
- `titles_a.py` / `titles_b.py` / `titles_c.py`: 全68作品（視聴順）。あらすじ・関連性・ポストクレジットなど。
- `importance.py`: 10点満点の重要度。5以上が「① 必ず観るべき」。点数は運営者が決める。勝手に変えない。
- `articles.py`: 解説記事5本。
- `ads.py`: 広告設定（Amazon タグ doomsdayguide-22、もしも経由の楽天 a_id=5875908 など）。「PR」表記とAmazonの表記は自動で出る。誤クリックを誘う広告は入れない。
- `trailers.py`: 予告編リンク。
- `site.css` / `app.js` / `sticky.js`: 見た目と動き。白背景、タイトルは濃いグリーン、見出しは紺。

## キャスト情報のルール
公式発表と噂を必ず分ける。ヒュー・ジャックマン、トビー・マグワイアは2026-10-31時点で噂の段階。

## 公式予告編のリンク（2026-10-31 に61作品を確認・登録済み）
未確認: アイアンマン、アイアンマン2、インクレディブル・ハルク、X-MEN（2000）、X-MEN：ファイナル ディシジョン、X-MEN：フューチャー&パスト、スパイダーマン2（2004）。公式チャンネルで予告編が見つからなかった。追加するときも次の手順を守る。
`src/trailers.py` の `TRAILERS` に、確認できた動画だけを登録する。登録した作品だけに「公式予告編を見る（YouTube）」ボタンが出る。未登録の作品にはボタンを出さない（運営者の希望で、公式チャンネル内の検索リンクは使わない）。
- 映画会社・配給会社の公式チャンネル（Marvel Entertainment @marvel、Sony Pictures @SonyPictures、20th Century Studios @20thCenturyStudios、日本の公式チャンネルなど）の動画だけ。
- 各候補を `https://www.youtube.com/oembed?format=json&url=<動画URL>` で取得し、author_name（チャンネル）と title（作品名）が一致するものだけ採用する。確認できない作品は登録しない。推測したURLは使わない。
- 先に `CHANNELS` の3つのチャンネルURLが本物か、チャンネルページで確認する。
- 動画やサムネイルは埋め込まない。別タブで開く普通のリンクにする。
- 追加したらビルドして push し、確認できた作品と、できなかった作品を運営者に報告する。
