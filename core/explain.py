from typing import List, Dict


def build_explanation(required_matched: List[str], required_missing: List[str],
                      preferred_matched: List[str], preferred_missing: List[str]) -> Dict[str, str]:
    strong = required_matched + preferred_matched
    missing = required_missing + preferred_missing

    strong_txt = ", ".join(strong) if strong else "—"
    missing_txt = ", ".join(missing) if missing else "—"

    return {
        "strong_match": strong_txt,
        "missing_skills": missing_txt,
        "note": "Required skills impact the score more than Preferred skills (weighted scoring)."
    }