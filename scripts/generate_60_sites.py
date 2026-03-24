import os
import time
from datetime import datetime
from google import genai

# 1. カギの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2026年現在の安定モデル（もし2.0がダメなら1.5-flashに書き換えてください）
MODEL_ID = "gemini-2.0-flash" 

# 5日間のテーマ（悩み）サイクル
TOPICS = [
    {"id": "A", "theme": "進路・将来の不安やキャリア形成"},
    {"id": "B", "theme": "対人関係・孤独感・コミュニティの悩み"},
    {"id": "C", "theme": "お金の管理・投資・経済的な自立"},
    {"id": "D", "theme": "心身の健康・メンタルヘルス・生活習慣"},
    {"id": "E", "theme": "自己研鑽・新しいスキルの習得・趣味の深化"}
]

# 今日の日付から0〜4のインデックスを計算
day_index = datetime.now().day % 5
current_topic = TOPICS[day_index]

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]

def generate_daily_set(age, gender):
    print(f"Generating: {age} {gender} Topic {current_topic['id']}...")
    
    prompt = (
        f"あなたはプロのアナリストです。{age}{gender}が抱える「{current_topic['theme']}」という悩みについて、"
        f"2026年3月の最新情勢を踏まえた解決策を1500字以上のMarkdown形式で執筆してください。"
        f"記事の最後には必ず、政治家マップと補助金マップへのリンクを自然な形で挿入してください。"
    )
    
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        
        # フォルダ名には悩みのID（A, B...）を含めて保存
        path = f"sites/{age}/{gender}/topic_{current_topic['id']}"
        os.makedirs(path, exist_ok=True)
        
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Success: {age} {gender}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print(f"--- Today's Mission: Topic {current_topic['id']} ({current_topic['theme']}) ---")
    
    for a in ages:
        for g in genders:
            generate_daily_set(a, g)
            # 💡 12記事なので、1分に1記事のペース（60秒休み）で動かせば制限に余裕で間に合います
            print("Waiting 60s to respect quota...")
            time.sleep(60)
