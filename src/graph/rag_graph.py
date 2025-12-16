"""
LangGraph definition for Shakespeare RAG system.

This graph defines the flow:
1. Query Retrieval Node - validates and prepares the query
2. Document Retrieval Node - retrieves relevant documents
3. LLM Invocation Node - generates the final response
"""

import logging
from langgraph.graph import StateGraph, START, END

from src.nodes.query_retrieval_node import query_retrieval_node
from src.nodes.document_retrieval_node import document_retrieval_node
from src.nodes.llm_invocation_node import llm_invocation_node
from .state import RAGState

logger = logging.getLogger(__name__)


def create_rag_graph(retriever):
    """
    Create and compile the RAG graph.

    The graph flow:
    START -> query_retrieval -> document_retrieval -> llm_invocation -> END

    Args:
        retriever: ShakespeareRetriever instance for document retrieval

    Returns:
        Compiled LangGraph application
    """
    logger.info("🔧 Building RAG graph...")

    # Initialize the graph with the state structure
    graph = StateGraph(RAGState)

    # Add nodes to the graph
    logger.info("  📌 Adding query_retrieval node...")
    graph.add_node("query_retrieval", query_retrieval_node)

    logger.info("  📌 Adding document_retrieval node...")
    # Create a wrapper function to pass retriever
    def document_retrieval_wrapper(state: RAGState) -> RAGState:
        return document_retrieval_node(state, retriever)

    graph.add_node("document_retrieval", document_retrieval_wrapper)

    logger.info("  📌 Adding llm_invocation node...")
    graph.add_node("llm_invocation", llm_invocation_node)

    # Define the flow: START -> query_retrieval -> document_retrieval -> llm_invocation -> END
    logger.info("  🔗 Setting up graph edges...")
    graph.add_edge(START, "query_retrieval")
    graph.add_edge("query_retrieval", "document_retrieval")
    graph.add_edge("document_retrieval", "llm_invocation")
    graph.add_edge("llm_invocation", END)

    # Compile the graph
    logger.info("  ✅ Compiling graph...")
    app = graph.compile()

    logger.info("✅ RAG graph built and compiled successfully")

    return app
