# agent/prompts/response_templates.py

def format_formula_response(formula_name: str, result: float, explanation: str = None) -> str:
    response = f"The result for {formula_name.upper()} is: {round(result, 2)}."
    if explanation:
        response += f"\nExplanation: {explanation}"
    return response

def format_retirement_age(age: int) -> str:
    return f"📅 You can retire around age {age} based on your current savings and return rate."

def format_savings_duration(years: int) -> str:
    return f"💸 Your savings will last approximately {years} years at the given withdrawal rate."

def format_monthly_target(amount: float) -> str:
    return f"📈 To reach your goal, save around ${round(amount, 2)} monthly."
