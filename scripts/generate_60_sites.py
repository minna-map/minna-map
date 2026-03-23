import os
import google.generativeai as genai
import time

# API Key Setting
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use the most stable model name
model = genai.GenerativeModel('gemini-1.5-flash')

# Patterns
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate(age, gender, theme):
    print(f"Generating: {age} {gender} {theme}...")
    prompt = f"Write a professional blog article for {age} {gender} about {theme} in 2026. Use Japanese. Format: Markdown."
    try:
        response = model.generate_content(prompt)
        path = f"sites/{age}/{gender}/{theme}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    for a in ages:
        for g in genders:
            for t in themes:
                generate(a, g, t)
                time.sleep(5)
