from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from usajobs_api import fetch_usajobs
from utils.config import get_llm
from utils.tracking import log_application, save_cover_letter_file


llm = get_llm()

def load_resume(file_path='data/sample_resume.txt'):
    with open(file_path, 'r') as f:
        return f.read()

def extract_between_markers(text, start_marker, end_marker=None):
    try:
        start_index = text.index(start_marker) + len(start_marker)
        end_index = text.index(end_marker, start_index) if end_marker else len(text)
        return text[start_index:end_index].strip()
    except ValueError:
        return "Not Found"

def run_pipeline(job_data, resume_text, user_bio):
    # Fetch job details
    job_summary = job_data['UserArea']['Details']['JobSummary']
    agency_name = job_data.get('OrganizationName', 'Unknown Agency')
    job_title = job_data.get('PositionTitle', 'Unknown Position')

    # Initialize Agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Create Tasks
    jd_task = create_jd_analysis_task(jd_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)
    message_task = create_messaging_task(messaging_agent, job_summary, agency_name, user_bio)

    # Run the crew
    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, message_task],
        llm=llm,
        process=Process.sequential
    )
    res = crew.kickoff()

    # Extract key outputs
    resume_task_output = str(resume_task.output)
    resume_summary = extract_between_markers(resume_task_output, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
    cover_letter = extract_between_markers(resume_task_output, "<<COVER_LETTER>>")    

    # Log and save
    log_application(job_title, agency_name, resume_summary)
    save_cover_letter_file(job_title, cover_letter)
    
    print("\n=== FINAL OUTPUT ===\n")
    print(res)

    return res

if __name__ == "__main__":
    run_pipeline()