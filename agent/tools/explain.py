# agent/tools/explain.py

from langchain_core.tools import tool

@tool
def explain_formula_tool(input: str) -> str:
    """
    Explains a common financial formula by name.
    Supported keywords: fv, pv, fv_annuity, pv_annuity, nper, rule_72
    """
    key = input.strip().lower()
    explanations = {
        "fv": "Future Value (FV) = PV × (1 + r)^n — calculates how much your money will grow over time.",
        "pv": "Present Value (PV) = FV / (1 + r)^n — determines today's value of a future sum.",
        "fv_annuity": "FV of Annuity = PMT × [(1 + r)^n – 1] / r — computes future value of recurring deposits.",
        "pv_annuity": "PV of Annuity = PMT × [1 – (1 + r)^(-n)] / r — computes how much a series of withdrawals is worth today.",
        "nper": "NPER estimates the number of periods to reach a goal based on payment and interest.",
        "rule_72": "Rule of 72: Years ≈ 72 / (rate × 100) — quickly estimates how long it takes to double your money."
    }

    return explanations.get(key, "⚠️ Sorry, I don't recognize that formula keyword.")
