import os
import time
from google import genai

# 1. 最新のクライアント設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 無料枠で最も安定しているモデルを指定
MODEL_ID = "gemini-1.5-flash" 

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Generating for: {age} {gender} {theme}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。"
    
    try:
        # 最新の生成命令
        response = client.models.generate_content(
            model=MODEL_ID,
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
                # 記事を作成
                success = generate(a, g, t)
                
                # 💡 根本解決のポイント：
                # 無料枠の制限を避けるため、1記事ごとに40秒間しっかり休みます。
                # これにより、60記事を数時間かけて確実に完走させます。
                print("Waiting 40 seconds for safety...")
                time.sleep(40)
