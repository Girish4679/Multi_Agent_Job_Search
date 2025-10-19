import os
from pathlib import Path
from PyPDF2 import PdfReader
import streamlit as st

def get_resume_text():
    """
    Handles both pasted resume text and PDF uploads.
    Returns the resume text as a string.
    """
    # Text area for pasted resume
    resume_text = st.text_area("Paste resume text (or upload a PDF below)", height=200)

    # PDF upload option
    uploaded_pdf = st.file_uploader("Upload resume PDF", type=["pdf"])
    if uploaded_pdf is not None:
        # Use package-root (job_hunt_assistant/) as canonical data dir
        pkg_root = Path(__file__).resolve().parents[1]   # job_hunt_assistant/
        # create single canonical subdir: job_hunt_assistant/data/resume/
        out_dir = pkg_root / "data" / "resume"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded PDF to disk under package data/resume/
        pdf_path = out_dir / uploaded_pdf.name
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        # Extract text from PDF (in-memory)
        try:
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            st.error(f"Failed to extract text from PDF: {e}")
            pdf_text = ""

        # Prefer uploaded PDF text over pasted text
        if pdf_text.strip():
            resume_text = pdf_text
            st.success(f"Loaded resume from {uploaded_pdf.name}")

    return resume_text

