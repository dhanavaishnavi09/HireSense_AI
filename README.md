# HireSense AI 🚀
Skill-First Resume Screening with Explainable Matching

HireSense AI is a lightweight resume screening engine that scores candidates on actual skill matches against a Job Description (JD).

Rather than relying on heavy NLP or large models, it employs a bright, pragmatic strategy:

- Skill dictionary mapping
- TF-IDF + cosine similarity
- Weighted keyword scoring
- Rule-based explainability
- Optional embeddings (future enhancement)

The aim is straightforward: precise, transparent, and interview-worthy candidate assessment.


🔍 **Problem**

Current ATS solutions:

- Lean too heavily on keyword matching
- Ignore context
- Lack any meaningful explanation for scores

HireSense AI emphasizes skill alignment with clear explanations, allowing recruiters to confidently rely on the results.


⚙️ **How It Works**

- Resume Upload (PDF)
- Job Description Paste
- Skill extraction and normalization
- Similarity calculation (TF-IDF + cosine)
- Weighted skill scoring
- Explainable candidate evaluation report generation


🧠 **Scoring Logic**

Final score aggregates:

- Skill match percentage (weighted)
- Text similarity score
- Rule-based adjustments (boosts & penalties)

This ensures the system remains:

- Technically sound
- Easy to explain in an interview
- Practical for real-world applications


🛠️ **Tech Stack**

- Python
- Streamlit
- scikit-learn (TF-IDF + cosine similarity)
- pdfplumber
- JSON skill database

This iteration:

- Eliminates redundancy
- Sounds natural
- Maintains technical rigor
- Has a product focus

📂 Built with a modular architecture separating resume extraction, skill analysis, scoring engine, and explainability logic.


