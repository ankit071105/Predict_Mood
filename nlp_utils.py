import re
from sentence_transformers import SentenceTransformer, util

_sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_recommendation(text1, text2):
    emb1 = _sbert_model.encode(text1, convert_to_tensor=True)
    emb2 = _sbert_model.encode(text2, convert_to_tensor=True)
    return round(util.pytorch_cos_sim(emb1, emb2).item(), 3)

def extract_certifications_and_achievements(resume_text):
    lines = resume_text.splitlines()
    section_started = False
    collected_lines = []

    section_headers = [
        "certification", "certifications", "certifications & achievements",
        "achievements", "awards and certifications", "licenses", "honors"
    ]

    for i, line in enumerate(lines):
        lower_line = line.strip().lower()
        if any(header in lower_line for header in section_headers):
            section_started = True
            continue

        if section_started:
            if line.strip() == "" or re.match(r'^[A-Z][a-z]+:', line):
                break
            collected_lines.append(line.strip())

    result = [line for line in collected_lines if len(line) > 3]
    return list(set(result)) if result else []

def estimate_skill_depth(resume_text):
    skill_keywords = {
        "python": ["python", "pandas", "numpy", "scikit-learn"],
        "java": ["java", "spring", "spring boot"],
        "web development": ["html", "css", "javascript", "react", "angular", "vue", "node.js", "flask", "django"],
        "data science": ["machine learning", "deep learning", "nlp", "data analysis", "tensorflow", "pytorch"],
        "cloud": ["aws", "azure", "gcp"],
        "devops": ["docker", "kubernetes", "jenkins", "terraform"]
    }

    depth_indicators = [
        r"expert in", r"proficient in", r"hands[- ]on", r"strong background", r"deep understanding",
        r"3\+ years", r"4\+ years", r"5\+ years", r"\bexperienced\b", r"led projects", r"architected"
    ]

    resume_text = resume_text.lower()
    skill_depth_scores = {}

    for area, keywords in skill_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in resume_text:
                matches = sum(1 for phrase in depth_indicators if re.search(rf"{phrase}.*{keyword}", resume_text))
                score += matches
        normalized = min(score / len(depth_indicators), 1.0) if score > 0 else 0.0
        if normalized > 0:
            skill_depth_scores[area] = round(normalized, 2)

    return skill_depth_scores

def analyze_career_path(resume_text):
    job_levels = [
        "intern", "junior", "associate", "engineer", "developer", "senior", "lead", "manager", "architect",
        "director", "head", "vp", "chief", "cto", "ceo"
    ]

    resume_text = resume_text.lower()
    progression = [level for level in job_levels if level in resume_text]
    unique_levels = list(dict.fromkeys(progression))
    return min(len(unique_levels) / len(job_levels), 1.0)

def split_sections(text):
    sections = {}
    current_section = "General"
    sections[current_section] = []

    lines = text.splitlines()

    for line in lines:
        line_clean = line.strip()

        if re.search(r'education|educational background|academic profile|academics|scholastic|education & certifications', line_clean, re.I):
            current_section = "Education"
        elif re.search(r'project', line_clean, re.I):
            current_section = "Projects"
        elif re.search(r'training|certification', line_clean, re.I):
            current_section = "Training"
        elif re.search(r'extra[- ]?curricular|activities', line_clean, re.I):
            current_section = "Activities"

        if current_section not in sections:
            sections[current_section] = []

        if line_clean:
            sections[current_section].append(line_clean)

    return sections

def extract_skills(text, skill_set=None):
    if skill_set is None:
        skill_set = {
            "python", "java", "sql", "html", "css", "data analysis", "machine learning",
            "deep learning", "nlp", "c++", "javascript", "docker", "aws", "git", "linux"
        }

    text = text.lower()
    found_skills = {skill for skill in skill_set if skill.lower() in text}
    return list(found_skills)

def estimate_experience(text):
    matches = re.findall(r'(\d+)\+?\s+(?:years|yrs)\s+(?:of )?experience', text.lower())
    return max((int(match) for match in matches), default=0)

def extract_titles(text):
    career_keywords = [
        "intern", "trainee", "developer", "engineer", "software engineer", "senior developer",
        "team lead", "manager", "architect", "cto", "data analyst", "data scientist",
        "qa engineer", "web developer", "android developer", "ios developer", "sde",
        "ml engineer", "ai engineer", "research intern", "project manager",
        "campus ambassador", "club lead", "researcher", "lab assistant", "teaching assistant",
        "hackathon", "ideathon", "trainingship", "virtual internship", "bootcamp",
        "summer internship", "industrial training", "certification", "course completion",
        "open source contributor", "github contributor", "freelancer", "mentor", "volunteer",
        "project lead", "innovation head", "capstone project", "startup cofounder"
    ]

    text = text.lower()
    found = [keyword for keyword in career_keywords if keyword in text]
    return " → ".join(dict.fromkeys(found)) or "Career progression not found."

def count_categories(text):
    technical_skills = {"python", "java", "sql", "html", "css", "docker", "aws", "git", "linux", "javascript", "machine learning", "deep learning", "nlp"}
    soft_skills = {"communication", "teamwork", "leadership", "problem solving", "adaptability", "creativity", "critical thinking", "time management"}
    education_keywords = {"bachelor", "master", "phd", "degree", "university", "college", "school", "academy", "certificate", "certification"}
    project_keywords = {"project", "capstone", "prototype", "application", "game", "system", "website", "software", "platform"}
    achievement_keywords = {"award", "winner", "honor", "recognition", "published", "patent", "certificate", "certification"}
    experience_keywords = {"internship", "job", "work", "experience", "role", "position", "employment", "consultant", "freelance"}

    text_lower = text.lower()

    def count_hits(keywords):
        return sum(1 for kw in keywords if kw in text_lower)

    return {
        "Technical Skills": count_hits(technical_skills),
        "Soft Skills": count_hits(soft_skills),
        "Education": count_hits(education_keywords),
        "Projects": count_hits(project_keywords),
        "Achievements": count_hits(achievement_keywords),
        "Experience": count_hits(experience_keywords)
    }

def group_education_lines(lines):
    grouped = []
    current = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(keyword in line.lower() for keyword in [
            "school", "college", "university", "institute", "b.tech", "bachelor",
            "icse", "isc", "cbse", "engineering"
        ]) or re.search(r'\d{4}[-\u2013]\d{4}', line):
            if current:
                grouped.append(" | ".join(current))
                current = []
        current.append(line)

    if current:
        grouped.append(" | ".join(current))
    return grouped

def extract_basic_info(text):
    sections = split_sections(text)
    skills = extract_skills(text)

    education_section = sections.get("Education", []) + sections.get("Qualification", [])

    cleaned_education = education_section[:]
    grades_only = []

    # Robust: extract grading info from full resume text
    for line in text.splitlines():
        line_clean = line.strip()
        if re.search(r"\b(CGPA|GPA|Percentage|Grade)\b", line_clean, re.I):
            grade_match = re.search(
                r"(CGPA|GPA|Percentage|Grade)\s*[:;/\\\-]?\s*([0-9]{1,2}(\.[0-9]{1,2})?%?)",
                line_clean, re.I
            )
            if grade_match:
                grades_only.append(f"{grade_match.group(1)}: {grade_match.group(2)}")

    cleaned_education = list(dict.fromkeys([line for line in cleaned_education if len(line.strip()) > 8 and not line.strip().isdigit()]))
    grades_only = list(dict.fromkeys(grades_only))

    years_experience = estimate_experience(text)
    career_progression = extract_titles(text)

    red_flags = []
    red_flag_rules = [
        {"condition": lambda: years_experience < 1, "message": "Very low or no work experience"},
        {"condition": lambda: not cleaned_education or cleaned_education.lower() in {"n/a", "not detected", ""}, "message": "Education details missing or unclear"},
        {"condition": lambda: isinstance(cleaned_education, str) and "diploma" in cleaned_education.lower(), "message": "Only diploma-level education detected"},
        {"condition": lambda: 1 <= years_experience < 3, "message": "Junior-level experience"}
    ]

    for rule in red_flag_rules:
        try:
            if rule["condition"]():
                red_flags.append(rule["message"])
        except Exception as e:
            print(f"Red flag rule error: {e}")

    recommendations = []
    skills_recommendations = {
        "cloud": {"keywords": {"aws", "gcp", "azure", "cloud"}, "message": "Consider learning cloud technologies (AWS, GCP, Azure, etc.)"},
        "version_control": {"keywords": {"git", "github", "bitbucket"}, "message": "Include version control tools like Git in your profile."},
        "containerization": {"keywords": {"docker", "kubernetes"}, "message": "Familiarity with containerization tools (Docker, Kubernetes) is a valuable asset."},
        "testing": {"keywords": {"pytest", "unittest", "selenium", "junit"}, "message": "Include experience with testing frameworks for better code quality."},
        "soft_skills": {"keywords": {"communication", "teamwork", "leadership"}, "message": "Highlight soft skills like teamwork and communication."}
    }

    skills_text = " ".join(skills).lower()

    for category, data in skills_recommendations.items():
        if not any(keyword in skills_text for keyword in data["keywords"]):
            recommendations.append(data["message"])

    if not recommendations:
        recommendations.append("Well-rounded profile!")

    recommendation_summary = "; ".join(recommendations)
    confidence_score = min(0.5 + (0.05 * len(skills)), 1.0)

    return {
        "skills": skills,
        "education": "; ".join(group_education_lines(cleaned_education)) if cleaned_education else "Not detected",
        "grades": grades_only,
        "years_experience": years_experience,
        "career_progression": career_progression,
        "red_flags": red_flags,
        "confidence_score": confidence_score,
        "recommendations": recommendation_summary
    }

def generate_red_flags_html(red_flags):
    if not red_flags:
        return "<p>✅ No major red flags detected.</p>"
    red_flags_html = "".join(f"<li>⚠️ {flag}</li>" for flag in red_flags)
    return f"<ul>{red_flags_html}</ul><p>These points highlight possible gaps or inconsistencies that may benefit from closer review during the evaluation process. They do not automatically disqualify the candidate but can inform follow-up discussions or clarifications.</p>"

def count_academic_points(grades):
    """
    Grades: List of strings like ["CGPA: 8.9", "Percentage: 92%"]
    Returns academic performance as percentage score.
    """
    count = len(grades)
    if count >= 7:
        return 100
    elif count == 6:
        return 80
    elif count == 5:
        return 60
    elif count == 3:
        return 40
    elif count == 2:
        return 20
    elif count == 1:
        return 10
    else:
        return 0

# Inside nlp_utils.py

def calculate_experience_score(resume_exp, exp_required):
    if resume_exp >= exp_required:
        return 1.0
    elif resume_exp >= exp_required - 1:
        return 0.7
    elif resume_exp > 0:
        return 0.4
    return 0.2

def evaluate_relevant_experience(resume_text, jd_skills):
    text = resume_text.lower()
    count = sum(1 for skill in jd_skills if skill.lower() in text)
    return min(count / len(jd_skills), 1.0) if jd_skills else 0.0

def title_match_score(resume_text, jd_title):
    resume_text = resume_text.lower()
    jd_title = jd_title.lower()
    return 1.0 if jd_title in resume_text else 0.0

def leadership_mention_score(resume_text):
    leadership_terms = ["lead", "managed", "mentored", "supervised", "headed", "led team", "project lead"]
    resume_text = resume_text.lower()
    mentions = sum(1 for term in leadership_terms if term in resume_text)
    return min(mentions / len(leadership_terms), 1.0)

def extract_job_title(jd_text):
    # Try regex-based title extraction
    match = re.search(r'(?i)(we are hiring for|looking for|position:|role:)\s+([\w\s\-\/]+)', jd_text)
    if match:
        return match.group(2).strip()
    # Fallback: assume first line contains title
    return jd_text.strip().split("\n")[0][:100]
