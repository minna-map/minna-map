import os
from google import genai # 新しい読み込み方
import time

# 1. 新しいクライアントの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    # プロンプト（お願い）
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。最後に政治家マップと補助金マップへのリンクを必ず入れてください。"
    
    try:
        # 新規格の呼び出し方 (Gemini 2.0 Flash を使用)
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Success!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                time.sleep(5) # 5秒休み
