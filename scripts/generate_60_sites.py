import os
import time
from datetime import datetime
from google import genai
from google.genai import errors

# 1. カギの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 💡 根本解決：404を避けるための「名前の絶対指定」
# ログで以前「FOUND」と出ていた 1.0-pro を最優先にします。
# もし2.0が 429(枠0) なら、1.0の方が枠が空いている可能性が極めて高いです。
MODEL_ID = "gemini-1.0-pro"

# 5日間のテーマ（悩み）サイクル
TOPICS = [
    {"id": "A", "theme": "進路・将来の不安やキャリア形成"},
    {"id": "B", "theme": "対人関係・孤独感・コミュニティの悩み"},
    {"id": "C", "theme": "お金の管理・投資・経済的な自立"},
    {"id": "D", "theme": "心身の健康・メンタルヘルス・生活習慣"},
    {"id": "E", "theme": "自己研鑽・新しいスキルの習得・趣味の深化"}
]

day_index = datetime.now().day % 5
current_topic = TOPICS[day_index]
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]

def generate_daily_set(age, gender):
    print(f"Generating: {age} {gender} Topic {current_topic['id']} using {MODEL_ID}...")
    
    prompt = (
        f"あなたはプロのアナリストです。{age}{gender}が抱える「{current_topic['theme']}」という悩みについて、"
        f"2026年の最新情勢を踏まえた解決策をMarkdown形式で執筆してください。"
        f"最後に政治家マップと補助金マップへのリンクを入れてください。"
    )
    
    try:
        # モデル名を直接指定（models/ は不要）
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        
        path = f"sites/{age}/{gender}/topic_{current_topic['id']}"
        os.makedirs(path, exist_ok=True)
        
        with open(f"{path}/index.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ SUCCESS: {age} {gender}")
        return True
    except errors.ClientError as e:
        # 429が出た場合は「枠(Quota)」の問題なので、時間を空けるしかありません
        if "429" in str(e):
            print(f"❌ QUOTA ERROR (429): あなたのアカウントの無料枠が 0 です。")
            print("解決策: Google AI Studioで 'Create API key in NEW project' を試してください。")
        else:
            print(f"❌ FAILED ({MODEL_ID}): {e}")
        return False

if __name__ == "__main__":
    print(f"--- Cycle Target: Topic {current_topic['id']} ---")
    
    for a in ages:
        for g in genders:
            success = generate_daily_set(a, g)
            # 枠制限を回避するため、さらに長く休みます（80秒）
            print("Waiting 80s...")
            time.sleep(80)
