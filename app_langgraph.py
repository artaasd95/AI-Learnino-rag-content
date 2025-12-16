"""
Shakespeare RAG System using LangGraph.

This is the new LangGraph-based version of the application.
The original app.py remains unchanged for reference.
"""

from src.graph.rag_graph import create_rag_graph
from src.retrieval.shakespeare_retriever import ShakespeareRetriever
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()


def main():
    """
    Main entry point for the LangGraph-based Shakespeare RAG system.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)

    print("=" * 60)
    print("Shakespeare RAG System - LangGraph + Qdrant + OpenRouter")
    print("=" * 60)
    
    # Check for required environment variable
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n❌ ERROR: OPENROUTER_API_KEY not found in environment variables!")
        print("Please create a .env file with your OpenRouter API key.")
        print("See .env.example for reference.")
        return
    
    print("\n📚 Initializing components...")
    print("  - Loading Qdrant vector database...")
    print("  - Setting up embeddings (OpenRouter)...")
    print("  - Building LangGraph workflow...")
    print("  - Initializing language model (DeepSeek)...")
    
    try:
        # Initialize retriever (this will connect to Qdrant and load/create collection)
        logger.info("Initializing ShakespeareRetriever...")
        retriever = ShakespeareRetriever()
        print("  ✓ Qdrant connection established")
        
        # Create the LangGraph application
        logger.info("Creating RAG graph...")
        graph_app = create_rag_graph(retriever)
        print("  ✓ LangGraph workflow ready")
        print("  ✓ Language model ready")
        print("  ✓ All components initialized\n")
        
        print("=" * 60)
        print("System ready! Ask questions about Shakespeare's works.")
        print("Type 'quit' or 'exit' to stop.")
        print("=" * 60)
        
        # Simple query loop
        while True:
            print("\n" + "-" * 60)
            query = input("🔍 Your question: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            print("\n💭 Processing your query through LangGraph...")
            
            try:
                # Prepare initial state
                initial_state = {
                    "query": query,
                    "retrieved_documents": [],
                    "context": "",
                    "response": ""
                }
                
                # Invoke the graph
                logger.info(f"Invoking graph with query: '{query}'")
                result = graph_app.invoke(initial_state)
                
                # Extract and display the response
                response = result.get("response", "No response generated")
                print(f"\n📖 Answer:\n{response}")
                
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}", exc_info=True)
                print(f"\n❌ Error processing query: {str(e)}")
                print("Please check the logs for more details.")
            
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}", exc_info=True)
        print(f"\n❌ Error during initialization: {str(e)}")
        print("\nPlease check:")
        print("  1. Qdrant is running (docker-compose up -d)")
        print("  2. OPENROUTER_API_KEY is set in .env file")
        print("  3. All dependencies are installed (pip install -r requirements.txt)")
        print("  4. LangGraph is installed (pip install langgraph)")


if __name__ == "__main__":
    main()
