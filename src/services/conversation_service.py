from langchain_core.retrievers import BaseRetriever
from langchain_core.chains import Chain

class ConversationService:
    def __init__(self, chain: Chain, retriever: BaseRetriever):
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
            retrieved_context = self._retrieve_relevant_context(query)
            
            response = self.chain.run({
                'question': query,
                'context': retrieved_context
            })
                
            return response
            
        except Exception as e:
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
            documents = self.retriever.get_relevant_documents(query)
            if not documents:
                return "No relevant Shakespeare text found."
            
            context_parts = []
            for doc in documents[:3]:
                context_parts.append(f"Source: {doc.metadata.get('source', 'Unknown')}")
                context_parts.append(f"Content: {doc.page_content[:500]}...")
                context_parts.append("---")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Error retrieving context: {str(e)}"