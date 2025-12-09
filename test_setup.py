#!/usr/bin/env python3
"""
Test script to verify the Shakespeare RAG system structure is set up correctly.
"""

import os
import sys

def test_structure():
    print("Testing project structure...")
    
    required_dirs = [
        'src',
        'src/chains',
        'src/services', 
        'src/retrieval',
        'src/utils',
        'data/folger-shakespeares'
    ]
    
    required_files = [
        'src/chains/main_chain.py',
        'src/services/conversation_service.py',
        'src/retrieval/shakespeare_retriever.py',
        'src/utils/config.py',
        'requirements.txt',
        '.env.example',
        'app.py'
    ]
    
    print("\nChecking directories:")
    all_dirs_ok = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} (MISSING)")
            all_dirs_ok = False
    
    print("\nChecking files:")
    all_files_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (MISSING)")
            all_files_ok = False
    
    print("\nChecking data files:")
    data_files = os.listdir('data/folger-shakespeares')
    print(f"Found {len(data_files)} Shakespeare text files")
    
    if len(data_files) > 0:
        print(f"✓ Data directory contains {len(data_files)} files")
    else:
        print("✗ No data files found")
        all_files_ok = False
    
    print(f"\n{'='*50}")
    if all_dirs_ok and all_files_ok:
        print("✓ Project structure is set up correctly!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OPENAI_API_KEY to .env")
        print("3. Run: pip install -r requirements.txt")
        print("4. Run: python app.py")
        return True
    else:
        print("✗ Project structure has issues")
        return False

if __name__ == "__main__":
    success = test_structure()
    sys.exit(0 if success else 1)