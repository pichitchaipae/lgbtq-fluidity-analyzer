"""
Simple manual test for Gemini AI integration
Run this to quickly verify Gemini is working
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\n" + "="*60)
print("🧪 SIMPLE GEMINI TEST")
print("="*60)

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
print(f"\n1️⃣ Checking GEMINI_API_KEY...")
if api_key:
    print(f"   ✅ Found: {api_key[:20]}...{api_key[-4:]}")
else:
    print(f"   ❌ Not found in environment")
    exit(1)

# Try to import and initialize
print(f"\n2️⃣ Importing Gemini SDK...")
try:
    import google.generativeai as genai
    print(f"   ✅ google.generativeai imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import: {e}")
    print(f"   Run: pip install google-generativeai")
    exit(1)

# Configure Gemini
print(f"\n3️⃣ Configuring Gemini...")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print(f"   ✅ Gemini 2.5 Flash model initialized")
except Exception as e:
    print(f"   ❌ Configuration failed: {e}")
    exit(1)

# Test a simple prompt
print(f"\n4️⃣ Testing Gemini with a simple prompt...")
try:
    response = model.generate_content("Say 'Hello from Gemini!' in both Thai and English.")
    print(f"   ✅ Gemini responded!")
    print(f"\n   Response:")
    print(f"   {'-'*56}")
    print(f"   {response.text}")
    print(f"   {'-'*56}")
except Exception as e:
    print(f"   ❌ Generation failed: {e}")
    exit(1)

# Test with statistical data
print(f"\n5️⃣ Testing with statistical interpretation...")
test_data = {
    "sexual_orientation": {
        "F": 12.45,
        "p": 0.001,
        "eta_squared": 0.34
    }
}

prompt = f"""Analyze these statistical results and provide a brief interpretation in both Thai and English:

{json.dumps(test_data, indent=2)}

Provide a short, clear interpretation suitable for research participants."""

try:
    response = model.generate_content(prompt)
    print(f"   ✅ Statistical interpretation generated!")
    print(f"\n   Response:")
    print(f"   {'-'*56}")
    print(f"   {response.text}")
    print(f"   {'-'*56}")
except Exception as e:
    print(f"   ❌ Generation failed: {e}")
    exit(1)

print(f"\n" + "="*60)
print("🎉 ALL TESTS PASSED!")
print("="*60)
print(f"\n✨ Gemini AI is working correctly!")
print(f"\nNext steps:")
print(f"  • Start backend: cd backend && python -m uvicorn app.main:app --reload")
print(f"  • Test in frontend: http://localhost:5173")
print(f"  • Complete survey → Advanced Analysis → AI Mode")
print(f"\n" + "="*60 + "\n")
