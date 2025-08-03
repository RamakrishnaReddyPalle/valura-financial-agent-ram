# agent/memory/json_memory.py

import os
import json
from typing import List, Union
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage, BaseMessage

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SESSIONS_DIR = os.path.join(PROJECT_ROOT, "sessions")

class JSONMessageHistory(BaseChatMessageHistory):
    """
    A custom chat history implementation that stores messages in a JSON file
    specific to each session.
    """

    def __init__(self, session_id: str):
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        self.file_path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        self.messages: List[BaseMessage] = self._load_messages()

    def _load_messages(self) -> List[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []

        messages: List[BaseMessage] = []
        for item in data:
            if item.get("role") == "human":
                messages.append(HumanMessage(content=item.get("content", "")))
            elif item.get("role") == "ai":
                messages.append(AIMessage(content=item.get("content", "")))
        return messages

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)
        self.save()

    def clear(self) -> None:
        self.messages = []
        self.save()

    def save(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(
                [
                    {
                        "role": "human" if isinstance(m, HumanMessage) else "ai",
                        "content": m.content,
                    }
                    for m in self.messages
                ],
                f,
                indent=2,
            )
