#!/usr/bin/env python3
"""
Simple test to check ShakespeareRetriever initialization
"""
import os
# Set dummy environment variables for testing
os.environ['OPENROUTER_API_KEY'] = 'dummy_key'

try:
    from src.retrieval.shakespeare_retriever import ShakespeareRetriever
    print("Testing ShakespeareRetriever creation...")

    # This should fail gracefully due to dummy API key, but shouldn't crash with field errors
    retriever = ShakespeareRetriever()
    print("ShakespeareRetriever created successfully!")

    # Check if the method exists
    if hasattr(retriever, 'get_relevant_documents'):
        print("get_relevant_documents method is available")
    else:
        print("ERROR: get_relevant_documents method not found")

except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()