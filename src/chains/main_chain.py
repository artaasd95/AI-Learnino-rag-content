from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_shakespeare_chain():
    prompt_template = PromptTemplate(
        input_variables=["question", "context"],
        template="""You are an expert on Shakespeare's works. Use the provided context from Shakespeare's texts to answer the question accurately and helpfully.

Context from Shakespeare's works:
{context}

Question: {question}

Answer based on the Shakespeare context provided. If the context doesn't contain relevant information, say so but still try to provide a helpful response based on your knowledge of Shakespeare.

Answer:"""
    )
    
    # Use OpenRouter with deepseek v3.2 model
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.3
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)