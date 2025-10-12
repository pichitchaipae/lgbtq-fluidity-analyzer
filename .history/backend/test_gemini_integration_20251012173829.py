"""
Test script for Gemini AI integration
Tests the complete flow: API endpoint → Gemini service → response
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.gemini_interpreter import GeminiInterpreter
from app.core.config import get_settings

settings = get_settings()

async def test_gemini_service():
    """Test Gemini service directly"""
    print("\n" + "="*60)
    print("🧪 TESTING GEMINI AI SERVICE")
    print("="*60)
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"   AI Provider: {settings.ai_provider}")
    print(f"   Gemini API Key: {'✅ Configured' if settings.gemini_api_key else '❌ Missing'}")
    
    if not settings.gemini_api_key:
        print("\n❌ ERROR: GEMINI_API_KEY not configured in .env")
        return False
    
    # Initialize Gemini interpreter
    try:
        interpreter = GeminiInterpreter()
        print(f"\n✅ GeminiInterpreter initialized successfully")
    except Exception as e:
        print(f"\n❌ Failed to initialize GeminiInterpreter: {e}")
        return False
    
    # Test data: Sample ANOVA results
    test_data = {
        "sexual_orientation": {
            "F": 12.45,
            "p": 0.001,
            "eta_squared": 0.34,
            "df_between": 2,
            "df_within": 97
        },
        "gender_identity": {
            "F": 8.32,
            "p": 0.015,
            "eta_squared": 0.21,
            "df_between": 3,
            "df_within": 96
        },
        "attraction_patterns": {
            "F": 15.78,
            "p": 0.0001,
            "eta_squared": 0.42,
            "df_between": 4,
            "df_within": 95
        }
    }
    
    print(f"\n📊 Test Data:")
    print(f"   Testing {len(test_data)} ANOVA results")
    print(f"   Variables: {', '.join(test_data.keys())}")
    
    # Test interpretation
    print(f"\n🤖 Requesting Gemini interpretation...")
    print(f"   (This may take 2-5 seconds...)")
    
    try:
        interpretation = await interpreter.get_interpretation(test_data)
        
        print(f"\n✅ SUCCESS! Gemini returned interpretation")
        print(f"\n" + "-"*60)
        print(f"📝 INTERPRETATION:")
        print(f"-"*60)
        print(interpretation)
        print(f"-"*60)
        
        # Validate response
        if len(interpretation) > 100:
            print(f"\n✅ Response length: {len(interpretation)} characters (Good!)")
        else:
            print(f"\n⚠️  Response length: {len(interpretation)} characters (Short)")
        
        if "sexual orientation" in interpretation.lower() or "gender identity" in interpretation.lower():
            print(f"✅ Response contains relevant terms")
        else:
            print(f"⚠️  Response may not be relevant")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during interpretation: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

async def test_api_endpoint():
    """Test the full API endpoint"""
    print("\n" + "="*60)
    print("🌐 TESTING API ENDPOINT")
    print("="*60)
    
    try:
        import httpx
        
        url = "http://localhost:8000/api/v2/analysis"
        
        # Sample request payload
        payload = {
            "responses": [
                {"question_id": 1, "value": 3},
                {"question_id": 2, "value": 4},
                {"question_id": 3, "value": 2},
                {"question_id": 4, "value": 5},
                {"question_id": 5, "value": 3}
            ],
            "use_ai": True,
            "user_language": "th"
        }
        
        print(f"\n📤 Sending POST request to: {url}")
        print(f"   AI Mode: Enabled")
        print(f"   Language: Thai")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ API Response: 200 OK")
                print(f"\n📊 Response contains:")
                print(f"   - ANOVA Results: {'✅' if 'anova_results' in data else '❌'}")
                print(f"   - AI Interpretation: {'✅' if 'ai_interpretation' in data else '❌'}")
                print(f"   - Privacy Notice: {'✅' if 'privacy_notice' in data else '❌'}")
                
                if 'ai_interpretation' in data:
                    interp = data['ai_interpretation']
                    print(f"\n📝 AI Interpretation Preview:")
                    print(f"   {interp[:200]}...")
                
                return True
            else:
                print(f"\n❌ API Error: {response.status_code}")
                print(f"   {response.text}")
                return False
                
    except ImportError:
        print(f"\n⚠️  httpx not installed, skipping API endpoint test")
        print(f"   Install with: pip install httpx")
        return None
    except Exception as e:
        print(f"\n❌ API Test Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 GEMINI AI INTEGRATION TEST SUITE")
    print("="*60)
    print(f"   Date: 2025-10-12")
    print(f"   Model: gemini-1.5-flash")
    print(f"   Provider: Google Gemini")
    
    results = []
    
    # Test 1: Gemini Service
    service_ok = await test_gemini_service()
    results.append(("Gemini Service", service_ok))
    
    # Test 2: API Endpoint (if backend is running)
    api_ok = await test_api_endpoint()
    if api_ok is not None:
        results.append(("API Endpoint", api_ok))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✨ Next Steps:")
        print("   1. Test in frontend: http://localhost:5173")
        print("   2. Complete survey and click 'Advanced Analysis'")
        print("   3. Select 'AI Mode' and verify Gemini interpretation")
    else:
        print("\n⚠️  SOME TESTS FAILED - Check errors above")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
