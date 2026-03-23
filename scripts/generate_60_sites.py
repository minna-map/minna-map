import os
import google.generativeai as genai
import time

# API Key Setting
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 最新の安定した名前で呼び出します
model = genai.GenerativeModel('gemini-1.5-flash')

# 60 Patterns
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Working on: {age} {gender} {theme}...")
    prompt = f"Write a professional blog article for {age} {gender} about {theme} in 2026. Use Japanese language. Format: Markdown."
    try:
        # AIにお話を作ってもらいます
        response = model.generate_content(prompt)
        
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success!")
        return True
    except Exception as e:
        # もしエラーが出たら内容を教えてもらいます
        print(f"Error details: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                # Geminiが疲れないように5秒お休みします
                time.sleep(5)
