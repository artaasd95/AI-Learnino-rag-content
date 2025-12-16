#!/usr/bin/env python3
"""
Test script to check BaseRetriever methods
"""
from langchain_core.retrievers import BaseRetriever
import inspect

print("Checking BaseRetriever methods...")

# Get all methods of BaseRetriever
methods = [method for method in dir(BaseRetriever) if not method.startswith('_')]
print(f"Public methods: {methods}")

# Check if get_relevant_documents exists
if hasattr(BaseRetriever, 'get_relevant_documents'):
    print("get_relevant_documents method exists")
    method = getattr(BaseRetriever, 'get_relevant_documents')
    print(f"Method signature: {inspect.signature(method)}")
else:
    print("get_relevant_documents method NOT found")

# Check abstract methods
abstract_methods = getattr(BaseRetriever, '__abstractmethods__', set())
print(f"Abstract methods: {abstract_methods}")