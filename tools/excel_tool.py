# tools/excel_tool.py
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from crewai.tools import tool
from config.settings import OUTPUT_DIR, EXCEL_PATH
import json, os

@tool("Write Test Cases to Excel")
def write_excel_tool(test_cases_json: str) -> str:
    """
    Accepts a JSON string of test cases and writes them into a
    formatted Excel file. Each test case must have these keys:
    test_id, module, test_scenario, test_steps, expected_result,
    priority, test_type.
    Returns a success or error message string.
    """
    # ── Step 1: Parse JSON ─────────────────────────────────────
    try:
        data = json.loads(test_cases_json)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON provided. Details: {e}"

    if not isinstance(data, list) or len(data) == 0:
        return "ERROR: JSON must be a non-empty list of test case objects."

    # ── Step 2: Create Workbook ────────────────────────────────
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    headers = [
        "Test ID", "Module", "Test Scenario",
        "Test Steps", "Expected Result", "Priority", "Test Type"
    ]

    # ── Step 3: Style Header Row ───────────────────────────────
    BLUE   = PatternFill("solid", fgColor="1F4E79")
    WHITE  = Font(bold=True, color="FFFFFF", size=11)
    CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.fill = BLUE
        cell.font = WHITE
        cell.alignment = CENTER
    ws.row_dimensions[1].height = 30

    # ── Step 4: Write Data Rows ────────────────────────────────
    PRIORITY_COLORS = {
        "high":   "FF6B6B",  # Red
        "medium": "FFD966",  # Yellow
        "low":    "92D050",  # Green
    }

    for row_num, tc in enumerate(data, 2):
        ws.cell(row=row_num, column=1, value=tc.get("test_id",        f"TC_{row_num-1:03d}"))
        ws.cell(row=row_num, column=2, value=tc.get("module",         "General"))
        ws.cell(row=row_num, column=3, value=tc.get("test_scenario",  ""))
        ws.cell(row=row_num, column=4, value=tc.get("test_steps",     ""))
        ws.cell(row=row_num, column=5, value=tc.get("expected_result",""))
        ws.cell(row=row_num, column=6, value=tc.get("priority",       "Medium"))
        ws.cell(row=row_num, column=7, value=tc.get("test_type",      "Functional"))

        # Wrap text in Steps & Expected Result columns
        ws.cell(row=row_num, column=4).alignment = Alignment(wrap_text=True)
        ws.cell(row=row_num, column=5).alignment = Alignment(wrap_text=True)

        # Color-code Priority cell
        priority_key = tc.get("priority", "medium").lower()
        color = PRIORITY_COLORS.get(priority_key, "FFFFFF")
        ws.cell(row=row_num, column=6).fill = PatternFill("solid", fgColor=color)
        ws.cell(row=row_num, column=6).alignment = Alignment(horizontal="center")

    # ── Step 5: Auto-fit Column Widths ─────────────────────────
    COLUMN_MAX_WIDTH = {"A": 10, "B": 18, "C": 35, "D": 45, "E": 45, "F": 12, "G": 18}
    for col_letter, max_w in COLUMN_MAX_WIDTH.items():
        ws.column_dimensions[col_letter].width = max_w

    # ── Step 6: Add Freeze Panes (header always visible) ───────
    ws.freeze_panes = "A2"

    # ── Step 7: Save File ──────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    wb.save(EXCEL_PATH)

    return (
        f"SUCCESS: Excel saved at '{EXCEL_PATH}' "
        f"with {len(data)} test cases written."
    )
