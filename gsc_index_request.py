"""
Google Indexing API - URLインデックス申請スクリプト
koi-hajime用
"""

import subprocess
import json
import sys

URLS = [
    "https://koi-hajime.github.io/koi-hajime/",
    "https://koi-hajime.github.io/koi-hajime/articles/seishain-matching-timing.html",
    "https://koi-hajime.github.io/koi-hajime/articles/matching-app-20dai-hajimete.html",
    "https://koi-hajime.github.io/koi-hajime/articles/freeter-deai-nai-matching.html",
    "https://koi-hajime.github.io/koi-hajime/articles/matching-app-ryokin-hikaku.html",
    "https://koi-hajime.github.io/koi-hajime/articles/matching-profile-kakikata.html",
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

def request_indexing(url, token):
    import urllib.request
    data = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
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
    print(f"取得完了\n")

    success = 0
    failed = 0

    total = len(URLS)
    for i, url in enumerate(URLS, 1):
        print(f"[{i:2d}/{total}] {url.split('/')[-1] or 'index'}", end=" ... ")
        status, body = request_indexing(url, token)
        if status == 200:
            print("OK")
            success += 1
        else:
            print(f"NG ({status}): {body.get('error', {}).get('message', body)}")
            failed += 1

    print(f"\n完了: 成功 {success}件 / 失敗 {failed}件")

if __name__ == "__main__":
    main()
