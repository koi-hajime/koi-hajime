"""
Google Search Console URL Inspection API - インデックス状況チェック
koi-hajime用
"""

import subprocess
import json
import sys
import urllib.request
import time

SITE_URL = "https://koi-hajime.com/"

URLS = [
    "https://koi-hajime.com/",
    "https://koi-hajime.com/privacy.html",
    "https://koi-hajime.com/articles/freeter-deai-nai-matching.html",
    "https://koi-hajime.com/articles/freeter-kekkon-matching.html",
    "https://koi-hajime.com/articles/matching-app-20dai-hajimete.html",
    "https://koi-hajime.com/articles/matching-app-man-20dai.html",
    "https://koi-hajime.com/articles/matching-app-ryokin-hikaku.html",
    "https://koi-hajime.com/articles/matching-profile-kakikata.html",
    "https://koi-hajime.com/articles/pairs-review.html",
    "https://koi-hajime.com/articles/seishain-matching-timing.html",
]

def get_access_token():
    result = subprocess.run(
        ["/Users/yamato_o/Downloads/google-cloud-sdk/bin/gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("エラー: アクセストークン取得失敗")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def inspect_url(url, token):
    data = json.dumps({
        "inspectionUrl": url,
        "siteUrl": SITE_URL,
    }).encode()
    req = urllib.request.Request(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-goog-user-project": "project-51d120e2-4c4f-4acd-9d8",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def main():
    print("アクセストークン取得中...")
    token = get_access_token()
    print("取得完了\n")

    indexed = []
    not_indexed = []
    errors = []

    total = len(URLS)
    for i, url in enumerate(URLS, 1):
        label = url.replace("https://koi-hajime.com/", "") or "index"
        print(f"[{i:2d}/{total}] {label}", end=" ... ")

        status, body = inspect_url(url, token)

        if status != 200:
            msg = body.get("error", {}).get("message", str(body))
            print(f"エラー ({status}): {msg}")
            errors.append((label, msg))
        else:
            result = body.get("inspectionResult", {})
            index_status = result.get("indexStatusResult", {})
            verdict = index_status.get("verdict", "UNKNOWN")

            if verdict == "PASS":
                coverage = index_status.get("coverageState", "")
                print(f"インデックス済み ({coverage})")
                indexed.append(label)
            else:
                coverage = index_status.get("coverageState", verdict)
                print(f"未インデックス ({coverage})")
                not_indexed.append((label, coverage))

        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"インデックス済み: {len(indexed)}件 / {total}件")
    print(f"未インデックス : {len(not_indexed)}件")
    print(f"エラー         : {len(errors)}件")

    if indexed:
        print(f"\n【インデックス済み一覧】")
        for label in indexed:
            print(f"  - {label}")

    if not_indexed:
        print(f"\n【未インデックス一覧】")
        for label, reason in not_indexed:
            print(f"  - {label} ({reason})")

    if errors:
        print(f"\n【エラー一覧】")
        for label, msg in errors:
            print(f"  - {label}: {msg}")

if __name__ == "__main__":
    main()
