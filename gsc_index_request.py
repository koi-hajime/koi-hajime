"""
Google Indexing API - URLインデックス申請スクリプト
koi-hajime用
"""

import subprocess
import json
import sys

URLS = [
    "https://koi-hajime.com/",
    "https://koi-hajime.com/articles/seishain-matching-timing.html",
    "https://koi-hajime.com/articles/matching-app-20dai-hajimete.html",
    "https://koi-hajime.com/articles/freeter-deai-nai-matching.html",
    "https://koi-hajime.com/articles/matching-app-ryokin-hikaku.html",
    "https://koi-hajime.com/articles/matching-profile-kakikata.html",
    "https://koi-hajime.com/articles/pairs-review.html",
    "https://koi-hajime.com/articles/matching-app-man-20dai.html",
    "https://koi-hajime.com/articles/freeter-kekkon-matching.html",
    "https://koi-hajime.com/privacy.html",
    "https://koi-hajime.com/articles/matching-shinanai.html",
    "https://koi-hajime.com/articles/message-tsuzukanai.html",
    "https://koi-hajime.com/articles/matching-app-photo-nashi.html",
    "https://koi-hajime.com/articles/matching-app-dame-pattern.html",
    "https://koi-hajime.com/articles/shakaijin-1nenme-matching.html",
    "https://koi-hajime.com/articles/naishikei-matching.html",
    "https://koi-hajime.com/articles/chihou-matching.html",
    "https://koi-hajime.com/articles/hitorigurase-matching.html",
    "https://koi-hajime.com/articles/kekkon-so-vs-matching.html",
    "https://koi-hajime.com/articles/20dai-konkatsu-hajimekata.html",
    "https://koi-hajime.com/articles/freeter-seishain-deai.html",
    "https://koi-hajime.com/articles/matching-app-fee-dansei.html",
    # 追加記事（30本）
    "https://koi-hajime.com/articles/matching-first-message.html",
    "https://koi-hajime.com/articles/matching-line-exchange.html",
    "https://koi-hajime.com/articles/matching-first-meet.html",
    "https://koi-hajime.com/articles/matching-kokuhaku-timing.html",
    "https://koi-hajime.com/articles/matching-unmatch-reason.html",
    "https://koi-hajime.com/articles/matching-second-date.html",
    "https://koi-hajime.com/articles/date-plan-first.html",
    "https://koi-hajime.com/articles/matching-app-photo-tips.html",
    "https://koi-hajime.com/articles/matching-app-jiko-shoukai.html",
    "https://koi-hajime.com/articles/matching-app-return-message.html",
    "https://koi-hajime.com/articles/bachelo-date-review.html",
    "https://koi-hajime.com/articles/whippy-review.html",
    "https://koi-hajime.com/articles/nacodo-review.html",
    "https://koi-hajime.com/articles/hanamel-review.html",
    "https://koi-hajime.com/articles/matching-app-20dai-zenhan.html",
    "https://koi-hajime.com/articles/matching-app-hitomishiri.html",
    "https://koi-hajime.com/articles/matching-app-busy.html",
    "https://koi-hajime.com/articles/matching-app-shigoto-kakikata.html",
    "https://koi-hajime.com/articles/matching-app-two-use.html",
    "https://koi-hajime.com/articles/tensyoku-go-matching.html",
    "https://koi-hajime.com/articles/matching-app-cost-plan.html",
    "https://koi-hajime.com/articles/matching-sagi-mibujoshiki.html",
    "https://koi-hajime.com/articles/concoi-vs-pappy.html",
    "https://koi-hajime.com/articles/matching-app-kekkon-zentei.html",
    "https://koi-hajime.com/articles/kekkon-so-hikaku.html",
    "https://koi-hajime.com/articles/kekkon-so-20dai-nyuukai.html",
    "https://koi-hajime.com/articles/matching-vs-konkatsu-party.html",
    "https://koi-hajime.com/articles/matching-app-success-rate.html",
    "https://koi-hajime.com/articles/matching-app-dansei-osusume.html",
    "https://koi-hajime.com/articles/matching-app-complete-guide.html",
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
