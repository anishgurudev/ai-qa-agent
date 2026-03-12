# tests/test_crew.py
import json

def test_excel_tool_with_sample_data():
    """Tests the Excel tool with 2 sample test cases."""
    from tools import write_excel_tool
    import os

    sample = [
        {
            "test_id": "TC_001",
            "module": "Login",
            "test_scenario": "Valid login with correct credentials",
            "test_steps": "1. Open app\n2. Enter valid email\n3. Enter valid password\n4. Click Login",
            "expected_result": "User is redirected to dashboard",
            "priority": "High",
            "test_type": "Functional"
        },
        {
            "test_id": "TC_002",
            "module": "Login",
            "test_scenario": "Login with wrong password",
            "test_steps": "1. Open app\n2. Enter valid email\n3. Enter wrong password\n4. Click Login",
            "expected_result": "Error message: Invalid credentials",
            "priority": "High",
            "test_type": "Negative"
        }
    ]

    result = write_excel_tool(json.dumps(sample))
    assert "SUCCESS" in result
    assert os.path.exists("output/test_cases.xlsx")
    print("✅ Test passed:", result)

if __name__ == "__main__":
    test_excel_tool_with_sample_data()
