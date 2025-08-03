# inference_pipeline/prediction.py

from agent.orchestrator import run_intro_agent, run_tool_agent, run_output_agent
from agent.memory.json_memory import JSONMessageHistory
from langchain.schema.messages import AIMessage
from agent.llms import input_llm
from langchain_core.prompts import ChatPromptTemplate


def run_pipeline(user_input: str, session_id: str) -> str:
    # --- Load memory ---
    memory = JSONMessageHistory(session_id=session_id)

    # --- Stage 1: Intro LLM ---
    intro_response = run_intro_agent(user_input, session_id)

    if "[[GENERAL_CHAT]]" in intro_response:
        return intro_response.replace("[[GENERAL_CHAT]]", "").strip()

    elif "[[HANDOFF_TO_TOOLS]]" in intro_response:
        tool_result = run_tool_agent(user_input, session_id)
        tool_output = tool_result.get("output", "No output.")
        
        if "Missing required field" in tool_output or "KeyError" in tool_output:
            # Handle missing values
            ...

        # NEW: if tool output is too generic, pass to output LLM
        if tool_output and len(tool_output) < 40:
            return run_output_agent(tool_output, session_id)

        return run_output_agent(tool_output, session_id)

    else:
        # Fallback — treat intro_response as final
        return intro_response


    # --- Stage 2: Route to tool agent ---
    tool_result = run_tool_agent(user_input, session_id)
    tool_output = tool_result.get("output", "No output.")

    # --- Stage 2.5: Check for missing field errors ---
    if "Missing required field" in tool_output or "KeyError" in tool_output:
        prompt = ChatPromptTemplate.from_messages([
            ("system", open("agent/prompts/missing_fields.txt").read()),
            ("human", f"User input: {user_input}\n Tool response: {tool_output}\n Previous memory: {[m.content for m in memory.messages]}")
        ])
        recovery = input_llm.invoke(prompt.format())
        memory.add_message(AIMessage(content=recovery.content))
        return recovery.content

    # --- Stage 3: Output enhancement LLM ---
    return run_output_agent(tool_result=tool_output, session_id=session_id)


def predict_from_message(user_input: str, session_id: str) -> str:
    """
    Main callable function from the app — handles a single input message and returns a string response.
    Uses full multi-stage agent pipeline with memory + LLM routing.
    """
    return run_pipeline(user_input=user_input, session_id=session_id)
