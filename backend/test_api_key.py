#!/usr/bin/env python3
"""
Test script to verify Google API key functionality
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    
    # Configure API
    api_key = os.getenv('GOOGLE_API_KEY')
    print(f"🔑 API Key loaded: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test API call
        test_question = "What is 2+2?"
        response = model.generate_content(test_question)
        
        print("✅ Google API Test Successful!")
        print(f"Question: {test_question}")
        print(f"Response: {response.text}")
        print("\n🚀 Your API key is working correctly!")
        
    else:
        print("❌ No API key found in environment variables")
        
except ImportError:
    print("❌ Google AI library not available")
except Exception as e:
    print(f"❌ API Test Failed: {e}")
    if "API_KEY" in str(e):
        print("🔧 Fix: Check if your API key is valid and has proper permissions")
    elif "quota" in str(e).lower():
        print("🔧 Fix: API quota exceeded, try again later")
    elif "authentication" in str(e).lower():
        print("🔧 Fix: Authentication failed, verify your API key")
