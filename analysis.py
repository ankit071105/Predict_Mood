#analysis.py
import streamlit as st
from nlp_utils import extract_basic_info
from faiss_engine import find_top_matches
from nlp_utils import generate_red_flags_html


def show_analysis(resume_text, jd_text_list=None):
    st.markdown("<h2 class='section-title'>🔭 Cosmic Resume Analysis</h2>", unsafe_allow_html=True)

    # Extract info from resume
    info = extract_basic_info(resume_text)

    # Ensure jd_text_list is a list, default empty
    jd_list = jd_text_list if jd_text_list else []
    jd_titles = find_top_matches(resume_text, jd_list) if jd_list else []

    # 1️⃣ Key Strengths
    skills = ", ".join(info.get("skills", []))
    st.markdown(f"""
    <div class="custom-card">
        <h4>1️⃣ Core Competencies</h4>
        <p><b>Identified Skills:</b> {skills if skills else 'N/A'}</p>
        <p>The candidate demonstrates a competent understanding of core development principles and tools, indicating readiness for structured engineering workflows.</p>
    </div>
    """, unsafe_allow_html=True)

    # 2️⃣ Suggestions for Enhancement
    recommendations = info.get("recommendations", [])
    if isinstance(recommendations, list):
        recommendations_html = "<ul>" + "".join(f"<li>{rec}</li>" for rec in recommendations) + "</ul>"
    else:
        recommendations_html = f"<p>{recommendations}</p>"

    st.markdown(f"""
    <div class="custom-card">
        <h4>2️⃣ Growth Opportunities</h4>
        {recommendations_html}
        <p>Targeted upskilling in select areas can significantly enhance alignment with evolving industry expectations.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3️⃣ Experience Assessment
    years_exp = info.get("years_experience", "N/A")
    st.markdown(f"""
    <div class="custom-card">
        <h4>3️⃣ Experience Summary</h4>
        <p><b>Estimated Experience:</b> 📅 {years_exp} year(s)</p>
        <p>Derived through contextual pattern recognition and career-specific terminology, this estimate provides a grounded view of professional tenure.</p>
    </div>
    """, unsafe_allow_html=True)

 # 4️⃣ Academic Performance Summary
    grades = info.get("grades", [])

# Build HTML for grades
    if grades:
        grades_html = "<ul>" + "".join([f"<li>📊 {g}</li>" for g in grades]) + "</ul>"
    else:
        grades_html = "<p>🎯 No grading info found.</p>"

    st.markdown(f"""
<div class="custom-card">
    <h4>4️⃣ Academic Performance</h4>
    {grades_html}
    <p>The listed grading details reflect the candidate’s academic consistency and performance benchmarks, useful for screening criteria.</p>
</div>
""", unsafe_allow_html=True)





    career_prog_raw = info.get("career_progression", "N/A")
    if career_prog_raw != "N/A":
        roles = [role.strip() for role in career_prog_raw.split("→")]
        career_prog_html = "<ol>" + "".join([f"<li>{role}</li>" for role in roles]) + "</ol>"
    else:
        career_prog_html = "<p>N/A</p>"

    # Render in Streamlit
    st.markdown(f"""
    <div class="custom-card">
        <h4>5️⃣ Career Journey</h4>
        {career_prog_html}
        <p>Chronological cues and title evolution indicate the candidate’s trajectory, reflecting advancement, functional versatility, and leadership potential.</p>
        </div>
    """, unsafe_allow_html=True)


   # 6️⃣ Red Flags / Concerns (Rewritten as a custom card)
    red_flags = info.get("red_flags", [])
    red_flags_summary = generate_red_flags_html(red_flags)

    st.markdown(f"""
<div class="custom-card">
<h4>6️⃣ Potential Concerns</h4>
{red_flags_summary}
</div>
""", unsafe_allow_html=True)



   # 7️⃣ Confidence Score
    confidence = info.get("confidence_score", 0.0)
    st.markdown(f"""
    <div class="custom-card">
        <h4>7️⃣ Overall Fit Score</h4>
        <p>📈 {confidence * 100:.2f}% match confidence</p>
        <p>This score reflects the candidate’s overall alignment with the core expectations of the role, including qualifications, experience, and cultural indicators. It serves as a guiding metric to support screening decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    # # 9️⃣ FAISS-Powered JD Suggestions
    # if jd_titles:
    #     st.markdown("""
    #     <div class="custom-card">
    #         <h4>9️⃣ Top Matching Job Descriptions</h4>
    #         <ul>
    #     """, unsafe_allow_html=True)
    #     for match in jd_titles[:5]:
    #         st.markdown(f"<li>🧾 {match['job_description'][:100]}...</li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)
