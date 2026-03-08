"""
Multi-Agent Data Analysis System
Main entry point for testing API connection
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

def test_api_connection():
    """Test the Anthropic API connection"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY not found in .env file")
        print("Please add your API key to the .env file")
        return False
    
    print("🔑 API Key found!")
    print(f"Key prefix: {api_key[:8]}...")
    
    try:
        # Initialize client
        client = Anthropic(api_key=api_key)
        
        print("\n🤖 Testing API connection...")
        
        # Make a simple test call
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with just: 'Connection successful!'"
                }
            ]
        )
        
        response_text = message.content[0].text
        
        print(f"✅ API Response: {response_text}")
        print(f"📊 Tokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")
        print("\n🎉 SUCCESS! Your environment is set up correctly.")
        print("You're ready to build the multi-agent system!\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your API key is correct in .env")
        print("2. Verify you have API credits at console.anthropic.com")
        print("3. Check your internet connection")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent Data Analysis System - Connection Test")
    print("=" * 60)
    print()
    
    test_api_connection()