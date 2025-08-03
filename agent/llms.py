# agent/llms.py

from langchain_community.chat_models import ChatOllama

# Model 1: Intro LLM — onboarding, routing, general conversation
intro_llm = ChatOllama(
    model="llama3:instruct",
    temperature=0.4
)

# Model 2: Input Reasoner — handles missing values, guesses, clarification
input_llm = ChatOllama(
    model="llama3:instruct",
    temperature=0.5
)

# Model 3: Output Enhancer — elaborates tool results into final response
output_llm = ChatOllama(
    model="llama3:instruct",
    temperature=0.5,
    top_p=0.8
)

# intro_llm = ChatOllama(model="mistral:instruct", temperature=0.4)
# input_llm = ChatOllama(model="mistral:instruct", temperature=0.6)
# output_llm = ChatOllama(model="mistral:instruct", temperature=0.4)

