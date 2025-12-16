from langchain_core.runnables import Runnable
from src.retrieval.shakespeare_retriever import ShakespeareRetriever
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self, chain: Runnable, retriever: ShakespeareRetriever):
        self.chain = chain
        self.retriever = retriever
    
    def process_query(self, query: str) -> str:
        """
        Process a single query about Shakespeare's works.

        Args:
            query: A question or query about Shakespeare (e.g., play name, character, quote)

        Returns:
            Response based on retrieved context from Shakespeare's works
        """
        try:
            logger.info("📚 Retrieving context...")
            retrieved_context = self._retrieve_relevant_context(query)
            logger.info(f"📄 Context retrieved ({len(retrieved_context)} chars)")

            logger.info("🤖 Calling language model...")

            # Prepare the prompt input
            prompt_input = {
                'question': query,
                'context': retrieved_context
            }

            # Log the prompt being sent to LLM
            logger.info("📝 Prompt being sent to LLM:")
            logger.info(f"   Question: {prompt_input['question']}")
            logger.info(f"   Context Length: {len(prompt_input['context'])} characters")
            logger.info(f"   Context Preview: {prompt_input['context'][:300]}...")

            response = self.chain.invoke(prompt_input)
            logger.info("✅ Response generated")

            return response

        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return f"Error processing query: {str(e)}"
    
    def _retrieve_relevant_context(self, query: str) -> str:
        """
        Retrieve relevant context from Shakespeare's works based on the query.

        Args:
            query: The search query

        Returns:
            Formatted context string with relevant passages
        """
        try:
            logger.info("🔍 Calling retriever.get_relevant_documents...")
            documents = self.retriever._get_relevant_documents(query)
            logger.info(f"📑 Retrieved {len(documents)} documents")

            if not documents:
                return "No relevant Shakespeare text found."

            context_parts = []
            for doc in documents[:3]:
                context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}")
                context_parts.append(f"Content: {doc.page_content[:500]}...")
                context_parts.append("---")

            return "\n".join(context_parts)

        except Exception as e:
            logger.error(f"❌ Error in _retrieve_relevant_context: {str(e)}")
            return f"Error retrieving context: {str(e)}"