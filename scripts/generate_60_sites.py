import os
import google.generativeai as genai
from datetime import datetime
import time

# API Key Setting
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 60 Patterns (6 ages x 2 genders x 5 themes)
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate_article(age, gender, theme):
    age_jp = age.replace("s", "代")
    gender_jp = "男性" if gender == "male" else "女性"
    
    # Simple Prompt to avoid errors
    prompt = f"Write a Japanese blog article for {age_jp}{gender_jp} about {theme} in March 2026. Format: Markdown."
    
    try:
        response = model.generate_content(prompt)
        # Create folder and save
        dir_path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(dir_path, exist_ok=True)
        with open(f"{dir_path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Successfully generated: {age} {gender} {theme}")
        return True
    except Exception as e:
        print(f"Error at {age} {gender} {theme}: {str(e)}") # エラーの内容を具体的に表示
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate_article(a, g, t)
                time.sleep(5) # Wait 5 seconds to avoid rate limits
