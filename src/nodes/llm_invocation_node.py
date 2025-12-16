"""
LLM Invocation Node - Third node in the RAG pipeline.
Invokes the language model to generate a response.
"""

import logging
from src.graph.state import RAGState
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

logger = logging.getLogger(__name__)


def create_llm_chain():
    """
    Create the LLM chain for generating responses.

    Returns:
        Compiled chain: prompt | model | output_parser
    """
    # Define the prompt template
    prompt = ChatPromptTemplate.from_template("""You are an expert on Shakespeare's works. Use the provided context from Shakespeare's texts to answer the question accurately and helpfully.

Context from Shakespeare's works:
{context}

Question: {question}

Answer based on the Shakespeare context provided. If the context doesn't contain relevant information, say so but still try to provide a helpful response based on your knowledge of Shakespeare.

if the context is found in the data, after explanation write the main context that is found in the data.

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

    # Create the chain using the | operator
    chain = prompt | model | output_parser

    return chain


# Initialize chain once at module level
_llm_chain = None


def get_llm_chain():
    """Get or create the LLM chain (singleton pattern)."""
    global _llm_chain
    if _llm_chain is None:
        logger.info("🔧 Initializing LLM chain...")
        _llm_chain = create_llm_chain()
        logger.info("✅ LLM chain initialized")
    return _llm_chain


def llm_invocation_node(state: RAGState) -> RAGState:
    """
    Third node: LLM invocation to generate response.

    This node:
    - Takes the query and context from previous nodes
    - Invokes the LLM chain to generate a response
    - Logs the prompt and response details

    Args:
        state: Current graph state containing query and context

    Returns:
        Updated state with LLM response
    """
    logger.info("=" * 60)
    logger.info("🤖 LLM INVOCATION NODE - Generating response")
    logger.info("=" * 60)

    query = state.get("query", "")
    context = state.get("context", "")

    if not query:
        logger.error("❌ No query found in state")
        return {
            **state,
            "response": "Error: No query available for LLM processing."
        }

    if not context:
        logger.warning("⚠️ No context available, LLM will rely on its knowledge")

    try:
        # Get the LLM chain
        chain = get_llm_chain()

        # Prepare the prompt input
        prompt_input = {
            'question': query,
            'context': context
        }

        # Log the prompt being sent to LLM
        logger.info("📝 Prompt being sent to LLM:")
        logger.info(f"   Question: {prompt_input['question']}")
        logger.info(f"   Context Length: {len(prompt_input['context'])} characters")
        logger.info(f"   Context Preview: {prompt_input['context'][:300]}...")

        logger.info("🔄 Invoking LLM chain...")
        response = chain.invoke(prompt_input)

        logger.info("✅ Response generated successfully")
        logger.info(f"📏 Response length: {len(response)} characters")
        logger.info(f"📄 Response preview: {response[:200]}...")

        return {
            **state,
            "response": response
        }

    except Exception as e:
        logger.error(f"❌ Error in LLM invocation: {str(e)}", exc_info=True)
        return {
            **state,
            "response": f"Error generating response: {str(e)}"
        }
