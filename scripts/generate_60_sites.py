import os
import google.generativeai as genai
from datetime import datetime
import time

# API Key Setting
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use the most stable model name
model = genai.GenerativeModel('gemini-1.5-flash')

# 60 Patterns
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate_article(age, gender, theme):
    age_jp = age.replace("s", "代")
    gender_jp = "男性" if gender == "male" else "女性"
    
    prompt = f"あなたはプロのアナリストです。{age_jp}{gender_jp}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。最後に政治家マップと補助金マップへのリンクを必ず入れてください。"
    
    try:
        # Generate content with error check
        response = model.generate_content(prompt)
        
        # Save to folder
        dir_path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(dir_path, exist_ok=True)
        
        with open(f"{dir_path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Success: {age} {gender} {theme}")
        return True
    except Exception as e:
        print(f"Error at {age} {gender} {theme}: {str(e)}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate_article(a, g, t)
                # Take a 3-second break to stay safe
                time.sleep(3)
