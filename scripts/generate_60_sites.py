import os
import google.generativeai as genai
import time

# カギの設定
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 2026年の標準モデル（画面で見えている名前に合わせています）
MODEL_NAME = 'gemini-2.0-flash' 
model = genai.GenerativeModel(MODEL_NAME)

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事をMarkdown形式で書いてください。政治家マップへの言及も含めてください。"
    try:
        response = model.generate_content(prompt)
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Success")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                time.sleep(5)
