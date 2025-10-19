from crewai import Agent, Task
from utils.config import get_llm

llm = get_llm(temperature=0.3)

def get_resume_cl_agent():
    return Agent(
        role="Resume & Cover Letter Writer",
        goal="Customize application materials to match job descriptions",
        backstory="You're an expert in professional writing and tailoring resumes for job applications, especially in government and tech roles.",
        llm=llm,
        verbose=True
    )

def create_resume_cl_task(agent, job_summary, resume_text):
    return Task(
        description=f"""
        Based on the job summary below, tailor the candidate's resume summary and generate a personalized cover letter.
        
        --- Job Summary ---
        {job_summary}
        
        --- Resume Text ---
        {resume_text}
        
        Your output should include:
        1. Updated professional summary for resume
        2. A personalized cover letter suitable for a government job
        """,
        agent=agent,
        expected_output="""
        <<RESUME_SUMMARY>>
        [Your tailored 3-5 sentence resume summary here]

        <<COVER_LETTER>>
        [Your personalized cover letter here]
        """,
        output_file='/job_hunt_assistant/data/resume_agent_outputs/resume_agent_output.txt'
    )