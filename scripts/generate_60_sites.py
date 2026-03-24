import os
import time
from datetime import datetime
from google import genai

# 1. 新しいプロジェクトのカギを設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2026年の標準モデルに固定（429を避けるためこれ一本に絞ります）
MODEL_ID = "gemini-2.0-flash" 

# 5日間の悩みサイクル
TOPICS = [
    {"id": "A", "theme": "進路・将来の不安やキャリア形成"},
    {"id": "B", "theme": "対人関係・孤独感・コミュニティの悩み"},
    {"id": "C", "theme": "お金の管理・投資・経済的な自立"},
    {"id": "D", "theme": "心身の健康・メンタルヘルス・生活習慣"},
    {"id": "E", "theme": "自己研鑽・新しいスキルの習得・趣味の深化"}
]

# 今日の悩み（日本時間基準）
day_index = datetime.now().day % 5
current_topic = TOPICS[day_index]

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]

def generate(age, gender):
    print(f"--- Processing: {age} {gender} (Topic {current_topic['id']}) ---")
    prompt = f"あなたはプロのアナリストです。{age}{gender}の悩み「{current_topic['theme']}」について、2026年の最新視点で1500字以上のMarkdown記事を書いてください。"
    
    try:
        # 2.0-flashを呼び出し
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        
        path = f"sites/{age}/{gender}/topic_{current_topic['id']}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ SUCCESS")
        return True
    except Exception as e:
        print(f"❌ FATAL: {e}")
        return False

if __name__ == "__main__":
    print(f"Factory Start: Topic {current_topic['id']}")
    for a in ages:
        for g in genders:
            generate(a, g)
            # 💡 12記事なので、安全のために「80秒」休みます
            print("Cooling down 80s for safety...")
            time.sleep(80)
