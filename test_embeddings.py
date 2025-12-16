#!/usr/bin/env python3
"""
Test script to check if OpenRouter embeddings API is working
"""
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("🔍 Testing OpenRouter embeddings API...")

if not os.getenv('OPENROUTER_API_KEY'):
    print("❌ OPENROUTER_API_KEY not set")
    exit(1)

try:
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    print("📡 Testing embedding generation...")
    test_text = "To be or not to be"
    result = embeddings.embed_query(test_text)
    print(f"✅ Embeddings working! Generated {len(result)} dimensions")

except Exception as e:
    print(f"❌ Embeddings API failed: {str(e)}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. Network connectivity")
    print("3. OpenRouter service issues")