# agent/orchestrator.py

from agent.llms import intro_llm, output_llm, input_llm
from agent.builder import build_agent
from agent.memory.json_memory import JSONMessageHistory
from langchain.schema.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import re
import os

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

# --- Load the user-specific chat history memory (multi-turn safe) ---
def load_memory(session_id):
    return JSONMessageHistory(session_id=session_id)

# --- Run the Intro Agent to greet, detect intent, or ask for persona ---
def run_intro_agent(user_input: str, session_id: str) -> str:
    memory = load_memory(session_id)
    messages = memory.messages + [HumanMessage(content=user_input)]
    response = intro_llm.invoke(messages)
    memory.add_message(HumanMessage(content=user_input))
    memory.add_message(AIMessage(content=response.content))
    return response.content

# --- Parse a comma-separated input string into a dictionary ---
def parse_input_string(input_str):
    return {k.strip(): v.strip() for k, v in [item.split("=") for item in input_str.split(",") if "=" in item]}

# --- Expected keys for each tool ---
TOOL_PARAMS = {
    "monthly_saving_target_tool": ["goal", "years", "rate"],
    "retirement_age_calculator_tool": ["age", "savings", "monthly_saving", "goal", "rate"],
    "savings_longevity_tool": ["savings", "monthly_withdrawal", "rate"],
    "future_value_tool": ["pv", "rate", "n"],
    "present_value_tool": ["fv", "rate", "n"],
    "future_value_annuity_tool": ["pmt", "rate", "n"],
    "present_value_annuity_tool": ["pmt", "rate", "n"],
    "number_of_periods_tool": ["rate", "pmt", "pv"],
    "rule_of_72_tool": ["rate"]
}

# --- Detect and handle missing fields ---
def detect_missing_fields(tool_name: str, input_str: str):
    parsed = parse_input_string(input_str)
    expected_keys = TOOL_PARAMS.get(tool_name, [])
    missing = [k for k in expected_keys if k not in parsed]
    return parsed, missing

# --- Run the Routing Agent with Tools + Missing Field Reasoning ---
def run_tool_agent(user_input: str, session_id: str):
    agent = build_agent(session_id=session_id)
    result = agent.invoke({"input": user_input})

    # Try to parse tool name + input from LLM's structured plan
    pattern = r'"action":\s*"(.*?)".*?"action_input":\s*"(.*?)"'
    match = re.search(pattern, result.get("intermediate_steps", "") + str(result), re.DOTALL)

    if match:
        tool_name = match.group(1)
        action_input = match.group(2)
        parsed_input, missing = detect_missing_fields(tool_name, action_input)

        if missing:
            prompt = open(os.path.join(PROMPT_DIR, "missing_fields.txt")).read()
            user_msg = f"Tool: {tool_name}\nKnown: {parsed_input}\nMissing: {missing}"
            response = input_llm.invoke(prompt + "\n" + user_msg)
            return {"output": response.content, "needs_followup": True}

    return result

# --- Run Output Agent to enhance the final tool result + memory ---
def run_output_agent(tool_result: str, session_id: str) -> str:
    memory = load_memory(session_id)
    conversation = "\n".join([f"{m.type.upper()}: {m.content}" for m in memory.messages])

    prompt = ChatPromptTemplate.from_messages([
        ("system", open(os.path.join(PROMPT_DIR, "output_prompt.txt")).read()),
        ("human", "Conversation so far:\n{conversation}\n\nTool output:\n{tool_result}\n\nPlease explain the result clearly to the user.")
    ])

    response = output_llm.invoke(prompt.format(conversation=conversation, tool_result=tool_result))
    memory.add_message(AIMessage(content=response.content))
    return response.content
