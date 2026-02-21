import re
from typing import Optional, Tuple


def _to_years(num: float, unit: str) -> float:
    unit = unit.lower()
    if unit.startswith("month"):
        return num / 12.0
    return num


def extract_years_of_experience(text: str) -> float:
    """
    Extracts an approximate years-of-experience from resume text.
    Heuristic: take the maximum found among patterns.
    Examples:
      - "3 years", "2.5 yrs", "18 months", "1 year 6 months"
    """
    t = text.lower()

    # Pattern 1: "X years" or "X yrs"
    p1 = re.findall(r"(\d+(?:\.\d+)?)\s*(years?|yrs?)", t)
    years_vals = [_to_years(float(n), u) for n, u in p1]

    # Pattern 2: "X months"
    p2 = re.findall(r"(\d+(?:\.\d+)?)\s*(months?|mos?)", t)
    years_vals += [_to_years(float(n), "months") for n, _ in p2]

    # Pattern 3: "X year(s) Y month(s)"
    p3 = re.findall(r"(\d+(?:\.\d+)?)\s*years?\s*(\d+(?:\.\d+)?)\s*months?", t)
    for y, m in p3:
        years_vals.append(float(y) + float(m) / 12.0)

    if not years_vals:
        return 0.0

    return round(max(years_vals), 2)


def extract_required_experience_from_jd(jd_text: str) -> float:
    """
    Extract required experience from JD.
    Looks for patterns like:
      - "3+ years", "2 years", "minimum 5 years", "2-4 years"
    Returns a single float (best guess).
    """
    t = jd_text.lower()

    # Range like "2-4 years"
    rng = re.findall(r"(\d+(?:\.\d+)?)\s*[-to]{1,3}\s*(\d+(?:\.\d+)?)\s*years?", t)
    if rng:
        # take lower bound as "minimum"
        low = float(rng[0][0])
        return round(low, 2)

    # "3+ years"
    plus = re.findall(r"(\d+(?:\.\d+)?)\s*\+\s*years?", t)
    if plus:
        return round(float(plus[0]), 2)

    # "minimum 3 years"
    mn = re.findall(r"(?:minimum|min)\s*(\d+(?:\.\d+)?)\s*years?", t)
    if mn:
        return round(float(mn[0]), 2)

    # plain "3 years"
    plain = re.findall(r"(\d+(?:\.\d+)?)\s*years?", t)
    if plain:
        return round(float(plain[0]), 2)

    return 0.0