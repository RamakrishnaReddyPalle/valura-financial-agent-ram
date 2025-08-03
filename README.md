Solution to Take-away Assignment for AI/ML Engineer Position at Valura.ai

# 💰 **Valura Financial Planning Assistant**

This is an interactive AI-powered chatbot that guides users through personalized financial planning, including retirement strategies, savings goals, future value estimations, and more.

I built on a **multi-stage agentic system** using local LLMs via Ollama (`llama3:instruct`), the assistant is equipped to:
- Handle **general conversation**
- Extract financial **persona**
- Reason through **incomplete inputs**
- Execute **calculation tools**
- Return **clear, human-readable financial advice**

---

## 🚩 **Problem Statement**

Many people are unsure how to begin planning their finances, lack access to personalized tools, or don’t know how to translate abstract goals (like retiring at 50) into actionable strategies.

This agent solves this by combining:
- Conversational AI for user engagement
- Financial calculators for concrete output
- Multi-turn memory to track the user's goals over time

---

## 🧠 **Project Structure**

```

valura\_agent/
├── agent/
│   ├── builder.py                # Build LangChain agent with tools + memory
│   ├── orchestrator.py          # Manages flow: intro → tool → output
│   ├── llms.py                  # Defines all LLM models
│   ├── tools/                   # Financial tools (FV, PV, Retirement, etc.)
│   ├── memory/
│   │   ├── json\_memory.py       # Session-wise message history
│   │   ├── memory.py            # Persona extraction logic
│   │   └── persona\_memory.py    # Unified Persona data model
│   └── prompts/                 # Contains system prompts for intro/output/missing values
│
├── inference\_pipeline/
│   └── prediction.py            # Entry point for handling a single user message
│
├── sessions/                    # Persistent conversation logs (per user)
│
├── ui/
│   └── app.py                   # Gradio UI for the assistant
│
└── requirements.txt             # Python dependencies

```

---

## ⚙️ **Agent Flow and Reasoning**

The main idea is to follow a **3-stage decision pipeline**. Here's how it intelligently responds across various user inputs:

| User Input | Module | Description |
|------------|--------|-------------|
| `"Hi!"` | `intro_llm` | Detected as small talk → responds politely and explains financial capabilities |
| `"Can you help with retirement?"` | `intro_llm` → `[[GENERAL_CHAT]]` | Describes tools available + asks user for missing persona fields |
| `"I want to retire at 50"` | `intro_llm` → `[[HANDOFF_TO_TOOLS]]` → `tool_agent` | Passes input to retirement_age_calculator_tool |
| `"My age is 30, I save 1000/month"` | `tool_agent` → `input_llm` | Tries to complete inputs (e.g., missing income/savings) |
| After tool output: `"You can retire at age 58"` | `output_llm` | Enhances response with explanation & follow-up question |

💡 Every conversation is stored per user (`sessions/`), and the tool can handle **partial inputs**, **follow-up recovery**, and **streamed responses**.

---

## 🎬 **UI Demo Walkthrough**

> 📽️ [Demo Video — Walkthrough of Valura Agent UI](https://your-demo-link.com)

---

## 🛠️ **Setup Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/RamakrishnaReddyPalle/valura-financial-agent-ram.git
cd valura-agent
````

### 2. Set up the Environment

I used **Python 3.11**. Then create and activate a virtual environment:

```bash
python -m venv valura_agent
source valura_agent/bin/activate    # or .\valura_agent\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Install Ollama (for local LLM inference)

* Download and install Ollama from: [https://ollama.com](https://ollama.com)
* Then pull the LLaMA 3 instruct model:

```bash
ollama pull llama3:instruct
```

> You can monitor or serve Ollama in the background with:
>
> ```bash
> ollama serve
> ```

---

### 4. Run the App

Launch the full-streaming Gradio interface:

```bash
python ui/app.py
```

Then open your browser at `http://localhost:7860` and start chatting with **Valura: your financial assistant**.

---

## 🧾 **Sample Questions**

Use any of these to test the assistant’s capabilities:

* "What do I need to retire at 50?"
* "How much should I save monthly to reach \$1M in 25 years?"
* "Can you help me plan early retirement?"
* "How long will my savings of \$200,000 last if I withdraw \$5,000 monthly?"
* "What’s the future value of \$10,000 in 10 years at 7%?"

---

## 📦 **Tech Stack**

* **LangChain Agents & Tools**
* **Ollama + llama3\:instruct**
* **Gradio UI** with streaming
* **Custom memory management** with persistent JSON files
* **Modular, multi-stage reasoning architecture**

---

## 🧠 **Author**

Ramakrishna Reddy Palle
*B.Tech EE, IIT Bhubaneswar*
GitHub: [@RamakrishnaReddyPalle](https://github.com/RamakrishnaReddyPalle)



