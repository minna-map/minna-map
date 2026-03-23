import os
import google.generativeai as genai
import time

# 1. カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 【ここを書き換えてください！】
# 画面（AI Studio）で見えている名前（例: 'gemini-2.0-flash' や 'gemini-1.5-pro'）を入れてください
MODEL_NAME = 'gemini-3.0-pro' 

model = genai.GenerativeModel(MODEL_NAME)

# 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Starting: {age} {gender} {theme} with {MODEL_NAME}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事をMarkdown形式で書いてください。"
    
    try:
        response = model.generate_content(prompt)
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Success! ({MODEL_NAME})")
        return True
    except Exception as e:
        # ここでエラーが出たら、モデル名が間違っている合図です
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                time.sleep(10) # 1.5 Proなどの上位モデルは少しゆっくり動かします
