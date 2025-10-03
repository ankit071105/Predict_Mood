# 📁 job_matches.py

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from math import pi
from faiss_engine import find_top_matches
from nlp_utils import count_categories


def show_job_matches(resume_text, jd_text):
    st.markdown("<h2 class='section-title fade-in-up'>📊 Role Compatibility Analysis</h2>", unsafe_allow_html=True)

    jd_list = jd_text
    if not jd_list:
        st.error("❌ No valid job descriptions found.")
        return

    # Get top matching JDs via FAISS
    with st.spinner("🔭 Scanning for optimal matches..."):
        top_matches = find_top_matches(resume_text, jd_list, top_k=3)
    
    # Display top match score
    if top_matches:
        # Clamp the top score to stay within [0, 1] for pie chart stability
        top_score_raw = top_matches[0]["score"]
        top_score = max(0.0, min(top_score_raw, 1.0))

        # Enhanced metric display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="plot-container pulse" style="text-align: center;">
                <h4 style="color: #3498db; margin-bottom: 10px;">🔍 Top Match Score</h4>
                <div style="font-size: 2.5rem; font-weight: bold; color: #3498db; 
                            text-shadow: 0 0 10px rgba(52, 152, 219, 0.5);">
                    {top_score_raw * 100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if top_score_raw > 0.7:
                status_icon = "✅"
                status_text = "Strong Match"
                status_color = "#2ecc71"
            elif top_score_raw > 0.4:
                status_icon = "⚠️"
                status_text = "Moderate Match"
                status_color = "#f39c12"
            else:
                status_icon = "❌"
                status_text = "Low Match"
                status_color = "#e74c3c"
                
            st.markdown(f"""
            <div class="plot-container" style="text-align: center;">
                <h4 style="color: {status_color}; margin-bottom: 10px;">{status_icon} Compatibility Status</h4>
                <div style="font-size: 1.2rem; font-weight: bold; color: {status_color};">
                    {status_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Skill overlap percentage
        resume_words = set(re.findall(r"\w+", resume_text.lower()))
        jd_words = set(re.findall(r"\w+", " ".join(jd_list).lower()))
        common = resume_words.intersection(jd_words)
        common_skills = [word for word in common if len(word) > 3]
        skill_overlap_pct = len(common_skills) / max(len(jd_words), 1) * 100
        
        with col3:
            st.markdown(f"""
            <div class="plot-container" style="text-align: center;">
                <h4 style="color: #9b59b6; margin-bottom: 10px;">🧠 Skill Overlap</h4>
                <div style="font-size: 2.5rem; font-weight: bold; color: #9b59b6; 
                            text-shadow: 0 0 10px rgba(155, 89, 182, 0.5);">
                    {skill_overlap_pct:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Enhanced Pie Chart with 3D effect
        with st.container():
            st.markdown("<div class='plot-container fade-in-up'><h4>📈 Compatibility Score Visualization</h4>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(8, 8))
            
            # Create a 3D-like pie chart
            explode = (0.05, 0)  # slight explode for the match portion
            colors = ['#3498db', '#2c3e50']
            wedges, texts, autotexts = ax1.pie(
                [top_score, 1 - top_score],
                explode=explode,
                labels=["Match", "Gap"],
                autopct='%1.1f%%',
                colors=colors,
                startangle=90,
                shadow=True,
                textprops={'fontsize': 12, 'color': 'white', 'weight': 'bold'}
            )
            
            # Enhance the pie chart with 3D effect
            for w in wedges:
                w.set_edgecolor('white')
                w.set_linewidth(2)
                w.set_alpha(0.9)
                
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
                autotext.set_fontsize(14)
                
            # Add a center circle for a donut chart effect
            centre_circle = plt.Circle((0,0),0.70,fc='#0a0e17')
            fig1.gca().add_artist(centre_circle)
            
            # Set background color
            ax1.set_facecolor('#0a0e17')
            fig1.patch.set_facecolor('#0a0e17')
            
            ax1.axis('equal')
            plt.tight_layout()
            st.pyplot(fig1)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No top matches found to visualize.")

    # 📊 Enhanced Visualizations
    counts = count_categories(resume_text)

    # Radar chart for skills analysis
    with st.container():
        st.markdown("<div class='plot-container fade-in-up'><h4>📡 Skill Distribution Analysis</h4>", unsafe_allow_html=True)
        
        categories = ['Technical', 'Soft Skills', 'Education', 'Projects', 'Experience', 'Achievements']
        values = [
            counts["Technical Skills"], 
            counts["Soft Skills"], 
            counts["Education"], 
            counts["Projects"], 
            counts["Experience"],
            counts["Achievements"]
        ]
        
        # Scale values for better visualization
        max_val = max(values) if max(values) > 0 else 1
        values = [v/max_val * 100 for v in values]
        
        # Compute angle for each category
        angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
        angles += angles[:1]
        values += values[:1]
        
        fig2, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Plot data
        ax.plot(angles, values, linewidth=2, linestyle='solid', color='#3498db', marker='o', markersize=8)
        ax.fill(angles, values, alpha=0.4, color='#3498db')
        
        # Add labels
        ax.set_thetagrids([a * 180/pi for a in angles[:-1]], categories, color='white', fontsize=11, weight='bold')
        
        # Set yticks
        ax.set_rlabel_position(30)
        plt.yticks([25, 50, 75, 100], ["25%", "50%", "75%", "100%"], color="white", size=10)
        plt.ylim(0, 100)
        
        # Add grid
        ax.grid(True, color='rgba(255, 255, 255, 0.2)', linestyle='--', linewidth=0.5)
        
        # Set background color
        ax.set_facecolor('#0a0e17')
        fig2.patch.set_facecolor('#0a0e17')
        
        plt.tight_layout()
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced bar charts with 3D effect
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='plot-container fade-in-up'><h4>📊 Skills & Education Distribution</h4>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        categories = ["Technical Skills", "Soft Skills", "Education"]
        values = [counts["Technical Skills"], counts["Soft Skills"], counts["Education"]]
        
        # Create gradient bars
        bars = ax3.bar(categories, values, color=['#3498db', '#9b59b6', '#2ecc71'], alpha=0.8, edgecolor='white', linewidth=2)
        
        # Add value labels on top of bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{values[i]}', ha='center', va='bottom', color='white', fontweight='bold')
        
        # Customize the chart
        ax3.set_ylabel('Count', fontweight='bold', color='white')
        ax3.tick_params(axis='x', labelrotation=45, colors='white')
        ax3.tick_params(axis='y', colors='white')
        
        # Set background color
        ax3.set_facecolor('#0a0e17')
        fig3.patch.set_facecolor('#0a0e17')
        
        # Add grid
        ax3.grid(True, color='rgba(255, 255, 255, 0.1)', linestyle='--', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig3)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='plot-container fade-in-up'><h4>📚 Experience & Achievements</h4>", unsafe_allow_html=True)
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        
        categories = ["Projects", "Achievements", "Experience"]
        values = [counts["Projects"], counts["Achievements"], counts["Experience"]]
        
        # Create gradient bars
        bars = ax4.bar(categories, values, color=['#e74c3c', '#f39c12', '#1abc9c'], alpha=0.8, edgecolor='white', linewidth=2)
        
        # Add value labels on top of bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{values[i]}', ha='center', va='bottom', color='white', fontweight='bold')
        
        # Customize the chart
        ax4.set_ylabel('Count', fontweight='bold', color='white')
        ax4.tick_params(axis='x', labelrotation=45, colors='white')
        ax4.tick_params(axis='y', colors='white')
        
        # Set background color
        ax4.set_facecolor('#0a0e17')
        fig4.patch.set_facecolor('#0a0e17')
        
        # Add grid
        ax4.grid(True, color='rgba(255, 255, 255, 0.1)', linestyle='--', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig4)
        st.markdown("</div>", unsafe_allow_html=True)

    # Matched keywords with enhanced visualization
    with st.expander("🧩 Keyword Alignment Analysis (Click to Expand)", expanded=False):
        if common_skills:
            # Create a tag cloud effect
            st.markdown("### 📍 Shared Keywords Found")
            
            # Group skills by length for visualization
            col1, col2, col3 = st.columns(3)
            skills_by_col = [common_skills[i::3] for i in range(3)]
            
            for idx, col in enumerate([col1, col2, col3]):
                with col:
                    for skill in skills_by_col[idx]:
                        # Vary the badge style based on skill length
                        if len(skill) > 8:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #3498db, #2980b9);
                                        padding: 8px 12px; margin: 5px 0; border-radius: 20px;
                                        text-align: center; color: white; font-weight: bold;
                                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                                {skill.title()}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #9b59b6, #8e44ad);
                                        padding: 8px 12px; margin: 5px 0; border-radius: 20px;
                                        text-align: center; color: white; font-weight: bold;
                                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                                {skill.title()}
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("No significant keyword overlap found between resume and job description.")

    # Display Top JD Matches with enhanced UI
    with st.expander("📋 Top Matching Opportunities (FAISS Analysis)", expanded=False):
        for i, match in enumerate(top_matches):
            # Different colors for different ranks
            if i == 0:
                color = "#2ecc71"  # Green for top match
                icon = "🥇"
            elif i == 1:
                color = "#f39c12"  # Orange for second
                icon = "🥈"
            else:
                color = "#3498db"  # Blue for third
                icon = "🥉"
                
            jd_preview = match["job_description"][:200].replace("\n", " ").strip()
            
            st.markdown(f"""
            <div style="background: rgba(18, 25, 40, 0.7); padding: 15px; border-radius: 10px; 
                        border-left: 5px solid {color}; margin-bottom: 15px;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="color: {color}; margin: 0;">{icon} Match: {match['score'] * 100:.2f}%</h4>
                    <div style="background: {color}; color: white; padding: 5px 10px; 
                                border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                        Rank #{i+1}
                    </div>
                </div>
                <p style="color: #bdc3c7; margin-top: 10px;">{jd_preview}...</p>
            </div>
            """, unsafe_allow_html=True)

# for the summary logic
def get_resume_match_summary(resume_text, jd_text):
    jd_list = jd_text if isinstance(jd_text, list) else [jd_text]
    if not jd_list:
        return None

    top_matches = find_top_matches(resume_text, jd_list, top_k=3)
    top_score_raw = top_matches[0]["score"] if top_matches else 0.0
    top_score = max(0.0, min(top_score_raw, 1.0))

    resume_words = set(re.findall(r"\w+", resume_text.lower()))
    jd_words = set(re.findall(r"\w+", " ".join(jd_list).lower()))
    common_skills = [word for word in resume_words.intersection(jd_words) if len(word) > 3]
    skill_overlap_pct = len(common_skills) / max(len(jd_words), 1) * 100

    counts = count_categories(resume_text)

    return {
        "top_score": top_score,
        "top_score_raw": top_score_raw,
        "skill_overlap_pct": skill_overlap_pct,
        "counts": counts,
    }