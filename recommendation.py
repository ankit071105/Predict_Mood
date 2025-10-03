import streamlit as st
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from nlp_utils import extract_skills

# Load SBERT model once
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# --- Semantic Recommendation Function ---
def semantic_recommendation(resume_text, jd_text):
    if isinstance(jd_text, list): jd_text = " ".join(jd_text)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(resume_emb, jd_emb).item()
    return round(similarity_score, 3)

# --- Skill extraction utility ---
def extract_skills(text):
    from nlp_utils import extract_skills as base_extract
    return base_extract(text)

# --- Main Recommendation Function ---
def show_recommendation(resume_text, jd_text):
    jd_combined = " ".join(jd_text) if isinstance(jd_text, list) else jd_text

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_combined))

    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills
    total_required = len(jd_skills) or 1
    confidence_score = round(len(matched_skills) / total_required, 2)

    hard_skills = {
        "python", "java", "node.js", "docker", "aws", "gcp", "sql", "mongodb", "pytorch", "react", "spring boot",
        "typescript", "fastapi", "flask", "tensorflow", "azure", "kubernetes", "ci/cd", "spark", "graphql", "airflow"
    }
    soft_skills = {
        "teamwork", "communication", "leadership", "adaptability", "critical thinking", "problem solving"
    }

    matched_hard = resume_skills & hard_skills
    matched_soft = resume_skills & soft_skills

    critical_keywords = {"aws", "gcp", "kubernetes", "ci/cd", "graphql", "communication", "leadership"}
    critical_missing = critical_keywords & missing_skills

    match_tags = []
    if confidence_score >= 0.85:
        match_tags.append("#interview_ready")
    elif confidence_score >= 0.6:
        match_tags.append("#upskill_needed")
    else:
        match_tags.append("#role_mismatch")

    if {"aws", "gcp"} & missing_skills:
        match_tags.append("#cloud_gap")
    if matched_soft:
        match_tags.append("#culture_fit")
    if len(matched_hard) >= 5:
        match_tags.append("#tech_fit")

    learning_links = {
        "aws": "AWS Essentials (LinkedIn Learning)",
        "gcp": "Google Cloud Fundamentals (Coursera)",
        "kubernetes": "Kubernetes for Developers (Udemy)",
        "ci/cd": "CI/CD with GitHub Actions (Coursera)",
        "graphql": "Fullstack GraphQL (FreeCodeCamp)",
        "communication": "Effective Communication Skills (LinkedIn)",
        "leadership": "Leadership Principles (HarvardX)"
    }

    suggestions = [f"• {learning_links[skill]}" for skill in critical_missing if skill in learning_links]
    suggested_courses = "<br>" + "<br>".join(suggestions) if suggestions else "None"

    semantic_score = semantic_recommendation(resume_text, jd_combined)
    final_tag = "#recommended" if semantic_score > 0.75 else "#not_recommended"

    analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    from nlp_utils import extract_basic_info

    info = extract_basic_info(resume_text)

  


    def card(title, content):
        st.markdown(f"""
        <div style="background-color:#212F45;padding:1rem;border-radius:10px;margin-bottom:1rem;">
            <h4 style="color:#ffffff;margin-bottom:0.5rem;">{title}</h4>
            <div style="color:#e0e0e0;font-size:0.95rem;">{content}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>🧭 Final Recommendation</h2>", unsafe_allow_html=True)
    # card("🛠️ Skills Breakdown", f"""
    #     <ul>
    #         <li>Hard Skills Matched: {len(matched_hard)} / {len(hard_skills)}</li>
    #         <li>Soft Skills Matched: {len(matched_soft)} / {len(soft_skills)}</li>
    #     </ul>
    # """)
    # 7️⃣ Summary Recommendation
    screening_reco = info.get("recommendations", "N/A")
    if isinstance(screening_reco, list):
        screening_reco = ", ".join(screening_reco)
    st.markdown(f"""
    <div class="custom-card">
        <h4>📜 Screening Recommendation</h4>
        <p>✅ {screening_reco}</p>
        <p>This insight is based on resume parsing and skill-role mapping.</p>
    </div>
    """, unsafe_allow_html=True)    
    # card("🧩 Critical Missing Skills", ", ".join(critical_missing) if critical_missing else "None")
    card("🧭 Match Tags", " ".join(match_tags) or "None")
    card("🔄 Suggested Learning", suggested_courses)
    card("🧮 Confidence Score", f"{confidence_score * 100:.1f}%")
    card("🧠 SBERT Semantic Match Score", f"{semantic_score * 100:.1f}%")
    card("✅ Final Verdict", final_tag)
    card("⏱️ Analysis Timestamp", analysis_time)
