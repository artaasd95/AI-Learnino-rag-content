from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from pydantic import Field
import os
from typing import List, Optional, Any
import glob

# Load environment variables from .env file
load_dotenv()

class ShakespeareRetriever(BaseRetriever):
    embeddings: Optional[OpenAIEmbeddings] = Field(default=None, description="OpenAI embeddings for vectorization")
    qdrant_url: str = Field(default="http://localhost:6333", description="Qdrant server URL")
    collection_name: str = Field(default="shakespeare_collection", description="Qdrant collection name")
    vectorstore: Optional[QdrantVectorStore] = Field(default=None, description="Qdrant vector store for document retrieval")
    def __init__(self):
        # Initialize OpenRouter embeddings (compatible with OpenAI API)
        embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small"),
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "shakespeare_collection")

        super().__init__(
            embeddings=embeddings,
            qdrant_url=qdrant_url,
            collection_name=collection_name
        )

        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "folger-shakespeares", "*.txt")
        text_files = glob.glob(data_path)
        
        if not text_files:
            raise ValueError("No Shakespeare text files found in data directory")
        
        documents = []
        for file_path in text_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            play_name = os.path.basename(file_path).replace("_TXT_FolgerShakespeare.txt", "").replace("-", " ").title()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            chunks = text_splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                documents.append(Document(
                    page_content=chunk,
                    metadata={
                        "source": play_name,
                        "chunk_index": i,
                        "file_path": file_path
                    }
                ))
        
        # Initialize Qdrant client
        qdrant_client = QdrantClient(url=self.qdrant_url)
        
        # Check if collection exists, if not create it
        try:
            collections = qdrant_client.get_collections().collections
            collection_exists = any(col.name == self.collection_name for col in collections)
            
            if collection_exists:
                # Load existing collection
                self.vectorstore = QdrantVectorStore(
                    client=qdrant_client,
                    collection_name=self.collection_name,
                    embedding=self.embeddings
                )
            else:
                # Create new collection from documents
                self.vectorstore = QdrantVectorStore.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    url=self.qdrant_url,
                    collection_name=self.collection_name
                )
        except Exception as e:
            # If there's an error, try creating from documents
            self.vectorstore = QdrantVectorStore.from_documents(
                documents=documents,
                embedding=self.embeddings,
                url=self.qdrant_url,
                collection_name=self.collection_name
            )
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
        **kwargs: Any
    ) -> List[Document]:
        print(f"🔍 Searching for: '{query}'")
        if not self.vectorstore:
            print("❌ Vectorstore not initialized")
            return []

        try:
            print("📡 Calling similarity_search...")
            results = self.vectorstore.similarity_search(query, k=5)
            print(f"✅ Found {len(results)} documents")
            return results
        except Exception as e:
            print(f"❌ Error in similarity search: {str(e)}")
            return []

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
        **kwargs: Any
    ) -> List[Document]:
        return self._get_relevant_documents(query, run_manager=run_manager, **kwargs)