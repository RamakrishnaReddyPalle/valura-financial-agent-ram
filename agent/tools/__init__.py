# agent/tools/__init__.py

from .calculators import (
    retirement_age_calculator_tool,
    savings_longevity_tool,
    monthly_saving_target_tool
)
from .formulas import (
    future_value_tool,
    present_value_tool,
    future_value_annuity_tool,
    present_value_annuity_tool,
    rule_of_72_tool,
    number_of_periods_tool
)
from .personas import set_persona_tool
from .explain import explain_formula_tool

__all__ = [
    "set_persona_tool",
    "future_value_tool", "present_value_tool",
    "future_value_annuity_tool", "present_value_annuity_tool",
    "rule_of_72_tool", "number_of_periods_tool",
    "retirement_age_calculator_tool", "savings_longevity_tool",
    "monthly_saving_target_tool", "explain_formula_tool",
    "get_all_tools"
]

def get_all_tools():
    return [
        set_persona_tool,
        future_value_tool,
        present_value_tool,
        future_value_annuity_tool,
        present_value_annuity_tool,
        rule_of_72_tool,
        number_of_periods_tool,
        retirement_age_calculator_tool,
        savings_longevity_tool,
        monthly_saving_target_tool,
        explain_formula_tool
    ]
