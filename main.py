# main.py
import streamlit as st
from resume_upload import handle_resume_upload
from jd_input import handle_jd_input
from analysis import show_analysis
from job_matches import show_job_matches
from screening import show_screening
from recommendation import show_recommendation
from faiss_engine import find_top_matches
import random

st.set_page_config(page_title="ZenResume - Advanced Analytics", layout="wide")

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add animated space background
space_bg_js = """
<script>
function createSpaceBackground() {
    const container = document.createElement('div');
    container.classList.add('space-bg');
    
    // Create stars
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        const size = Math.random() * 3;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDuration = (Math.random() * 5 + 3) + 's';
        star.style.animationDelay = (Math.random() * 5) + 's';
        star.style.opacity = Math.random() * 0.7 + 0.3;
        container.appendChild(star);
    }
    
    // Create nebulae
    const nebula1 = document.createElement('div');
    nebula1.classList.add('nebula', 'nebula-1');
    container.appendChild(nebula1);
    
    const nebula2 = document.createElement('div');
    nebula2.classList.add('nebula', 'nebula-2');
    container.appendChild(nebula2);
    
    // Create floating particles
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        const size = Math.random() * 4 + 1;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        particle.style.animationDelay = (Math.random() * 5) + 's';
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        container.appendChild(particle);
    }
    
    document.body.appendChild(container);
}
createSpaceBackground();
</script>
"""
st.components.v1.html(space_bg_js, height=0)

# Add Exo 2 font
st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700&display=swap' rel='stylesheet'>
""", unsafe_allow_html=True)

# Persistent session state to track if "Next" is clicked
if "show_tabs" not in st.session_state:
    st.session_state.show_tabs = False

# Sidebar Inputs
st.sidebar.title("📤 Upload Inputs")
resume_text = handle_resume_upload()
jd_text = handle_jd_input()

# Prepare JD list for multi-match
if jd_text:
    if "jd_list" not in st.session_state:
        st.session_state.jd_list = jd_text.split("\n\n") if isinstance(jd_text, str) else jd_text

# Sidebar Next Button
if resume_text and jd_text:
    next_clicked = st.sidebar.button("🚀 Launch Analysis", help="Click to begin analysis")

    if next_clicked:
        st.session_state.show_tabs = True

# Conditional display of main sections
if st.session_state.show_tabs and resume_text and jd_text:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2.5rem;' class="float">
        <h1 class="header-title">ZenResume</h1>
        <p class="header-subtitle">Advanced Resume Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Resume and JD successfully uploaded! Analysis initialized...")

    tabs = st.tabs([
        "🔍 Fit Overview",
        "📊 Role Matching",
        "📋 Comprehensive Screening",
        "🎯 Final Recommendation"
    ])

    with tabs[0]:
        with st.spinner("Analyzing resume structure..."):
            show_analysis(resume_text, jd_text)

    with tabs[1]:
        with st.spinner("Calculating role compatibility..."):
            show_job_matches(resume_text, st.session_state.jd_list)

    with tabs[2]:
        with st.spinner("Running comprehensive screening..."):
            screening_score = show_screening(resume_text, jd_text)

    with tabs[3]:
        with st.spinner("Generating final recommendations..."):
            show_recommendation(resume_text, jd_text)

# ... rest of your code ...

else:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2.5rem;' class="float">
        <h1 class="header-title">ZenResume</h1>
        <p class="header-subtitle">Advanced Resume Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add animated placeholder content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2.5rem; border-radius: 16px; 
                    background: rgba(18, 25, 40, 0.7); border: 1px solid rgba(52, 152, 219, 0.3);
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);' class="pulse">
            <h3 style='color: #3498db; margin-bottom: 1.5rem;'>Welcome to ZenResume Analytics</h3>
            <div style='font-size: 3.5rem; margin: 1.5rem 0; line-height: 1.2;'>
                <span style='color: #3498db;'>📄</span> 
                <span style='color: #9b59b6;'>→</span> 
                <span style='color: #f1c40f;'>🔍</span> 
                <span style='color: #9b59b6;'>→</span> 
                <span style='color: #2ecc71;'>📊</span>
            </div>
            <p style='color: #bdc3c7;'>Upload your resume and job description to unlock powerful analytics</p>
            <p style='color: #7f8c8d; font-size: 0.9rem; margin-top: 1.5rem;'>Navigate to the sidebar to upload your documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("📄 Please upload Resume and Job Description, then click **Launch Analysis** in the sidebar.")