"""
Query Retrieval Node - First node in the RAG pipeline.
Handles query input validation and preparation.
"""

import logging
from src.graph.state import RAGState

logger = logging.getLogger(__name__)


def query_retrieval_node(state: RAGState) -> RAGState:
    """
    First node: Query retrieval and validation.

    This node:
    - Validates the input query
    - Logs the query for tracking
    - Prepares the query for document retrieval

    Args:
        state: Current graph state containing the query

    Returns:
        Updated state with validated query
    """
    logger.info("=" * 60)
    logger.info("🔍 QUERY RETRIEVAL NODE - Processing query")
    logger.info("=" * 60)

    query = state.get("query", "")

    if not query:
        logger.error("❌ Query is empty")
        return {
            **state,
            "response": "Error: Query cannot be empty."
        }

    if not isinstance(query, str):
        logger.error(f"❌ Invalid query type: {type(query)}")
        return {
            **state,
            "response": f"Error: Query must be a string, got {type(query)}."
        }

    query = query.strip()

    if not query:
        logger.error("❌ Query is empty after stripping")
        return {
            **state,
            "response": "Error: Query cannot be empty."
        }

    logger.info(f"✅ Query validated: '{query}'")
    logger.info(f"📏 Query length: {len(query)} characters")

    # Return updated state with validated query
    return {
        **state,
        "query": query,
        "retrieved_documents": [],
        "context": "",
        "response": ""
    }
