import re


def clean_text(text: str) -> str:
    """
    Basic cleaning: lowercase, normalize spaces.
    """
    text = (text or "").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()