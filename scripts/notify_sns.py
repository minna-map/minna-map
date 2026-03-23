import os
from atproto import Client

def notify():
    try:
        client = Client()
        client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])
        text = "【自動更新】60の専門ブログを更新しました！最新の政治・経済ニュースをアナリストが分析。 #資産運用 #2026年 https://minna-map.github.io"
        client.send_post(text)
        print("SNS投稿成功！")
    except:
        print("SNSは設定待ちだよ")

if __name__ == "__main__":
    notify()
