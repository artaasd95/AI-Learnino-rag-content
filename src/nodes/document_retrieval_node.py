"""
Document Retrieval Node - Second node in the RAG pipeline.
Retrieves relevant documents from the vector store.
"""

import logging
from src.graph.state import RAGState

logger = logging.getLogger(__name__)


def document_retrieval_node(state: RAGState, retriever) -> RAGState:
    """
    Second node: Document retrieval from vector store.

    This node:
    - Takes the validated query from previous node
    - Retrieves relevant documents using the retriever
    - Formats the context for LLM consumption
    - Logs retrieval details

    Args:
        state: Current graph state containing the query
        retriever: ShakespeareRetriever instance for document retrieval

    Returns:
        Updated state with retrieved documents and formatted context
    """
    logger.info("=" * 60)
    logger.info("📚 DOCUMENT RETRIEVAL NODE - Retrieving documents")
    logger.info("=" * 60)

    query = state.get("query", "")

    if not query:
        logger.error("❌ No query found in state")
        return {
            **state,
            "response": "Error: No query available for retrieval."
        }

    try:
        logger.info(f"🔍 Searching for documents related to: '{query}'")

        # Retrieve relevant documents
        documents = retriever._get_relevant_documents(query)
        logger.info(f"✅ Retrieved {len(documents)} documents")

        if not documents:
            logger.warning("⚠️ No documents retrieved")
            return {
                **state,
                "retrieved_documents": [],
                "context": "No relevant Shakespeare text found."
            }

        # Log details of retrieved documents
        for i, doc in enumerate(documents[:5]):  # Log top 5
            logger.info(f"📄 Document {i+1}:")
            logger.info(f"   Source: {doc.metadata.get('source', 'Unknown')}")
            logger.info(f"   Chunk Index: {doc.metadata.get('chunk_index', 'Unknown')}")
            logger.info(f"   Content Preview: {doc.page_content[:200]}...")
            logger.info(f"   Full Content Length: {len(doc.page_content)} characters")

        # Format context from retrieved documents
        context_parts = []
        for doc in documents[:3]:  # Use top 3 documents for context
            context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}")
            context_parts.append(f"Content: {doc.page_content[:500]}...")
            context_parts.append("---")

        formatted_context = "\n".join(context_parts)

        logger.info(f"📝 Formatted context length: {len(formatted_context)} characters")
        logger.info(f"📝 Context preview: {formatted_context[:300]}...")

        return {
            **state,
            "retrieved_documents": documents,
            "context": formatted_context
        }

    except Exception as e:
        logger.error(f"❌ Error in document retrieval: {str(e)}", exc_info=True)
        return {
            **state,
            "retrieved_documents": [],
            "context": f"Error retrieving context: {str(e)}"
        }
