from crewai import Task, Agent
from utils.config import get_llm

llm = get_llm()

def get_jd_analyst_agent():
    agent = Agent(
        role = "JD Analyst",
        goal = "Understand and summarize government job postings",
        backstory="You're an expert in job market analysis with a focus on US federal job listings.",
        llm=llm,
        verbose=True
    )
    return agent

def create_jd_analysis_task(agent, job_desc):
    task = Task(
        description=f"""
        Analyze the following USAJobs job posting and extract:
        - A summary of the role
        - Key skills required
        - Any specific qualifications or eligibility
        \n\nJob Description:\n{job_desc}
        """,
        expected_output="A structured markdown summary containing sections for Qualifications, Required Skills, and Responsibilities.",
        agent=agent,
        output_file='data/report.md'
    )
    return task