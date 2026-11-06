# site-analytics（非公開）

mocchima.com のアクセス数を Google アナリティクスから毎日自動で集めて、`data/` に保存するロボット。

- `data/latest/`: 一番新しい数字（Claude はここを読んで分析する）
- `data/日付/`: その日に集めた数字（あとで比べる用）
- `fetch_ga.py`: 集める中身。`.github/workflows/fetch.yml`: 毎日 朝9時7分（日本時間）に動かす設定。

必要な秘密の値（Settings → Secrets and variables → Actions → New repository secret）:
- `GA_KEY`: ロボット用アカウント（サービスアカウント）の鍵 JSON の中身
- `GA_PROPERTY_ID`: アナリティクスのプロパティ ID（数字）

このリポジトリは必ず非公開のままにする（アクセスの数字が入るため）。
