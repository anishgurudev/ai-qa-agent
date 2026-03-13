# agents.py
import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

from config.settings import groq_llm

# ── Agent 1: PRD Analyst ────────────────────────────────────
prd_analyst = Agent(
    role="Business Analyst / Product Manager",
    goal="Thoroughly analyze PRD documents and extract ALL functional and non-functional requirements",
    backstory=(
        "You are a senior product analyst with 10+ years of experience extracting "
        "requirements from product documents. You are meticulous about identifying "
        "every requirement, edge case, and user flow."
    ),
    llm=groq_llm,
    max_iter=3,
    verbose=True,
    allow_delegation=False
)

# ── Agent 2: Test Case Designer ─────────────────────────────
test_case_designer = Agent(
    role="QA Engineer / Test Designer",
    goal="Design structured test cases and output them as a raw JSON array only",
    backstory=(
        "You are an expert QA engineer with deep knowledge of test design methodologies "
        "(boundary value analysis, equivalence partitioning, etc.). You create test cases "
        "that are thorough, well-structured, and easy to execute. Every requirement gets "
        "both positive and negative test coverage."
        "You are an expert QA engineer who outputs test cases strictly as a "
        "raw JSON array with no extra text, no markdown, no explanation."
    ),
    llm=groq_llm,
    max_iter=3,
    verbose=True,
    allow_delegation=False
)
