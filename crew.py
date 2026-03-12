# crew.py
from crewai import Crew, Process
from agents import prd_analyst, test_case_designer, excel_formatter
from tasks import create_tasks

def run_crew(prd_text: str) -> str:
    """
    Assembles the crew, runs the full pipeline for the given PRD,
    and returns the final output string.
    """
    tasks = create_tasks(prd_text)

    crew = Crew(
        agents=[prd_analyst, test_case_designer, excel_formatter],
        tasks=tasks,
        process=Process.sequential,  # Task 1 → Task 2 → Task 3 in order
        verbose=True
    )

    result = crew.kickoff()
    return str(result)
