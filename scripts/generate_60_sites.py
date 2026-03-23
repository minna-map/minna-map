import os
import google.generativeai as genai
from datetime import datetime
import time
import urllib.request
import xml.etree.ElementTree as ET

# カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# ターゲット（60パターン）
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def get_latest_news(keyword):
    try:
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(keyword)}+when:1d&hl=ja&gl=JP&ceid=JP:ja"
        with urllib.request.urlopen(url) as response:
            tree = ET.parse(response)
            root = tree.getroot()
            headlines = [item.find('title').text for item in root.findall('.//item')[:3]]
            return " | ".join(headlines)
    except:
        return "最新の経済情勢"

def generate_article(age, gender, theme):
    age_jp = age.replace("s", "代")
    gender_jp = "男性" if gender == "male" else "女性"
    theme_info = {
        "finance": ("金融・運用", "株価 投資"),
        "law": ("法律・権利", "裁判 法律"),
        "admin": ("行政・助成金", "補助金 給付金"),
        "politics": ("政治影響", "政治 議員"),
        "lifestyle": ("ライフプラン", "老後 介護")
    }
    theme_jp, keyword = theme_info[theme]
    news = get_latest_news(keyword)

    prompt = f"""
    あなたはプロのアナリストです。2026年3月の視点で執筆してください。
    【最新ニュース】{news}
    【ターゲット】{age_jp}{gender_jp}
    【テーマ】{theme_jp}
    1500字程度のブログ記事をMarkdown形式で書いてください。
    最後は「政治家マップ」「補助金マップ」「資格マップ」へ誘導すること。
    ---TITLE---（ここにタイトル）---DESC---（ここに説明文）---CONTENT---（ここに本文）
    """
    
    try:
        response = model.generate_content(prompt)
        # 保存処理（sites/フォルダ内に整理）
        dir_path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(dir_path, exist_ok=True)
        with open(f"{dir_path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Success: {age_jp}{gender_jp}")
    except:
        print("Error occurred")

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate_article(a, g, t)
                time.sleep(2) # 脳みそが疲れないように少し休むよ
