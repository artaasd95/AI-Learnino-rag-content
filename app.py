from src.services.conversation_service import ConversationService
from src.retrieval.shakespeare_retriever import ShakespeareRetriever
from src.chains.main_chain import create_shakespeare_chain
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    print("=" * 60)
    print("Shakespeare RAG System - Qdrant + OpenRouter")
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
    print("  - Initializing language model (DeepSeek)...")
    
    try:
        # Initialize retriever (this will connect to Qdrant and load/create collection)
        retriever = ShakespeareRetriever()
        print("  ✓ Qdrant connection established")
        
        # Create the chain
        chain = create_shakespeare_chain()
        print("  ✓ Language model ready")
        
        # Create conversation service
        conversation_service = ConversationService(chain, retriever)
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
            
            print("\n💭 Processing your query...")
            response = conversation_service.process_query(query)
            print(f"\n📖 Answer:\n{response}")
            
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        print("\nPlease check:")
        print("  1. Qdrant is running (docker-compose up -d)")
        print("  2. OPENROUTER_API_KEY is set in .env file")
        print("  3. All dependencies are installed (pip install -r requirements.txt)")

if __name__ == "__main__":
    main()