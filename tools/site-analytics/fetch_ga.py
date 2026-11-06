"""Google アナリティクス（GA4）から数字を集めて data/ に CSV で保存するロボット。

GitHub Actions が毎週動かす。必要なもの（GitHub の Settings → Secrets and variables → Actions）:
  GA_KEY          ロボット用アカウント（サービスアカウント）の鍵（JSON の中身をそのまま）
  GA_PROPERTY_ID  アナリティクスのプロパティ ID（数字だけ。例: 512345678）
"""
import csv
import datetime as dt
import json
import os
import sys

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, OrderBy, RunReportRequest
from google.oauth2 import service_account

# 名前: (並べる項目, 数える項目, 期間の開始, 並べ替え)
REPORTS = {
    # 毎日の合計（1年分）
    "daily": (["date"], ["activeUsers", "newUsers", "sessions", "screenPageViews", "engagementRate", "averageSessionDuration"], "365daysAgo", "date"),
    # よく見られているページ
    "pages": (["hostName", "pagePath", "pageTitle"], ["screenPageViews", "activeUsers", "userEngagementDuration", "engagementRate"], "28daysAgo", "-screenPageViews"),
    # 最初に開かれたページ
    "landing": (["landingPage"], ["sessions", "activeUsers", "engagementRate", "bounceRate"], "28daysAgo", "-sessions"),
    # どこから来たか（Google 検索、X、LINE など）
    "sources": (["sessionSource", "sessionMedium"], ["sessions", "activeUsers", "engagementRate", "averageSessionDuration"], "28daysAgo", "-sessions"),
    # どこから来たか × 毎日（バズった日の確認用）
    "sources_daily": (["date", "sessionSource", "sessionMedium"], ["sessions"], "90daysAgo", "date"),
    # 国と言語（英語版が読まれているか）
    "countries": (["country", "language"], ["activeUsers", "sessions"], "28daysAgo", "-activeUsers"),
    # スマホかパソコンか
    "devices": (["deviceCategory"], ["activeUsers", "sessions", "engagementRate"], "28daysAgo", "-activeUsers"),
    # 曜日と時間（Xに投稿する時間を決める参考）
    "hours": (["dayOfWeekName", "hour"], ["sessions", "activeUsers"], "28daysAgo", "-sessions"),
    # ボタンのクリックなどの出来事
    "events": (["eventName"], ["eventCount", "activeUsers"], "28daysAgo", "-eventCount"),
    # 外部リンクのクリック（予告編・広告・シェアボタンなど）
    "outbound": (["linkDomain", "linkUrl"], ["eventCount"], "28daysAgo", "-eventCount"),
}


def run(client, prop, name, dims, mets, start, order):
    desc = order.startswith("-")
    key = order.lstrip("-")
    ob = OrderBy(metric=OrderBy.MetricOrderBy(metric_name=key), desc=desc) if key in mets \
        else OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name=key), desc=desc)
    req = RunReportRequest(property=f"properties/{prop}", dimensions=[Dimension(name=d) for d in dims],
                           metrics=[Metric(name=m) for m in mets], date_ranges=[DateRange(start_date=start, end_date="yesterday")],
                           order_bys=[ob], limit=10000)
    res = client.run_report(req)
    rows = [[v.value for v in r.dimension_values] + [v.value for v in r.metric_values] for r in res.rows]
    return dims + mets, rows


def main():
    prop = os.environ["GA_PROPERTY_ID"].strip()
    info = json.loads(os.environ["GA_KEY"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/analytics.readonly"])
    client = BetaAnalyticsDataClient(credentials=creds)
    today = dt.date.today().isoformat()
    for folder in (f"data/{today}", "data/latest"):
        os.makedirs(folder, exist_ok=True)
    failed = []
    for name, (dims, mets, start, order) in REPORTS.items():
        try:
            head, rows = run(client, prop, name, dims, mets, start, order)
        except Exception as e:  # 1つ失敗しても残りは集める
            failed.append(f"{name}: {e}")
            continue
        for folder in (f"data/{today}", "data/latest"):
            with open(f"{folder}/{name}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(head)
                w.writerows(rows)
        print(f"{name}: {len(rows)} rows")
    with open("data/latest/fetched_at.txt", "w", encoding="utf-8") as f:
        f.write(dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST") + "\n")
        f.writelines(f"FAILED {x}\n" for x in failed)
    if failed:
        print("\n".join(failed), file=sys.stderr)
        if len(failed) == len(REPORTS):
            sys.exit(1)


if __name__ == "__main__":
    main()
