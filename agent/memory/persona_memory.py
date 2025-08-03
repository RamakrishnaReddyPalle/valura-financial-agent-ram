from dataclasses import dataclass
from agent.memory.memory import extract_persona
from langchain.schema.messages import BaseMessage

@dataclass
class Persona:
    age: int
    income: float
    savings: float
    monthly_saving: float
    goal_age: int
    return_rate: float

def get_persona(memory) -> Persona:
    """
    Extract persona details from memory (JSONMessageHistory or ConversationBufferMemory).
    """
    # If it's ConversationBufferMemory, extract inner messages
    if hasattr(memory, "chat_memory"):
        messages = memory.chat_memory.messages
    else:
        messages = memory.messages  # JSONMessageHistory

    p = extract_persona_from_messages(messages)
    return Persona(
        age=int(p.get("age", 0)),
        income=float(p.get("income", 0)),
        savings=float(p.get("savings", 0)),
        monthly_saving=float(p.get("monthly_saving", 0)),
        goal_age=int(p.get("goal_age", 0)),
        return_rate=float(p.get("return_rate", 0.06))  # default return rate 6%
    )

# Utility (extracted logic from extract_persona)
def extract_persona_from_messages(messages: list[BaseMessage]) -> dict:
    persona = {}
    for msg in messages:
        if isinstance(msg, (str, BaseMessage)) and "User persona set:" in str(msg):
            try:
                text = msg.content.split("User persona set:")[-1]
                pairs = [kv.strip() for kv in text.split(",")]
                for pair in pairs:
                    if "=" in pair:
                        k, v = pair.split("=")
                        persona[k.strip()] = float(v.strip())
            except Exception:
                continue
    return persona
