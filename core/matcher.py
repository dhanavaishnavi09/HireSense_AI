from dataclasses import dataclass
from typing import List, Dict, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class MatchResult:
    tfidf_similarity_pct: float
    weighted_skill_score_pct: float
    overall_score_pct: float
    required_matched: List[str]
    required_missing: List[str]
    preferred_matched: List[str]
    preferred_missing: List[str]


def tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF cosine similarity between resume text and JD text.
    Returns percentage.
    """
    vect = TfidfVectorizer(stop_words="english")
    X = vect.fit_transform([resume_text, jd_text])
    sim = cosine_similarity(X[0], X[1])[0][0]
    return round(float(sim) * 100.0, 2)


def weighted_skill_score(
    resume_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str],
    required_weight: int = 3,
    preferred_weight: int = 1,
) -> Tuple[float, List[str], List[str], List[str], List[str]]:
    """
    Weighted scoring:
    - required skills get higher weight
    - preferred skills get lower weight
    """
    resume_set = set(resume_skills)
    req_set = set(required_skills)
    pref_set = set(preferred_skills)

    req_matched = sorted(req_set & resume_set)
    req_missing = sorted(req_set - resume_set)

    pref_matched = sorted(pref_set & resume_set)
    pref_missing = sorted(pref_set - resume_set)

    total = (len(required_skills) * required_weight) + (len(preferred_skills) * preferred_weight)
    if total == 0:
        return 0.0, req_matched, req_missing, pref_matched, pref_missing

    score = (len(req_matched) * required_weight) + (len(pref_matched) * preferred_weight)
    pct = round((score / total) * 100.0, 2)

    return pct, req_matched, req_missing, pref_matched, pref_missing


def combine_scores(tfidf_pct: float, skill_pct: float, tfidf_weight: float = 0.4, skill_weight: float = 0.6) -> float:
    """
    Final overall score = weighted combination.
    Default: skill matching matters more than raw text similarity.
    """
    overall = (tfidf_pct * tfidf_weight) + (skill_pct * skill_weight)
    return round(overall, 2)


def evaluate(
    resume_text: str,
    jd_text: str,
    resume_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str],
) -> MatchResult:
    t_pct = tfidf_similarity(resume_text, jd_text)

    s_pct, req_m, req_miss, pref_m, pref_miss = weighted_skill_score(
        resume_skills=resume_skills,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
    )

    overall = combine_scores(t_pct, s_pct)

    return MatchResult(
        tfidf_similarity_pct=t_pct,
        weighted_skill_score_pct=s_pct,
        overall_score_pct=overall,
        required_matched=req_m,
        required_missing=req_miss,
        preferred_matched=pref_m,
        preferred_missing=pref_miss,
    )