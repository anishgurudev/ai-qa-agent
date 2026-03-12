# agents.py
import os
from dotenv import load_dotenv
from crewai import Agent
from tools.excel_tool import write_excel_tool

# Load environment variables FIRST before any config imports
load_dotenv()

# Now import config after environment is loaded (this creates the LLM client)
from config.settings import groq_llm
from tools.excel_tool import write_excel_tool

# ── Agent 1: PRD Analyst ────────────────────────────────────
prd_analyst = Agent(
    role="Business Analyst / Product Manager",
    goal="Thoroughly analyze PRD documents and extract ALL functional and non-functional requirements",
    backstory=(
        "You are a senior product analyst with 10+ years of experience extracting "
        "requirements from product documents. You are meticulous about identifying "
        "every requirement, edge case, and user flow. Your analysis is the foundation "
        "for comprehensive test coverage."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

# ── Agent 2: Test Case Designer ─────────────────────────────
test_case_designer = Agent(
    role="QA Engineer / Test Designer",
    goal="Design comprehensive, detailed test cases covering all requirements with positive, negative, and boundary cases",
    backstory=(
        "You are an expert QA engineer with deep knowledge of test design methodologies "
        "(boundary value analysis, equivalence partitioning, etc.). You create test cases "
        "that are thorough, well-structured, and easy to execute. Every requirement gets "
        "both positive and negative test coverage."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

# ── Agent 3: Excel Formatter ────────────────────────────────
excel_formatter = Agent(
    role="Test Documentation Specialist",
    goal="Convert test case data into a well-formatted, professional Excel spreadsheet",
    backstory=(
        "You are a documentation expert who specializes in organizing test cases into "
        "readable, professional Excel formats. You ensure proper formatting, styling, "
        "and validation before saving. You use the Excel writing tool to create files "
        "that QA teams can immediately use."
    ),
    tools=[write_excel_tool],
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)
