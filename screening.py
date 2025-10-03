import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import (
    extract_basic_info,
    extract_certifications_and_achievements,
    estimate_skill_depth,
    analyze_career_path,
    count_academic_points,
    calculate_experience_score,
    evaluate_relevant_experience,
    title_match_score,
    leadership_mention_score,
    extract_job_title
)
import re
import time

# Inject CSS styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def extract_years_of_experience(resume_text):
    text = resume_text.lower()
    matches = re.findall(r'(\d+)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience', text)
    academic_phrases = re.findall(r'\d+(st|nd|rd|th)?\s+year\s+(student|b\.?tech|m\.?tech|undergraduate)', text)
    if academic_phrases:
        return 0
    if matches:
        years = [int(y) for y in matches if int(y) <= 50]
        return max(years) if years else 0
    return 0

def extract_jd_requirements(jd_text):
    requirements = {
        "required_skills": [],
        "min_experience": 0,
        "required_degree": ""
    }

    jd_text = jd_text.lower()
    known_skills = [
        "python", "java", "javascript", "typescript", "c++", "c", "go", "rust", "ruby", "scala", "kotlin", "r",
        "react", "angular", "vue", "next.js", "node.js", "flask", "django", "express", "spring boot", "fastapi",
        "machine learning", "deep learning", "nlp", "computer vision", "data analysis", "data visualization",
        "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "tensorflow", "keras", "pytorch", "huggingface",
        "sql", "mysql", "postgresql", "mongodb", "firebase", "cassandra", "oracle", "sqlite", "snowflake",
        "aws", "azure", "gcp", "heroku", "digitalocean", "lambda", "s3", "ec2", "firebase",
        "docker", "kubernetes", "jenkins", "gitlab", "github actions", "ansible", "terraform", "helm",
        "pytest", "unittest", "selenium", "cypress", "postman", "jmeter",
        "git", "github", "bitbucket", "jira", "confluence",
        "communication", "leadership", "teamwork", "problem solving", "adaptability", "critical thinking",
        "excel", "power bi", "tableau", "airflow", "hadoop", "spark", "kafka", "elasticsearch", "graphql", "rest api"
    ]

    requirements["required_skills"] = [skill for skill in known_skills if skill in jd_text]
    exp_match = re.search(r'(\d+)\+?\s+years? of experience', jd_text)
    if exp_match:
        requirements["min_experience"] = int(exp_match.group(1))
    if "bachelor" in jd_text or "b.tech" in jd_text:
        requirements["required_degree"] = "bachelor"
    elif "master" in jd_text or "m.tech" in jd_text:
        requirements["required_degree"] = "master"
    return requirements

def show_screening(resume_text, jd_text):
    st.markdown("<h2 class='section-title'>📋 Screening Dashboard</h2>", unsafe_allow_html=True)

    resume_info = extract_basic_info(resume_text)
    if isinstance(jd_text, list):
        jd_text = jd_text[0] if jd_text else ""
    jd_info = extract_jd_requirements(jd_text)

    resume_exp = extract_years_of_experience(resume_text)
    exp_required = jd_info.get("min_experience", 0)
    jd_title = extract_job_title(jd_text)
    jd_skills = jd_info.get("required_skills", [])

    # ✅ New experience relevance logic
    experience_relevance = (
        0.4 * calculate_experience_score(resume_exp, exp_required) +
        0.3 * evaluate_relevant_experience(resume_text, jd_skills) +
        0.2 * title_match_score(resume_text, jd_title) +
        0.1 * leadership_mention_score(resume_text)
    )

    soft_skills = {   "adaptability", "collaboration", "communication", "creativity", "critical thinking", "decision making", "emotional intelligence", "empathy", "leadership", "negotiation", "organization", "problem solving", "teamwork", "time management", "work ethic", "flexibility", "conflict resolution", "accountability", "active listening", "attention to detail", "cooperation", "dependability", "discipline", "initiative", "interpersonal skills", "resilience", "resourcefulness", "self-awareness", "stress management", "verbal communication", "written communication", "positivity", "motivation", "curiosity", "open-mindedness", "self-confidence", "constructive criticism", "risk management", "strategic thinking", "customer service", "delegation", "project management", "goal setting", "business etiquette", "persuasiveness", "tactfulness", "inclusivity", "diversity awareness", "presentation skills", "cultural intelligence", "mentoring", "coaching", "assertiveness", "patience", "public speaking", "influence", "clarity", "sense of humor", "mindfulness", "self-discipline", "proactive mindset", "team building", "diplomacy", "analytical mindset", "prioritization", "design thinking", "multitasking", "perspective taking", "learning agility", "self-motivation", "body language awareness", "growth mindset", "feedback reception", "task ownership", "inspirational speaking", "information sharing", "storytelling", "professionalism", "change management", "value alignment", "process orientation", "initiative at work", "rapport building", "barrier handling", "self-reflection", "credibility", "relationship nurturing", "ethical communication", "honesty", "reliability", "followership", "respectfulness", "personal development", "eagerness to learn", "consensus building", "humility", "networking", "helpfulness", "meeting deadlines", "clarifying expectations"
    }
    overlap = len([s for s in soft_skills if s in resume_text.lower()])
    culture_fit = min(overlap / len(soft_skills), 1.0)

    academic_score = count_academic_points(resume_info.get("grades", [])) / 100

    screening_score = (
        experience_relevance * 0.4 +
        culture_fit * 0.2 +
        academic_score * 0.4
    )

    with st.spinner("Scoring resume against job description..."):
        time.sleep(1)

    cert_achievements = extract_certifications_and_achievements(resume_text)
    skill_depth = estimate_skill_depth(resume_text)
    career_analysis = analyze_career_path(resume_text)

    # Display key metrics
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🧐 Overall Score", f"{screening_score * 100:.1f}%")
        col2.metric("💼 Experience", f"{experience_relevance * 100:.1f}%")
        col3.metric("🤝 Culture Fit", f"{culture_fit * 100:.1f}%")
        col4.metric("🧪 Academic Performance", f"{academic_score * 100:.1f}%")

    from job_matches import get_resume_match_summary

    match_data = get_resume_match_summary(resume_text, jd_text)

    if match_data:
        summary_parts = []

        if match_data["top_score_raw"] >= 0.75:
            summary_parts.append("📌 The resume exhibits strong alignment with the core responsibilities and expectations outlined in the job description, indicating the candidate is likely well-prepared for the role with minimal additional training required.")
        elif match_data["top_score_raw"] >= 0.5:
            summary_parts.append("📌 The resume demonstrates a reasonable alignment with several key responsibilities outlined in the job description. While the candidate may require some upskilling or onboarding, they possess a foundational background suitable for the role.")
        else:
            summary_parts.append("📌 The resume shows limited alignment with the job requirements. Significant gaps in core skills or experience suggest the candidate may not yet be fully prepared for this role without substantial training or role adjustment.")

        if match_data["counts"]["Technical Skills"] >= 5:
            summary_parts.append("💻 Strong technical competency reflected through consistent mentions of industry-relevant tools, platforms, or languages, indicating a solid grasp of the role’s technical expectations.")
        else:
            summary_parts.append("💻 Limited demonstration of technical proficiency in the resume. Consider emphasizing or expanding on key tools, technologies, or platforms relevant to the desired role.")

        if match_data["counts"]["Projects"] + match_data["counts"]["Achievements"] >= 3:
            summary_parts.append("🏆 Projects and achievements highlight practical experience and initiative, demonstrating the candidate’s ability to apply knowledge effectively in real-world contexts.")
        else:
            summary_parts.append("🏆 Resume presents limited project or achievement evidence. Including more hands-on work, initiatives, or accomplishments could strengthen the demonstration of applied skills and proactive engagement.")

        summary_html = "<ul style='line-height: 1.8;'>"
        for point in summary_parts:
            summary_html += f"<li>{point}</li>"
        summary_html += "</ul>"

        st.markdown(f"""
            <div class="custom-card">
                <h4>📌 Screening Summary</h4>
                <p style='margin-bottom: 8px; color: #555;'>Key observations based on ATS alignment, skill presence, and project strength:</p>
                {summary_html}
            </div>
        """, unsafe_allow_html=True)

    cert_html = (
        "<ul>" + "".join([f"<li>{item}</li>" for item in cert_achievements]) + "</ul>"
        if cert_achievements else
        "<p>No certifications or achievements found in the specified section.</p>"
    )
    st.markdown(f"""
        <div class="custom-card">
            <h4>📜 Certifications & Achievements</h4>
            {cert_html}
        </div>
    """, unsafe_allow_html=True)

    if isinstance(career_analysis, (int, float)):
        career_html = f"""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='font-size: 20px; font-weight: bold; color: #00BFFF;'>{career_analysis * 100:.0f}%</div>
            <div style='color: #ccc;'>Estimated alignment with a defined career trajectory.</div>
        </div>
        """
    else:
        career_html = f"<p>{career_analysis}</p>"

    st.markdown(f"""
        <div class="custom-card">
            <h4>🔍 Career Path Analysis</h4>
            {career_html}
        </div>
    """, unsafe_allow_html=True)

    return screening_score
