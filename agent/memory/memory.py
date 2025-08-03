# agent/memory/memory.py

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage
from agent.memory.json_memory import JSONMessageHistory


def build_memory(session_id: str = "default") -> ConversationBufferMemory:
    """
    Builds conversation memory for a specific session using JSON-based message history.
    This enables persistence across restarts.
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=JSONMessageHistory(session_id=session_id)
    )


def extract_persona(memory: ConversationBufferMemory) -> dict:
    """
    Parses stored memory to extract persona context (if previously set).
    Looks for system messages with 'User persona set:'.
    """
    persona = {}
    for msg in memory.chat_memory.messages:
        if isinstance(msg, BaseMessage) and getattr(msg, "type", "") == "system":
            if isinstance(msg.content, str) and "User persona set:" in msg.content:
                parts = msg.content.split(":")[1].strip().split(", ")
                for item in parts:
                    if "=" in item:
                        key, val = item.split("=")
                        persona[key.strip()] = float(val) if "." in val or val.isdigit() else val
    return persona
