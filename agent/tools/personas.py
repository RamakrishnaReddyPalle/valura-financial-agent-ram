# agent/tools/personas.py

from langchain_core.tools import tool

@tool
def set_persona_tool(input: str) -> str:
    """
    Save user's financial persona from a string.
    Example input: "age=35, income=100000, savings=15000, monthly_saving=2000, goal_age=60, return_rate=0.07"
    """
    try:
        fields = dict(item.strip().split("=") for item in input.split(","))
        age = int(fields.get("age", 0))
        income = float(fields.get("income", 0))
        savings = float(fields.get("savings", 0))
        monthly_saving = float(fields.get("monthly_saving", 0))
        goal_age = int(fields.get("goal_age", 0))
        return_rate = float(fields.get("return_rate", 0.06))

        return (
            f"Persona saved:\n"
            f"Age: {age}, Income: {income}, Savings: {savings},\n"
            f"Monthly Saving: {monthly_saving}, Goal Age: {goal_age}, Return Rate: {return_rate}"
        )
    except Exception as e:
        return f"⚠️ Error parsing persona: {str(e)}"
