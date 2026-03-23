import os
import google.generativeai as genai
import time

# 1. カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_working_model():
    """動くAIを実際に見つけるまでテストする機能"""
    # 試してみたいモデルのリスト（新しい順）
    candidate_models = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'models/gemini-1.5-flash',
        'gemini-1.0-pro'
    ]
    
    print("Searching for a working AI model...")
    for model_name in candidate_models:
        try:
            test_model = genai.GenerativeModel(model_name)
            # 実際に短い挨拶ができるかテスト
            response = test_model.generate_content("Hi")
            if response:
                print(f"✅ Found working model: {model_name}")
                return test_model
        except Exception as e:
            print(f"❌ Model {model_name} failed. Trying next...")
            continue
    
    # 全部ダメだった場合、リストにある最初のものを一応返す
    print("⚠️ No model responded. Using default fallback.")
    return genai.GenerativeModel('gemini-1.5-flash')

# 2. 最初に「動くAI」を特定する
active_model = get_working_model()

# 3. 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    prompt = f"Write a professional blog article for {age} {gender} about {theme} in 2026. Use Japanese. Format: Markdown."
    try:
        # さっき見つけた「動くAI」でお仕事をする
        response = active_model.generate_content(prompt)
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
                time.sleep(5) # 安全のために5秒休み
