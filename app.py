import streamlit as st
import re
from google import genai
from google.genai import types
import base64
import pdfplumber

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    
def generate_response(resume_text, job_desc):
    client = genai.Client(
        vertexai=False,
        api_key="AIzaSyAWt8blzVszVkfvlh1Rlpf8Qjn5MicEQVA",
    )

    # Text template for the Gemini AI model
    textsi_1 = """Hiring Manager & Resume Reviewer

    You are an AI-powered recruiter evaluating job applications based on a specific job description. Your role is to analyze the user's resume as if you were the hiring manager for the position. You provide detailed feedback on how well the applicant aligns with the job and what they can do to improve their chances of getting hired.

    As the recruiter, you will:

    Assess Resume Fit:
    Review the resume and compare it to the job description, noting how well it aligns.
    Identify key wording differences and suggest refinements to match industry expectations and employer preferences.
    Identify Skill Gaps:
    Essential Missing Skills: Highlight any required skills the candidate lacks and explain why they are important.
    Bonus Skills: Note skills that are preferred but not required and suggest ways to acquire them.
    Evaluate Experience Relevance:
    Determine how well the past projects of the candidate and work history match the job description.
    Highlight strengths and gaps in experience that a hiring manager would notice.
    Provide Recruiter-Style Advice:
    Offer professional recommendations on how to improve the resume and overall application based on recruiter priorities.
    Suggest concrete actions (e.g., gaining relevant experience, working on specific projects, acquiring certifications) to make them a stronger candidate.
    Your tone should be insightful, direct, and practical—just like a real recruiter giving feedback to an applicant.

    You are the AI hiring manager for this job."""

    # Combine resume text and job description for the input
    user_input = f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}"

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_input)])]

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.8,
        max_output_tokens=1024,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=textsi_1)],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-1.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text


# Streamlit UI
st.title('ScanDidate')
st.title('Scan Your Resume with an AI Hiring Manager :)')


image_path = "purple_pic.png"
with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
image_base64 =  f"data:image/webp;base64,{encoded_string}"

# Inject custom CSS to set a background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({image_base64});
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True
)

# File uploader for the resume
resume_file = st.file_uploader("Upload your Resume", type=['txt', 'pdf'])
job_desc = st.text_area("Job Description", height=200)

# Display the match score when the user clicks the button
if resume_file is not None and job_desc:
    # Read resume content
    if resume_file.type == "text/plain":
        resume_text = resume_file.read().decode("utf-8")
    elif resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    else:
        st.error("Please upload a valid .pdf or .txt file.")
    
if st.button("Generate output from our AI Expert"):
    generate_response(resume_text, job_desc)
    feedback = generate_response(resume_text, job_desc)  # Generate the feedback
    st.text_area("Feedback", feedback, height=300)  # Display the feedback