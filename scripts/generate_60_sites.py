import os
import google.generativeai as genai
import time

# 1. カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_best_model():
    """今この瞬間、本当に動くモデルを自動で見つける"""
    candidates = ['gemini-1.5-flash', 'gemini-1.0-pro', 'models/gemini-1.5-flash', 'models/gemini-1.0-pro']
    
    print("--- 接続テスト開始 ---")
    for name in candidates:
        try:
            m = genai.GenerativeModel(name)
            # 実際に1文字だけ生成させてテスト
            m.generate_content("test")
            print(f"✅ 成功: {name} を使用します")
            return m
        except Exception:
            print(f"❌ 失敗: {name}")
            continue
    
    # 全部ダメな場合の最後の手段
    print("⚠️ 候補が全滅しました。標準モデルで強行します。")
    return genai.GenerativeModel('gemini-1.0-pro')

# 2. 使えるAIを決定
model = get_best_model()

# 3. 60パターン
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Generating article for: {age} {gender} {theme}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。最後に政治家マップと補助金マップへのリンクを必ず入れてください。"
    
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
                # 1.0-proの場合、少しゆっくり動かすのがコツ（10秒）
                time.sleep(10)
