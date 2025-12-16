"""
State definitions for the RAG graph.

This module contains the state structures used by the LangGraph workflow.
Separated to avoid circular imports.
"""

from typing import TypedDict


class RAGState(TypedDict):
    """
    State structure for the RAG graph.

    Attributes:
        query: The user's query/question
        retrieved_documents: List of retrieved Document objects
        context: Formatted context string from retrieved documents
        response: Final response from the LLM
    """
    query: str
    retrieved_documents: list  # List[Document] - using list for TypedDict compatibility
    context: str
    response: str
