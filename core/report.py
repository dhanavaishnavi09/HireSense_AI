from io import BytesIO
from typing import List, Dict

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def build_rankings_pdf(title: str, df: pd.DataFrame) -> bytes:
    """
    Generates a simple PDF report of the ranking table.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, title)
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(x, y, "HireSense AI — Ranked Resume Matches")
    y -= 20

    # Table-like render (simple)
    cols = ["candidate", "overall_score_pct", "skill_score_pct", "tfidf_pct", "resume_exp_years", "jd_req_years", "missing_required"]
    cols = [c for c in cols if c in df.columns]

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, " | ".join(cols))
    y -= 14

    c.setFont("Helvetica", 9)
    for _, row in df.head(25).iterrows():
        line = []
        for col in cols:
            val = row[col]
            if isinstance(val, float):
                line.append(f"{val:.2f}")
            else:
                s = str(val)
                # keep line short
                s = (s[:60] + "…") if len(s) > 60 else s
                line.append(s)
        c.drawString(x, y, " | ".join(line))
        y -= 12
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()