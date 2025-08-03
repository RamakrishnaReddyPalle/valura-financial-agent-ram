# agent/builder.py

from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from agent.tools import get_all_tools
from agent.memory.json_memory import JSONMessageHistory
from langchain_core.tools import tool

@tool
def respond_naturally_tool(input: str) -> str:
    """Fallback response for general conversation or small talk."""
    return f"I'm here to assist with financial planning, but happy to chat! You said: '{input}'"

def build_agent(session_id: str = "default"):
    base_tools = get_all_tools() + [respond_naturally_tool]

    wrapped_tools = [
        Tool(
            name=t.name,
            func=t.invoke,
            description=t.description,
            args_schema=t.args_schema
        ) for t in base_tools
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=JSONMessageHistory(session_id=session_id)
    )

    model = ChatOllama(model="llama3:instruct", temperature=0.7)

    agent = initialize_agent(
        tools=wrapped_tools,
        llm=model,
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent
