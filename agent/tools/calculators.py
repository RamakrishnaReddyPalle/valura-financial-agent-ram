# agent/tools/calculators.py

from langchain_core.tools import tool
from math import log, ceil, floor

def parse_str_to_dict(input_str: str) -> dict:
    return {
        k.strip(): float(v.strip()) if '.' in v or v.strip().isdigit() else v.strip()
        for k, v in (item.split("=") for item in input_str.split(","))
    }

@tool
def retirement_age_calculator_tool(input: str) -> str:
    """Estimates retirement age to reach goal amount. Format: age=30, savings=10000, monthly_saving=2000, goal=1000000, rate=0.07"""
    data = parse_str_to_dict(input)
    age = int(data["age"])
    savings = data["savings"]
    monthly_saving = data["monthly_saving"]
    goal = data["goal"]
    rate = data["rate"]

    r = rate / 12
    n = log((goal * r / monthly_saving) + 1) / log(1 + r)
    years_needed = ceil(n / 12)
    return f"You can retire at approximately age {age + years_needed}."

@tool
def savings_longevity_tool(input: str) -> str:
    """Estimates how long savings will last with fixed withdrawal. Format: savings=200000, monthly_withdrawal=5000, rate=0.05"""
    data = parse_str_to_dict(input)
    savings = data["savings"]
    monthly_withdrawal = data["monthly_withdrawal"]
    rate = data["rate"]

    r = rate / 12
    n = log(1 - (savings * r) / monthly_withdrawal) / log(1 + r)
    return f"Your savings will last approximately {floor(-n / 12)} years."

@tool
def monthly_saving_target_tool(input: str) -> str:
    """Calculates monthly savings needed to hit a target goal. Format: goal=500000, years=20, rate=0.06"""
    data = parse_str_to_dict(input)
    goal = data["goal"]
    years = int(data["years"])
    rate = data["rate"]

    r = rate / 12
    n = years * 12
    pmt = goal * r / ((1 + r) ** n - 1)
    return f"You need to save approximately ${round(pmt, 2)} per month."
