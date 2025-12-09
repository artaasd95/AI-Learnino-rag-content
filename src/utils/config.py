import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    
    required_env_vars = ['OPENROUTER_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'openrouter_api_key': os.getenv('OPENROUTER_API_KEY'),
        'model_name': os.getenv('MODEL_NAME', 'deepseek/deepseek-chat'),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'openai/text-embedding-3-small'),
        'qdrant_url': os.getenv('QDRANT_URL', 'http://localhost:6333'),
        'qdrant_collection_name': os.getenv('QDRANT_COLLECTION_NAME', 'shakespeare_collection')
    }