# 📁 File: resume_upload.py

import streamlit as st
import fitz  # PyMuPDF
import tempfile

def extract_text_from_pdf(pdf_file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name
    
    doc = fitz.open(tmp_file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def handle_resume_upload():
    uploaded_file = st.sidebar.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.sidebar.success("✅ Resume uploaded and processed.")
        return resume_text
    return None 