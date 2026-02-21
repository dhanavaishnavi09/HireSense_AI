import os
import pandas as pd
import streamlit as st

from core.pdf_extract import extract_text_from_pdf
from core.preprocess import clean_text
from core.skills import load_skills_db, extract_skills
from core.matcher import evaluate
from core.explain import build_explanation
from core.experience import extract_years_of_experience, extract_required_experience_from_jd
from core.projects import extract_projects
from core.report import to_csv_bytes, build_rankings_pdf


st.set_page_config(page_title="HireSense AI", layout="wide")
st.title("HireSense AI — Explainable ATS Simulation (Multi-Resume Ranking)")

SKILLS_DB_PATH = os.path.join("data", "skills_db.json")

# Inputs
left, right = st.columns([1, 1])

with left:
    resume_files = st.file_uploader(
        "Upload Resume PDFs (you can upload multiple)",
        type=["pdf"],
        accept_multiple_files=True
    )

with right:
    jd_text_input = st.text_area("Paste Job Description", height=240)

st.caption("")

top_n = st.slider("Show Top N", min_value=3, max_value=25, value=10, step=1)

if st.button("🔍 Evaluate & Rank"):
    if not resume_files or not jd_text_input.strip():
        st.warning("Please upload at least 1 resume PDF and paste the job description.")
        st.stop()

    # Load skills DB
    db = load_skills_db(SKILLS_DB_PATH)
    required = [s.lower() for s in db.get("required", [])]
    preferred = [s.lower() for s in db.get("preferred", [])]
    synonyms = db.get("synonyms", {})

    all_skills = list(dict.fromkeys(required + preferred))  # unique

    jd_text = clean_text(jd_text_input)
    jd_req_years = extract_required_experience_from_jd(jd_text)

    rows = []
    detailed = []

    for f in resume_files:
        raw = extract_text_from_pdf(f)
        resume_text = clean_text(raw)

        resume_exp = extract_years_of_experience(resume_text)
        resume_projects = extract_projects(raw)  # raw keeps lines better

        resume_skills = extract_skills(resume_text, all_skills, synonyms=synonyms)

        result = evaluate(
            resume_text=resume_text,
            jd_text=jd_text,
            resume_skills=resume_skills,
            required_skills=required,
            preferred_skills=preferred,
        )

        exp_gap = round(max(0.0, jd_req_years - resume_exp), 2)

        exp = build_explanation(
            required_matched=result.required_matched,
            required_missing=result.required_missing,
            preferred_matched=result.preferred_matched,
            preferred_missing=result.preferred_missing,
        )

        candidate_name = f.name.replace(".pdf", "")

        rows.append({
            "candidate": candidate_name,
            "overall_score_pct": result.overall_score_pct,
            "skill_score_pct": result.weighted_skill_score_pct,
            "tfidf_pct": result.tfidf_similarity_pct,
            "resume_exp_years": resume_exp,
            "jd_req_years": jd_req_years,
            "experience_gap_years": exp_gap,
            "missing_required": ", ".join(result.required_missing) if result.required_missing else "—",
            "missing_preferred": ", ".join(result.preferred_missing) if result.preferred_missing else "—",
        })

        detailed.append({
            "candidate": candidate_name,
            "strong_match": exp["strong_match"],
            "missing_skills": exp["missing_skills"],
            "projects_detected": ", ".join(resume_projects) if resume_projects else "—",
        })

    df = pd.DataFrame(rows).sort_values(by=["overall_score_pct", "skill_score_pct", "tfidf_pct"], ascending=False).reset_index(drop=True)
    df_top = df.head(top_n)

    st.subheader("🏁 Ranked Candidates")
    st.dataframe(df_top, use_container_width=True)

    # Downloads
    st.subheader("⬇️ Export")
    st.download_button(
        "Download CSV (Ranking Report)",
        data=to_csv_bytes(df),
        file_name="hiresense_ranking_report.csv",
        mime="text/csv"
    )

    pdf_bytes = build_rankings_pdf("HireSense AI — Ranking Report", df)
    st.download_button(
        "Download PDF (Ranking Report)",
        data=pdf_bytes,
        file_name="hiresense_ranking_report.pdf",
        mime="application/pdf"
    )

    # Show detailed explainability for Top 1
    st.divider()
    st.subheader("🧠 Explainability (Top Candidate)")

    top_candidate = df.iloc[0]["candidate"]
    top_info = next((d for d in detailed if d["candidate"] == top_candidate), None)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Top Candidate", top_candidate)
        st.write("**Strong match:**")
        st.success(top_info["strong_match"] if top_info else "—")
        st.write("**Missing skills:**")
        st.error(top_info["missing_skills"] if top_info else "—")

    with c2:
        st.write("**Projects detected (heuristic):**")
        st.write(top_info["projects_detected"] if top_info else "—")
        st.write("**Experience:**")
        st.write(f"Resume: {df.iloc[0]['resume_exp_years']} yrs | JD asks: {df.iloc[0]['jd_req_years']} yrs | Gap: {df.iloc[0]['experience_gap_years']} yrs")

    with st.expander("🔎 Notes (how scoring works)"):
        st.write(
            "- Overall score = 60% weighted skill score + 40% TF-IDF similarity\n"
            "- Required skills have higher weight than preferred skills\n"
            "- Experience extraction is heuristic (regex); it gives an approximate value"
        )