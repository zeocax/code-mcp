#!/usr/bin/env python3
"""Test script to verify file status functionality"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.project_manager import ProjectManager

def test_file_status():
    """Test file status operations"""
    print("=== Testing File Status Functionality ===\n")
    
    # Initialize project manager
    pm = ProjectManager()
    print(f"Project root: {pm.project_root}")
    print(f"Meta file: {pm.meta_file}")
    print(f"Meta file exists: {pm.meta_file.exists()}\n")
    
    # Test file path
    test_file = "server.py"
    
    # Test 1: Update file status
    print(f"1. Testing update_file_status for {test_file}")
    success = pm.update_file_status(test_file, audited=True)
    print(f"   Result: {success}\n")
    
    # Test 2: Get file status
    print(f"2. Testing get_file_status for {test_file}")
    status = pm.get_file_status(test_file)
    if status:
        print(f"   Status: {status}")
        print(f"   Audited: {status.get('audited')}")
        print(f"   Audited at: {status.get('audited_at')}")
        print(f"   Has hash: {'file_hash' in status}")
        if 'modified_after_audit' in status:
            print(f"   Modified after audit: {status.get('modified_after_audit')}")
    else:
        print(f"   No status found")
    print()
    
    # Test 3: List file status
    print("3. Testing list_file_status")
    table = pm.list_file_status()
    print(table)
    print()
    
    # Test 4: Check meta file content
    print("4. Checking project_meta.json content")
    meta = pm._load_meta()
    print(f"   file_status entries: {len(meta.get('file_status', {}))}")
    for path, status in meta.get('file_status', {}).items():
        print(f"   - {path}: audited={status.get('audited')}")

if __name__ == "__main__":
    test_file_status()