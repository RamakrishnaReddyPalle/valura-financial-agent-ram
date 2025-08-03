import os
import gradio as gr
from uuid import uuid4

import sys
import os

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from inference_pipeline.prediction import run_pipeline
from agent.memory.json_memory import JSONMessageHistory
from agent.memory.persona_memory import get_persona

# ✅ Global sessions directory
SESSIONS_DIR = os.path.join(PROJECT_ROOT, "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# 🔁 Fetch existing sessions
def list_sessions():
    return [f.replace(".json", "") for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]

# 🆕 Create a new session
def create_new_session():
    return str(uuid4())[:8]

# 📋 Display current persona (if any)
def get_persona_card(session_id):
    memory = JSONMessageHistory(session_id=session_id)
    persona = get_persona(memory)
    if persona.age == 0:
        return "📋 No persona saved yet."
    return f"""📋 **Persona Summary**
- Age: {persona.age}
- Income: {persona.income}
- Savings: {persona.savings}
- Monthly Saving: {persona.monthly_saving}
- Goal Age: {persona.goal_age}
- Return Rate: {persona.return_rate}
"""

# 🔄 Chat pipeline with streaming output
def chat_stream(user_msg, session_id):
    yield run_pipeline(user_input=user_msg, session_id=session_id)

# 💬 Initial message
def get_initial_message(session_id):
    return run_pipeline("Hi!", session_id)

# 🎛️ Gradio UI
with gr.Blocks(title="💰 Valura Financial Planning Agent") as app:
    gr.Markdown("## 💰 **Valura Financial Planning Agent**")

    with gr.Row():
        session_id_state = gr.State("default")

        session_selector = gr.Dropdown(
            label="💬 Select Session",
            choices=list_sessions(),
            value=None,
            interactive=True,
            allow_custom_value=True
        )

        new_btn = gr.Button("➕ Start New Session", variant="primary")
        persona_box = gr.Markdown(get_persona_card("default"))

    chatbot_box = gr.Chatbot(label="🧠 Ram - Financial Assistant")
    chat_input = gr.Textbox(placeholder="Ask about retirement, savings, goals...", show_label=False)
    send_button = gr.Button("💬 Send")

    # 🔁 Chat handler with session state
    def handle_user_message(msg, history, session_id):
        return history + [(msg, next(chat_stream(msg, session_id)))]

    send_button.click(
        fn=handle_user_message,
        inputs=[chat_input, chatbot_box, session_id_state],
        outputs=chatbot_box
    )

    sample_questions = [
        "What do I need to retire at 50?",
        "How much should I save monthly to reach $1M in 25 years?",
        "Can you help me plan early retirement?",
        "How long will my savings of $200,000 last if I withdraw $5,000 monthly?",
        "What’s the future value of $10,000 in 10 years at 7%?",
    ]

    with gr.Accordion("💡 Sample Questions", open=False):
        for q in sample_questions:
            gr.Button(q).click(
                fn=lambda q=q: [(q, next(chat_stream(q, session_id_state.value)))],
                inputs=[],
                outputs=chatbot_box
            )

    # 🔁 Session switching
    def on_session_select(session_id):
        session_id_state.value = session_id
        return get_persona_card(session_id)

    session_selector.change(
        fn=on_session_select,
        inputs=session_selector,
        outputs=persona_box
    )

    # ➕ New session
    def on_new_session():
        new_id = create_new_session()
        session_selector.choices = list_sessions()
        session_selector.value = new_id
        session_id_state.value = new_id
        initial_msg = get_initial_message(new_id)
        return get_persona_card(new_id), gr.update(choices=list_sessions(), value=new_id), [(initial_msg, "")]

    new_btn.click(
        fn=on_new_session,
        inputs=[],
        outputs=[persona_box, session_selector, chatbot_box]
    )

__all__ = ["app"]
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=8000, share=True)

