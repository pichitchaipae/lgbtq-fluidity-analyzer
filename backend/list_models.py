"""List available Gemini models"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("\n🔍 Available Gemini Models:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  ✓ {model.name}")
        print(f"    Display: {model.display_name}")
        print(f"    Description: {model.description}")
        print()
