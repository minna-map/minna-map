import os
import google.generativeai as genai

# カギの設定
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print(f"--- Diagnostic Start ---")
print(f"API Key exists: {api_key is not None and len(api_key) > 10}")

try:
    print("Listing ALL available models for this key:")
    models = genai.list_models()
    count = 0
    for m in models:
        print(f"FOUND: {m.name}")
        count += 1
    
    if count == 0:
        print("❌ CRITICAL: This API Key cannot see ANY models. Check account permissions.")
    else:
        print(f"Total {count} models found. Connection is OK.")

except Exception as e:
    print(f"❌ CONNECTION ERROR: {e}")

print(f"--- Diagnostic End ---")
