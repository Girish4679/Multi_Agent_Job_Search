# Job Hunt Assistant

A small Python-based agent that helps automate job searching and shortlisting. It provides:  
- A Streamlit front end for interactive searches.  
- Connectors to external job APIs (currently USAJobs).  
- Modular agents for fetching, parsing, and ranking job postings.  

## Quick Start

1. **Activate the virtual environment** (included) or create a new one:
```bash
# Use the included venv
source agent_job_hunt/bin/activate

# OR create a new venv
python -m venv .venv
source .venv/bin/activate
pip install -r job_hunt_assistant/requirements.txt
```

2. **Configure environment variables**

Copy .env and add required API keys.

3. **Run Streamlit inteface locally**
```bash 
python -m streamlit run job_hunt_assistant/streamlit_app.py
```

4. **Orchestrate automated workflows:**

Use orchestrator.py to run end-to-end pipelines (fetch → parse → rank → save).

## Future Work
* Replace sample resume and bio with real data.
* Improve the interface: add download buttons, store multiple applications.
* Deploy the app via Streamlit Community Cloud or Hugging Face Spaces.