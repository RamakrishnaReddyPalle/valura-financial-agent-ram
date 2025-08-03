# agent/tools/formulas.py
from langchain_core.tools import tool
from utils.parser import parse_input
import math

def parse_input(input: str) -> dict:
    return {
        k.strip(): float(v.strip())
        for k, v in (pair.split('=') for pair in input.split(','))
    }

@tool
def future_value_tool(input: str) -> float:
    """Calculate future value: FV = PV * (1 + r)^n"""
    data = parse_input(input)
    return round(data["pv"] * ((1 + data["rate"]) ** data["n"]), 2)

@tool
def present_value_tool(input: str) -> float:
    """Calculate present value: PV = FV / (1 + r)^n"""
    data = parse_input(input)
    return round(data["fv"] / ((1 + data["rate"]) ** data["n"]), 2)

@tool
def future_value_annuity_tool(input: str) -> float:
    """Calculate FV of annuity: FV = PMT × [(1 + r)^n – 1] / r"""
    data = parse_input(input)
    return round(data["pmt"] * (((1 + data["rate"]) ** data["n"] - 1) / data["rate"]), 2)

@tool
def present_value_annuity_tool(input: str) -> float:
    """Calculate PV of annuity: PV = PMT × [1 – (1 + r)^(-n)] / r"""
    data = parse_input(input)
    return round(data["pmt"] * (1 - (1 + data["rate"]) ** -data["n"]) / data["rate"], 2)

@tool
def number_of_periods_tool(input: str) -> float:
    """Calculate number of periods (Excel-style NPER)"""
    data = parse_input(input)
    rate = data["rate"]
    pmt = data["pmt"]
    pv = data["pv"]
    fv = data.get("fv", 0.0)
    if pmt == 0:
        raise ValueError("PMT must not be zero")
    return round(math.log((pmt + rate * fv) / (pmt + rate * pv)) / math.log(1 + rate), 2)

@tool
def rule_of_72_tool(input: str) -> float:
    """Estimate doubling time using Rule of 72: Years = 72 / (rate * 100)"""
    data = parse_input(input)
    return round(72 / (data["rate"] * 100), 2)
