from langchain_core.runnables import Runnable
from src.retrieval.shakespeare_retriever import ShakespeareRetriever

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
            print("📚 Retrieving context...")
            retrieved_context = self._retrieve_relevant_context(query)
            print(f"📄 Context retrieved ({len(retrieved_context)} chars)")

            print("🤖 Calling language model...")
            response = self.chain.invoke({
                'question': query,
                'context': retrieved_context
            })
            print("✅ Response generated")

            return response

        except Exception as e:
            print(f"❌ Error: {str(e)}")
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
            print("🔍 Calling retriever.get_relevant_documents...")
            documents = self.retriever._get_relevant_documents(query)
            print(f"📑 Retrieved {len(documents)} documents")

            if not documents:
                return "No relevant Shakespeare text found."

            context_parts = []
            for doc in documents[:3]:
                context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}")
                context_parts.append(f"Content: {doc.page_content[:500]}...")
                context_parts.append("---")

            return "\n".join(context_parts)

        except Exception as e:
            print(f"❌ Error in _retrieve_relevant_context: {str(e)}")
            return f"Error retrieving context: {str(e)}"