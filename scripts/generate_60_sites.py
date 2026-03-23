import os
import google.generativeai as genai
import time

# 1. カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# あなたのアカウントで「確実に動く」モデルを指定します
MODEL_NAME = 'gemini-1.0-pro'
model = genai.GenerativeModel(MODEL_NAME)

# 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。最後に政治家マップと補助金マップへのリンクを必ず入れてください。"
    try:
        # AIにお願いする
        response = model.generate_content(prompt)
        
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Success! ({MODEL_NAME} used)")
        return True
    except Exception as e:
        print(f"❌ Error at {age} {gender} {theme}: {e}")
        return False

if __name__ == "__main__":
    print(f"Starting factory with model: {MODEL_NAME}")
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                # 1.0-proは少しゆっくり動かすのがコツです（10秒休み）
                time.sleep(10)
