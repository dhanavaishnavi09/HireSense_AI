import json
import os
import re
from typing import Dict, List


def load_skills_db(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _contains_skill(text: str, skill: str) -> bool:
    """
    Safer matching:
    - For single words: word boundary match
    - For phrases: substring match
    """
    skill = skill.strip().lower()
    if not skill:
        return False

    if " " in skill:  # phrase
        return skill in text
    return re.search(rf"\b{re.escape(skill)}\b", text) is not None


def extract_skills(text: str, skills: List[str], synonyms: Dict[str, List[str]] | None = None) -> List[str]:
    """
    Extract skills from text using a skill list + optional synonym mapping.
    Returns canonical skills (keys from skills list).
    """
    synonyms = synonyms or {}
    found = set()

    # Build a list of (canonical, [variants])
    canonical_variants = []
    for s in skills:
        s_low = s.lower().strip()
        variants = [s_low] + [v.lower().strip() for v in synonyms.get(s_low, [])]
        canonical_variants.append((s_low, variants))

    for canonical, variants in canonical_variants:
        for v in variants:
            if _contains_skill(text, v):
                found.add(canonical)
                break

    return sorted(found)