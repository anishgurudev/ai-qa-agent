# tasks.py
from crewai import Task
from agents import prd_analyst, test_case_designer

def create_tasks(prd_text: str) -> list:

    # ── Task 1: Analyze PRD ────────────────────────────────────
    analyze_task = Task(
        description=f"""
Analyze the PRD document below carefully.

=== PRD DOCUMENT START ===
{prd_text}
=== PRD DOCUMENT END ===

Your output must include:
1. A numbered list of ALL functional requirements
2. A numbered list of non-functional requirements
3. Key edge cases and boundary conditions
""",
        expected_output="A structured, numbered list of all testable requirements.",
        agent=prd_analyst
    )

    # ── Task 2: Design Test Cases ──────────────────────────────
    design_task = Task(
        description="""
YOU MUST OUTPUT ONLY A RAW JSON ARRAY. NO TEXT BEFORE OR AFTER.

EXAMPLE FORMAT (follow exactly):
[{{"test_id":"TC_001","module":"Login","test_scenario":"Valid login","test_steps":"1. Open app\\n2. Enter email\\n3. Click Login","expected_result":"User redirected to dashboard","priority":"High","test_type":"Functional"}},{{"test_id":"TC_002","module":"Login","test_scenario":"Invalid password","test_steps":"1. Open app\\n2. Enter wrong password\\n3. Click Login","expected_result":"Error shown","priority":"High","test_type":"Negative"}}]

RULES:
- Output ONLY the JSON array (starts with [ ends with ])
- NO explanations, NO markdown, NO backticks
- Each object needs exactly 7 keys: test_id, module, test_scenario, test_steps, expected_result, priority, test_type
- Cover top 20 critical requirements (10 positive + 10 negative)
- Keep test_steps short (max 4 steps)

START YOUR RESPONSE WITH [ AND END WITH ]
""",
        expected_output="A raw JSON array of 20 test cases, nothing else.",
        agent=test_case_designer,
        context=[analyze_task]
    )


    # # ── Task 3: Write Excel ────────────────────────────────────
    # excel_task = Task(
    #     description="""
    # Your ONLY job is to call the tool "Write Test Cases to Excel".
    #
    # Follow these steps EXACTLY:
    #
    # STEP 1 — Format the test cases as a pure JSON array like this:
    # [
    #   {
    #     "test_id": "TC_001",
    #     "module": "Login",
    #     "test_scenario": "Valid login with correct credentials",
    #     "test_steps": "1. Open login page\n2. Enter valid email\n3. Enter valid password\n4. Click Login",
    #     "expected_result": "User is redirected to dashboard",
    #     "priority": "High",
    #     "test_type": "Functional"
    #   }
    # ]
    #
    # STEP 2 — Call the tool with ONLY the raw JSON array above.
    # - NO explanations before or after
    # - NO markdown code fences (no backticks)
    # - ONLY the [ ... ] array
    #
    # STEP 3 — Return the tool's response message.
    # """,
    #     expected_output=(
    #         "A confirmation message stating the Excel file was saved "
    #         "successfully, with the file path and number of test cases written."
    #     ),
    #     agent=excel_formatter,
    #     context=[design_task]
    # )

    return [analyze_task, design_task]
