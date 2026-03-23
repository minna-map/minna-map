import os
import google.generativeai as genai

# カギの読み込み
api_key = os.environ.get("GEMINI_API_KEY")
print(f"Key exists: {api_key is not None}") # カギがあるか確認

if api_key:
    genai.configure(api_key=api_key)
    try:
        # 接続テスト：利用可能なAIの名前をリストアップする
        print("Testing connection...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Found Model: {m.name}")
        
        # 1つだけ実行テスト
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        print("AI Response Success!")
    except Exception as e:
        print(f"Fatal Error: {e}")
else:
    print("Error: GEMINI_API_KEY is empty!")
