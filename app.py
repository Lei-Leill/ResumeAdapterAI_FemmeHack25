import streamlit as st
import re

# Simple function to calculate match score based on keyword overlap
def calculate_match(resume, job_desc):
    resume_words = set(re.findall(r'\w+', resume.lower()))
    job_desc_words = set(re.findall(r'\w+', job_desc.lower()))
    
    common_words = resume_words.intersection(job_desc_words)
    match_score = len(common_words) / len(job_desc_words) * 100  # A simple match percentage
    return match_score

# Streamlit UI
st.title('Resume and Job Description Match')

# File uploader for the resume
resume_file = st.file_uploader("Upload your Resume", type=['txt', 'pdf'])
job_desc = st.text_area("Job Description", height=200)

# Display the match score when the user clicks the button
if resume_file is not None and job_desc:
    # Read resume content
    if resume_file.type == "text/plain":
        resume_text = resume_file.read().decode("utf-8")
    else:
        st.error("Please upload a .txt file.")
    
    # Calculate and display the match score
    score = calculate_match(resume_text, job_desc)
    st.write(f"Match Score: {score:.2f}%")
