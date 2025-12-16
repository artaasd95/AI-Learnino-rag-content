#!/usr/bin/env python3
"""
Test script to check ShakespeareRetriever
"""
from src.retrieval.shakespeare_retriever import ShakespeareRetriever
import os

# Set a dummy API key for testing (this will fail but won't hang)
os.environ['OPENROUTER_API_KEY'] = 'dummy_key_for_testing'

print("Testing ShakespeareRetriever instantiation...")

try:
    retriever = ShakespeareRetriever()
    print("Retriever created successfully")

    # Check if get_relevant_documents method exists
    if hasattr(retriever, 'get_relevant_documents'):
        print("get_relevant_documents method exists")
    else:
        print("ERROR: get_relevant_documents method NOT found")

    print("Test completed")

except Exception as e:
    print(f"Error creating retriever: {str(e)}")
    import traceback
    traceback.print_exc()