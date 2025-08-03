# agent/memory/summary_memory.py

from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_models import ChatOpenAI  # ✅ You can continue using this for local models

def build_summary_memory(session_id: str = "default") -> ConversationSummaryBufferMemory:
    """
    Returns a summary buffer memory powered by your local LLaMA3.2 model via Ollama.
    Summarizes long conversations progressively.
    """
    llm = ChatOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        model="llama3.2"
    )

    return ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=1000
    )
