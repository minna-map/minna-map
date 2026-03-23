import os
from google import genai
import time
import sys

# 1. カギの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate_with_retry(age, gender, theme, max_retries=3):
    """エラーが出ても自動で待機してやり直すプロの機能"""
    prompt = f"あなたはプロの株式アナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。最後に政治家マップと補助金マップへのリンクを必ず入れてください。"
    
    for attempt in range(max_retries):
        try:
            # 無料枠で最も安定しているモデルに変更します
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt
            )
            
            path = f"sites/{age}/{gender}/{theme}"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}/index.md", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"✅ Success: {age} {gender} {theme}")
            return True

        except Exception as e:
            if "429" in str(e):
                wait_time = 30 * (attempt + 1) # 30秒、60秒...と待機時間を増やします
                print(f"⚠️ 混雑中... {wait_time}秒お休みしてやり直します (残り{max_retries - attempt - 1}回)")
                time.sleep(wait_time)
            else:
                print(f"❌ Error: {e}")
                return False
    return False

if __name__ == "__main__":
    print("🚀 工場を『安全運転モード』で開始します...")
    for a in ages:
        for g in genders:
            for t in themes:
                generate_with_retry(a, g, t)
                # 次の注文まで20秒あけます（これが無料枠のコツです）
                time.sleep(20)
