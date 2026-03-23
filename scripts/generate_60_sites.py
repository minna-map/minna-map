import os
import google.generativeai as genai
from datetime import datetime
import time

# API Key Setting
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use a very stable model name
model = genai.GenerativeModel('gemini-1.5-flash')

# 60 Patterns (6 ages x 2 genders x 5 themes)
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate_article(age, gender, theme):
    age_jp = age.replace("s", "代")
    gender_jp = "男性" if gender == "male" else "女性"
    
    prompt = f"Write a Japanese blog article for {age_jp}{gender_jp} about {theme} in March 2026. Use professional analyst tone. Format: Markdown."
    
    try:
        # Generate Content
        response = model.generate_content(prompt)
        
        # Save to folders
        dir_path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(dir_path, exist_ok=True)
        
        with open(f"{dir_path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Successfully generated: {age} {gender} {theme}")
        return True
    except Exception as e:
        # Check specific error
        print(f"Error at {age} {gender} {theme}: {str(e)}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate_article(a, g, t)
                # Take a breath for 5 seconds
                time.sleep(5)
