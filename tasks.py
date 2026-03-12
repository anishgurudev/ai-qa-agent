# tasks.py
from crewai import Task
from agents import prd_analyst, test_case_designer, excel_formatter

def create_tasks(prd_text: str) -> list:
    """
    Builds the 3-task pipeline for a given PRD text.
    Tasks run sequentially: analyze → design → format.
    """

    # ── Task 1: Analyze PRD ────────────────────────────────────
    analyze_task = Task(
        description=f"""
Analyze the PRD document below carefully and completely.

=== PRD DOCUMENT START ===
{prd_text}
=== PRD DOCUMENT END ===

Your output must include:
1. A numbered list of ALL functional requirements
2. A numbered list of non-functional requirements (performance, security, UX)
3. All user flows / journeys mentioned or implied
4. All edge cases and boundary conditions
5. Any ambiguous requirements QA should cover defensively

Be thorough. Missing a requirement here means missing test coverage later.
        """,
        expected_output=(
            "A structured, numbered list of ALL testable requirements grouped "
            "by category: Functional, Non-Functional, Edge Cases, User Flows."
        ),
        agent=prd_analyst
    )

    # ── Task 2: Design Test Cases ──────────────────────────────
    design_task = Task(
        description="""
Using the full requirements list from the Business Analyst, design test cases.

Rules:
- Each requirement must have AT LEAST: 1 positive + 1 negative test case
- Apply Boundary Value Analysis wherever inputs/limits are mentioned
- Cover integration points between modules
- Each test case MUST have all 7 fields:
  * test_id      → Format: TC_001, TC_002, ...
  * module       → Feature/module name (e.g., "Login", "Payment")
  * test_scenario → One clear sentence describing what is being tested
  * test_steps   → Numbered steps: "1. Open app\n2. Click Login..."
  * expected_result → Exact expected outcome
  * priority     → High / Medium / Low
  * test_type    → Functional / Negative / Boundary / Integration / Non-Functional
        """,
        expected_output=(
            "A complete, detailed list of test cases with all 7 fields "
            "filled for every single test case."
        ),
        agent=test_case_designer,
        context=[analyze_task]  # Receives Task 1's output as context
    )

    # ── Task 3: Write Excel ────────────────────────────────────
    excel_task = Task(
        description="""
Take the complete test case list and do the following:

STEP 1 — Build a valid JSON array.
  - Each element must have EXACTLY these keys (no extras, no missing):
    test_id, module, test_scenario, test_steps, expected_result, priority, test_type
  - Escape all special characters. No trailing commas. Valid JSON only.

STEP 2 — Call the tool "Write Test Cases to Excel" with the JSON string.

STEP 3 — Report back the tool's response (success message + file path).

IMPORTANT: Double-check your JSON is parseable before calling the tool.
        """,
        expected_output=(
            "A confirmation message stating the Excel file was saved "
            "successfully, with the file path and number of test cases written."
        ),
        agent=excel_formatter,
        context=[design_task]  # Receives Task 2's output as context
    )

    return [analyze_task, design_task, excel_task]
