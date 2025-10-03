# 📁 File: jd_input.py

import streamlit as st
import tempfile
import fitz  # PyMuPDF

def read_text_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        with open(tmp_file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        st.sidebar.error(f"Error reading text file: {str(e)}")
        return ""

def read_pdf_file(uploaded_file):
    try:
        text = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        with fitz.open(tmp_file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        st.sidebar.error(f"Error reading PDF file: {str(e)}")
        return ""

def handle_jd_input():
    st.sidebar.subheader("📑 Job Description Input")
    option = st.sidebar.radio("Choose how to provide JD:", ("Write JD", "Upload JD File"))

    jd_text = ""
    if option == "Write JD":
        jd_text = st.sidebar.text_area("📝 Paste one or more job descriptions (separate using two new lines)", height=250)
    elif option == "Upload JD File":
        jd_file = st.sidebar.file_uploader("📁 Upload a JD file (.txt or .pdf)", type=["txt", "pdf"])
        if jd_file:
            if jd_file.type == "text/plain":
                jd_text = read_text_file(jd_file)
            elif jd_file.type == "application/pdf":
                jd_text = read_pdf_file(jd_file)
            else:
                st.sidebar.warning("⚠️ Unsupported file type. Please upload a .txt or .pdf file.")
                return None

    # Cleanup and return multiple JDs if provided
    if jd_text:
        jd_list = [jd.strip() for jd in jd_text.split("\n\n") if jd.strip()]
        if jd_list:
            st.sidebar.success(f"✅ {len(jd_list)} JD(s) processed successfully.")
            return jd_list
        else:
            st.sidebar.warning("⚠️ JD content was empty after processing.")
            return None

    return None
