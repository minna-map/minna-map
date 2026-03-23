import os
import google.generativeai as genai
import time

# 1. カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def find_best_model():
    """使えるAIの名前を自動で探す魔法の機能"""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return m.name # 正しい名前を見つけたらそれを返す
        return 'models/gemini-1.5-flash' # 見つからなければ標準の名前
    except:
        return 'models/gemini-1.5-flash'

# ロボットに自分で名前を探させる
MODEL_NAME = find_best_model()
print(f"Using Model: {MODEL_NAME}")
model = genai.GenerativeModel(MODEL_NAME)

# 60パターン
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    prompt = f"Write a professional blog article for {age} {gender} about {theme} in 2026. Use Japanese. Format: Markdown."
    try:
        response = model.generate_content(prompt)
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("--- Success! ---")
        return True
    except Exception as e:
        print(f"Error details: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                time.sleep(5) # 5秒休んで安全に動かす
