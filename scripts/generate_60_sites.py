import os
import time
from datetime import datetime
from google import genai

# 1. カギの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 💡 根本解決のポイント：
# 2.0が「Limit 0」なら、最も制限のゆるい「1.5-flash-8b」に切り替えます。
# これにより「RESOURCE_EXHAUSTED」を物理的に回避します。
MODEL_ID = "gemini-1.5-flash-8b" 

# 5日間のテーマ（悩み）サイクル
TOPICS = [
    {"id": "A", "theme": "進路・将来の不安やキャリア形成"},
    {"id": "B", "theme": "対人関係・孤独感・コミュニティの悩み"},
    {"id": "C", "theme": "お金の管理・投資・経済的な自立"},
    {"id": "D", "theme": "心身の健康・メンタルヘルス・生活習慣"},
    {"id": "E", "theme": "自己研鑽・新しいスキルの習得・趣味の深化"}
]

# 今日の日付（日本時間）から0〜4を計算
day_index = datetime.now().day % 5
current_topic = TOPICS[day_index]

ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]

def generate_daily_set(age, gender):
    print(f"Generating: {age} {gender} Topic {current_topic['id']} with {MODEL_ID}...")
    
    prompt = (
        f"あなたはプロのアナリストです。{age}{gender}が抱える「{current_topic['theme']}」という悩みについて、"
        f"2026年の最新情勢を踏まえた解決策を1500字以上のMarkdown形式で執筆してください。"
        f"記事の最後には、政治家マップと補助金マップへのリンクを自然に入れてください。"
    )
    
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        
        # フォルダ構造を整理
        path = f"sites/{age}/{gender}/topic_{current_topic['id']}"
        os.makedirs(path, exist_ok=True)
        
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Success: {age} {gender}")
        return True
    except Exception as e:
        print(f"❌ Error with {MODEL_ID}: {e}")
        return False

if __name__ == "__main__":
    print(f"--- Running Cycle: Topic {current_topic['id']} ---")
    
    for a in ages:
        for g in genders:
            generate_daily_set(a, g)
            # 💡 機械的判断を避けるため、待ち時間を「70秒」に増やします
            print("Cooling down for 70s...")
            time.sleep(70)
