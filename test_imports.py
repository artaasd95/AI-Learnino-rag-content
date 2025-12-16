#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly and there are no circular import issues.
"""

try:
    print("Testing imports...")
    from src.graph.state import RAGState
    print("✓ RAGState import successful")

    from src.nodes.query_retrieval_node import query_retrieval_node
    print("✓ query_retrieval_node import successful")

    from src.nodes.document_retrieval_node import document_retrieval_node
    print("✓ document_retrieval_node import successful")

    from src.nodes.llm_invocation_node import llm_invocation_node
    print("✓ llm_invocation_node import successful")

    # Check if langgraph is available
    try:
        from src.graph.rag_graph import create_rag_graph
        print("✓ create_rag_graph import successful")
    except ImportError as langgraph_error:
        if "langgraph" in str(langgraph_error):
            print("! create_rag_graph import skipped - langgraph not installed")
            print("  Install with: pip install langgraph")
        else:
            raise langgraph_error

    print("\n[SUCCESS] All imports successful! Circular import issue resolved.")

except ImportError as e:
    print(f"\n[ERROR] Import error: {e}")
    exit(1)
except Exception as e:
    print(f"\n[ERROR] Unexpected error: {e}")
    exit(1)