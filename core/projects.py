import re
from typing import List


def extract_projects(text: str, max_projects: int = 5) -> List[str]:
    """
    Very simple heuristic project detection:
    - captures lines that look like project titles near "project" keyword
    - returns a list of short strings
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    projects = []

    for i, ln in enumerate(lines):
        l = ln.lower()
        if "project" in l:
            # try take the same line or next line as title
            candidate = ln
            if len(candidate) < 5 and i + 1 < len(lines):
                candidate = lines[i + 1]

            # clean bullets/symbols
            candidate = re.sub(r"^[\-\*\•\s]+", "", candidate).strip()
            if 6 <= len(candidate) <= 80:
                projects.append(candidate)

    # unique + limit
    uniq = []
    for p in projects:
        if p not in uniq:
            uniq.append(p)

    return uniq[:max_projects]