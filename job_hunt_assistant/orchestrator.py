from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent, create_id_analysis_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from usajobs_api import fetch_usajobs
from utils.config import get_llm

llm = get_llm()

def load_resume(file_path='data/sample_resume.txt'):
    with open(file_path, 'r') as f:
        return f.read()

def run_pipeline():
    keyword = "business analyst"
    job_posts = fetch_usajobs(keyword=keyword, location="Washington, DC")
    if not job_posts:
        print("No job postings found for ", keyword)
        return

    job_data = job_posts[0]['MatchedObjectDescriptor']
    job_summary = job_data['UserArea']['Details']['JobSummary']
    agency_name = job_data.get('OrganizationName', 'Unknown Agency')
    job_title = job_data.get('PositionTitle', 'Unknown Position')

    # Load resume and bio
    resume_text = load_resume()
    user_bio = "I'm a data professional passionate about public service."

    # Initialize Agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Create Tasks
    jd_task = create_id_analysis_task(jd_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)
    message_task = create_messaging_task(messaging_agent, job_summary, agency_name, user_bio)

    jd_crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, message_task],
        llm=llm,
        process=Process.sequential
    )

    res = jd_crew.kickoff()
    print("\n=== FINAL OUTPUT ===\n")
    print(res)


if __name__ == "__main__":
    run_pipeline()