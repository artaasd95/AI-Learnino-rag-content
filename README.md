# AI-Learnino RAG Content

[![GitHub Repository](https://img.shields.io/badge/GitHub-artaasd95/AI--Learnino--rag--content-blue)](https://github.com/artaasd95/AI-Learnino-rag-content)

This repository contains educational materials and code implementations for Retrieval-Augmented Generation (RAG) systems, part of the AI Learnino community lectures. The project demonstrates practical RAG implementation using Shakespeare's works as the knowledge base.

## 📚 Overview

This project showcases two approaches to building a RAG system:

1. **Original LangChain Implementation** (`app.py`) - Traditional chain-based approach
2. **LangGraph Implementation** (`app_langgraph.py`) - Modern graph-based workflow using LangGraph

Both implementations use:
- Qdrant vector database for document storage and retrieval
- OpenRouter API for embeddings and LLM inference
- Shakespeare's complete works as the knowledge base

## 🏗️ Architecture

### Original LangChain Architecture

```
Query → ConversationService → Retriever → LLM Chain → Response
       ↓
   ShakespeareRetriever
   (Qdrant Vector Store)
```

### LangGraph Architecture

```
START → Query Retrieval Node → Document Retrieval Node → LLM Invocation Node → END
         ↓                        ↓                        ↓
    Input Validation       Vector Search +          Prompt + LLM
    & Preparation           Context Formatting       Response Generation
```

The LangGraph implementation breaks down the RAG pipeline into three distinct nodes:

1. **Query Retrieval Node** (`src/nodes/query_retrieval_node.py`)
   - Validates and preprocesses user input
   - Ensures query quality and format

2. **Document Retrieval Node** (`src/nodes/document_retrieval_node.py`)
   - Searches Qdrant vector database for relevant Shakespeare text
   - Formats retrieved documents into context for LLM consumption

3. **LLM Invocation Node** (`src/nodes/llm_invocation_node.py`)
   - Constructs prompts with retrieved context
   - Invokes DeepSeek model via OpenRouter API
   - Generates final responses

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Docker (for Qdrant database)
- OpenRouter API key

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/artaasd95/AI-Learnino-rag-content.git
   cd AI-Learnino-rag-content
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenRouter API key
   ```

4. **Start Qdrant database:**
   ```bash
   docker-compose up -d
   ```

## 📖 Usage

### Original LangChain Version

```bash
python app.py
```

### LangGraph Version

```bash
python app_langgraph.py
```

Both applications will:
1. Initialize the Qdrant vector database with Shakespeare texts
2. Set up embeddings and LLM connections
3. Provide an interactive query interface

### Example Queries

- "What is the famous soliloquy from Hamlet?"
- "Describe Romeo and Juliet's first meeting"
- "What themes appear in Macbeth?"
- "Who is Prospero in The Tempest?"

## 📁 Project Structure

```
AI-Learnino-rag-content/
├── app.py                          # Original LangChain implementation
├── app_langgraph.py               # LangGraph implementation
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Qdrant database setup
├── test_*.py                      # Various test scripts
├── data/
│   └── folger-shakespeares/       # Shakespeare text files
├── src/
│   ├── graph/                     # LangGraph implementation
│   │   ├── __init__.py
│   │   ├── rag_graph.py          # Graph definition and workflow
│   │   └── state.py              # State structure definitions
│   ├── nodes/                     # Individual graph nodes
│   │   ├── __init__.py
│   │   ├── query_retrieval_node.py    # Query validation
│   │   ├── document_retrieval_node.py # Vector search
│   │   └── llm_invocation_node.py     # LLM generation
│   ├── chains/                    # Original LangChain chains
│   ├── retrieval/                 # Retrievers and embeddings
│   ├── services/                  # Service layer
│   └── utils/                     # Utilities and config
├── lecture-materials/             # Presentation slides
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key (required) | - |
| `MODEL_NAME` | LLM model to use | `deepseek/deepseek-chat` |
| `EMBEDDING_MODEL` | Embedding model | `openai/text-embedding-3-small` |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `QDRANT_COLLECTION_NAME` | Qdrant collection name | `shakespeare_collection` |

### Model Configuration

- **LLM**: DeepSeek Chat via OpenRouter API
- **Embeddings**: OpenAI text-embedding-3-small via OpenRouter
- **Vector Store**: Qdrant with cosine similarity
- **Chunk Size**: 1000 characters with 200 character overlap

## 🎯 Key Features

### LangGraph Advantages

- **Modular Design**: Each step is a separate, testable node
- **State Management**: Explicit state passing between nodes
- **Observability**: Detailed logging at each pipeline stage
- **Flexibility**: Easy to modify or extend individual components
- **Error Handling**: Granular error handling per node

### RAG Pipeline Features

- **Intelligent Retrieval**: Semantic search using vector embeddings
- **Context-Aware Responses**: LLM responses grounded in Shakespeare texts
- **Comprehensive Coverage**: All major Shakespeare works included
- **Source Attribution**: Responses include source work references

## 🧪 Testing

The repository includes various test scripts:

- `test_api_key.py` - API key validation
- `test_embeddings.py` - Embedding functionality
- `test_qdrant.py` - Vector database operations
- `test_retriever.py` - Document retrieval testing
- `test_shakespeare_retriever.py` - Shakespeare-specific retrieval

Run tests with:
```bash
python test_*.py
```

## 📚 Educational Materials

- **Presentation Slides**: `lecture-materials/RAG_Presentation.pptx`
- **Additional Resources**: `lecture-materials/retrieval_augmented_generation.pptx`

## 🤝 Contributing

This is an educational repository for the AI Learnino community. Contributions and improvements are welcome!

## 📄 License

See LICENSE file for details.

## 🔗 Links

- **GitHub Repository**: https://github.com/artaasd95/AI-Learnino-rag-content
- **AI Learnino Community**: Educational materials for AI learning
- **LangGraph Documentation**: https://docs.langchain.com/oss/python/langgraph/
- **LangChain Documentation**: https://python.langchain.com/

---

*Part of the AI Learnino community educational materials on Retrieval-Augmented Generation systems.*