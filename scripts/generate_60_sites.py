import os
from google import genai
import time

# 1. カギの設定
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def find_working_model():
    """今、あなたのカギで本当に使えるAIの名前を自動で見つける魔法"""
    print("AIのモデルを探索中...")
    try:
        # 使えるモデルをリストアップ
        available_models = []
        for m in client.models.list():
            # 文章生成ができるモデルだけを抽出
            if 'generateContent' in m.supported_methods:
                # 2026年で最も推奨される名前を優先的に探す
                if '1.5-flash' in m.name or '2.0-flash' in m.name:
                    print(f"✅ 利用可能なモデルを発見: {m.name}")
                    return m.name
                available_models.append(m.name)
        
        if available_models:
            print(f"⚠️ 推奨モデルが見つかりません。代わりのモデルを使用します: {available_models[0]}")
            return available_models[0]
            
    except Exception as e:
        print(f"❌ モデルの探索に失敗しました: {e}")
    
    # 万が一の時のための最終手段
    return 'gemini-1.5-flash'

# 2. 実行時に「今使える名前」を特定する
MODEL_ID = find_working_model()

# 60パターン設定
ages = ["10s", "20s", "30s", "40s", "50s", "60s"]
genders = ["male", "female"]
themes = ["finance", "law", "admin", "politics", "lifestyle"]

def generate_with_retry(age, gender, theme, max_retries=3):
    prompt = f"あなたはプロのアナリストです。{age}{gender}向けに、{theme}についての2026年3月の最新記事を1500字以上のMarkdown形式で書いてください。"
    
    for attempt in range(max_retries):
        try:
            # 特定したモデル名でお仕事を開始
            response = client.models.generate_content(
                model=MODEL_ID, 
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
                print(f"⚠️ 混雑中... 30秒待機します (残り{max_retries - attempt - 1}回)")
                time.sleep(30)
            else:
                print(f"❌ Error at {age} {gender} {theme}: {e}")
                return False
    return False

if __name__ == "__main__":
    print(f"🚀 工場開始！ 使用モデル: {MODEL_ID}")
    for a in ages:
        for g in genders:
            for t in themes:
                generate_with_retry(a, g, t)
                # 連続注文で怒られないように20秒あける
                time.sleep(20)
