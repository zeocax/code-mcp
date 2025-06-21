#!/usr/bin/env python3
"""Test LLM connectivity and functionality"""

import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.ai_config import ai_config
from core.ai_service import ai_service


def print_config():
    """Print current AI configuration"""
    print("=== AI Configuration ===")
    print(f"Provider: {ai_config.provider}")
    print(f"Model: {ai_config.model}")
    print(f"Temperature: {ai_config.temperature}")
    print(f"Max Tokens: {ai_config.max_tokens if ai_config.max_tokens else 'Not set (using model default)'}")
    
    # Check if using a thinking model
    thinking_models = ['o1', 'o1-preview', 'o1-mini', 'claude-3-opus', 'claude-3.5-sonnet']
    if any(model in ai_config.model.lower() for model in thinking_models):
        print(f"Note: Using thinking model - responses will be processed to extract code")
    
    if ai_config.provider == 'openai':
        print(f"OpenAI API Key: {'Set' if ai_config.openai_api_key else 'Not set'}")
        if ai_config.openai_base_url:
            print(f"OpenAI Base URL: {ai_config.openai_base_url}")
    elif ai_config.provider == 'anthropic':
        print(f"Anthropic API Key: {'Set' if ai_config.anthropic_api_key else 'Not set'}")
    
    # Print proxy settings
    print("\n=== Proxy Configuration ===")
    if ai_config.openai_proxy:
        print(f"OpenAI Proxy: {ai_config.openai_proxy}")
    elif ai_config.https_proxy:
        print(f"HTTPS Proxy: {ai_config.https_proxy}")
    elif ai_config.http_proxy:
        print(f"HTTP Proxy: {ai_config.http_proxy}")
    else:
        print("No proxy configured")
    print()


async def test_simple_prompt():
    """Test simple prompt to verify LLM connectivity"""
    print("=== Testing Simple Prompt ===")
    
    # Create simple test code
    old_code = """
def add(a, b):
    return a + b
"""
    
    new_code = """
def add(x, y):
    # TODO: implement addition
    pass
"""
    
    try:
        print("Sending test prompt to LLM...")
        result = await ai_service.audit_architecture_consistency(old_code, new_code)
        
        print("\n--- LLM Response ---")
        print(result)
        print("--- End Response ---\n")
        
        # Verify the response is valid Python code
        try:
            compile(result, '<string>', 'exec')
            print("✅ Response is valid Python code")
        except SyntaxError:
            print("⚠️  Response may contain non-code content (this is handled automatically)")
        
        print("✅ LLM test successful!")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {str(e)}")
        return False


async def test_proxy_connection():
    """Test LLM connectivity through proxy if configured"""
    print("\n=== Testing Proxy Connection ===")
    
    proxy_configured = ai_config.openai_proxy or ai_config.https_proxy or ai_config.http_proxy
    if not proxy_configured:
        print("ℹ️  No proxy configured, skipping proxy test")
        return True
    
    print(f"Testing connection through proxy...")
    
    # Simple test to verify proxy works
    old_code = "def hello(): return 'world'"
    new_code = "def hello(): pass"
    
    try:
        result = await ai_service.audit_architecture_consistency(old_code, new_code)
        print("✅ Proxy connection successful!")
        return True
    except Exception as e:
        print(f"❌ Proxy connection failed: {str(e)}")
        return False


async def test_code_improvement():
    """Test more complex code improvement scenario"""
    print("\n=== Testing Code Improvement ===")
    
    old_code = """
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def get_history(self):
        return self.history
"""
    
    new_code = """
class Calculator:
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
"""
    
    try:
        print("Testing code improvement capability...")
        result = await ai_service.audit_architecture_consistency(old_code, new_code)
        
        print("\n--- Improved Code ---")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("--- End ---\n")
        
        # Check if history feature was added back
        if "history" in result.lower():
            print("✅ LLM successfully identified and restored missing features!")
        else:
            print("⚠️  LLM response received, but missing features might not be restored")
        
        return True
        
    except Exception as e:
        print(f"❌ Code improvement test failed: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("🧪 LLM Connectivity Test\n")
    
    # Print configuration
    print_config()
    
    # Check if API key is configured
    if ai_config.provider == 'openai' and not ai_config.openai_api_key:
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        return
    elif ai_config.provider == 'anthropic' and not ai_config.anthropic_api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file")
        return
    
    # Run tests
    test_results = []
    
    # Test 1: Simple prompt
    test_results.append(await test_simple_prompt())
    
    # Test 2: Proxy connection (if configured)
    if test_results[0]:  # Only run if first test passed
        test_results.append(await test_proxy_connection())
    
    # Test 3: Code improvement
    if test_results[0]:  # Only run if first test passed
        test_results.append(await test_code_improvement())
    
    # Summary
    print("\n=== Test Summary ===")
    passed = sum(test_results)
    total = len(test_results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! LLM is working correctly.")
    else:
        print("❌ Some tests failed. Please check your configuration.")


if __name__ == "__main__":
    asyncio.run(main())