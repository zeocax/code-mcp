#!/usr/bin/env python3
"""Test script to simulate the audit status update"""

import sys
from pathlib import Path
import tempfile
import asyncio

sys.path.insert(0, str(Path(__file__).parent))

from handlers.ai_handler import handle_audit_architecture_consistency

async def test_audit_status():
    """Test audit status update through the handler"""
    print("=== Testing Audit Status Update ===\n")
    
    # Create temporary test files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as old_file:
        old_file.write("def hello():\n    print('Hello, world!')\n")
        old_path = old_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as new_file:
        new_file.write("def hello():\n    print('Hello, world!')\n")
        new_path = new_file.name
    
    print(f"Old file: {old_path}")
    print(f"New file: {new_path}\n")
    
    # Call the handler
    try:
        result = await handle_audit_architecture_consistency({
            'old_file': old_path,
            'new_file': new_path
        })
        print(f"Handler result: {result[0].text}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        Path(old_path).unlink(missing_ok=True)
        Path(new_path).unlink(missing_ok=True)

if __name__ == "__main__":
    asyncio.run(test_audit_status())