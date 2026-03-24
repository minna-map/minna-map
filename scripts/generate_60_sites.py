import os
import time
from google import genai

# 1. クライアント設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def find_working_model():
    """あなたのカギで「今、本当に動く」モデルを自動で見つける"""
    print("--- Model Discovery Start ---")
    # 2026年の主要モデル候補
    candidates = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    
    for model_id in candidates:
        try:
            print(f"Testing {model_id}...")
            # 実際に1文字生成させてテスト
            client.models.generate_content(model=model_id, contents="test")
            print(f"✅ Found! Using: {model_id}")
            return model_id
        except Exception as e:
            print(f"❌ {model_id} is not available. (Error: {e.code if hasattr(e, 'code') else 'Unknown'})")
            continue
    
    # 候補が全滅した場合、リストから直接取得を試みる
    try:
        for m in client.models.list():
            if "generateContent" in m.supported_methods:
                print(f"✅ Fallback Found: {m.name}")
                return m.name
    except:
        pass
        
    return "gemini-1.5-flash" # 最終手段

# 2. 使えるモデルを決定
WORKING_MODEL = find_working_model()

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Generating: {age} {gender} {theme}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を書いてください。"
    
    try:
        response = client.models.generate_content(
            model=WORKING_MODEL,
            contents=prompt
        )
        
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Success with {WORKING_MODEL}")
        return True
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        return False

if __name__ == "__main__":
    print(f"Target Model confirmed: {WORKING_MODEL}")
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                # 429エラーを避けるため、40秒しっかり休みます
                print("Waiting 40s for Quota limit...")
                time.sleep(40)
