from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_shakespeare_chain():
    # Define the prompt template
    prompt = ChatPromptTemplate.from_template("""You are an expert on Shakespeare's works. Use the provided context from Shakespeare's texts to answer the question accurately and helpfully.

Context from Shakespeare's works:
{context}

Question: {question}

Answer based on the Shakespeare context provided. If the context doesn't contain relevant information, say so but still try to provide a helpful response based on your knowledge of Shakespeare.

Answer:""")

    # Initialize the model with OpenRouter's base URL using init_chat_model
    model = init_chat_model(
        model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
        model_provider="openai",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.3,
        timeout=30,  # 30 second timeout
        max_retries=2,
        
    )

    # Define output parser
    output_parser = StrOutputParser()

    # Create the modern chain using the | operator
    chain = prompt | model | output_parser

    return chain