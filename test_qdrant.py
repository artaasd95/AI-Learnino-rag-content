#!/usr/bin/env python3
"""
Test script to check if Qdrant is running
"""
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

print(f"🔍 Checking Qdrant connection at {qdrant_url}...")

try:
    client = QdrantClient(url=qdrant_url)
    collections = client.get_collections()
    print(f"✅ Qdrant is running! Found {len(collections.collections)} collections")
    for col in collections.collections:
        print(f"  - {col.name}")
except Exception as e:
    print(f"❌ Qdrant connection failed: {str(e)}")
    print("\nMake sure Qdrant is running:")
    print("docker-compose up -d")