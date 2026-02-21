import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a PDF uploaded via Streamlit file_uploader.
    """
    parts = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)