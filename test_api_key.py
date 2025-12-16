#!/usr/bin/env python3
"""
Test script to check if environment variables are properly set
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Checking environment variables...")
print(f"OPENROUTER_API_KEY: {'✓ Set' if os.getenv('OPENROUTER_API_KEY') else '❌ Not set'}")
print(f"QDRANT_URL: {os.getenv('QDRANT_URL', 'http://localhost:6333')}")
print(f"COLLECTION_NAME: {os.getenv('QDRANT_COLLECTION_NAME', 'shakespeare_collection')}")
print(f"MODEL_NAME: {os.getenv('MODEL_NAME', 'deepseek/deepseek-chat')}")

if not os.getenv('OPENROUTER_API_KEY'):
    print("\n❌ OPENROUTER_API_KEY is required!")
    print("Create a .env file with your OpenRouter API key:")
    print("OPENROUTER_API_KEY=your_api_key_here")
    exit(1)

print("\n✅ Environment variables look good!")