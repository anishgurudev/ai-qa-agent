# main.py  ← Run this file to start the app
import gradio as gr
import os
from crew import run_crew
from config.settings import EXCEL_PATH

# ── Core Processing Function ───────────────────────────────────
def generate_test_cases(prd_text: str, history: list):
    """Called when user clicks Generate button."""

    # Guard: empty input
    if not prd_text or not prd_text.strip():
        history.append({"role": "assistant", "content": "⚠️ Please paste your PRD text first."})
        yield history, None
        return

    # Show "working" message immediately
    history.append({"role": "user",      "content": f"📄 PRD submitted ({len(prd_text)} characters)"})
    history.append({"role": "assistant", "content": "⏳ Agents are working... This takes ~few minutes .\n\n🔍 Agent 1 → Analyzing PRD\n🧪 Agent 2 → Designing test cases\n📊 Agent 3 → Writing Excel file"})
    yield history, None

    # Run the CrewAI pipeline
    try:
        result = run_crew(prd_text)

        # ✅ Python writes Excel directly — no LLM tool needed
        from tools.excel_tool import write_excel_tool
        excel_result = write_excel_tool.run(result)

        if os.path.exists(EXCEL_PATH):
            response = (
                f"✅ **Test cases generated successfully!**\n\n"
                f"📊 {excel_result}\n\n"
                f"📥 **Your Excel file is ready to download below.**"
            )
            history.append({"role": "assistant", "content": response})
            yield history, EXCEL_PATH
        else:
            history.append({"role": "assistant", "content": f"⚠️ {excel_result}\n\nRaw output:\n{result[:500]}"})
            yield history, None

    except Exception as e:
        history.append({"role": "assistant", "content": f"❌ **Error:** {str(e)}"})
        yield history, None

    # try:
    #     result = run_crew(prd_text)
    #
    #     if os.path.exists(EXCEL_PATH):
    #         response = (
    #             f"✅ **Test cases generated successfully!**\n\n"
    #             f"📊 **Agent Summary:**\n{result[:500]}{'...' if len(result) > 500 else ''}\n\n"
    #             f"📥 **Your Excel file is ready to download below.**"
    #         )
    #         history.append({"role": "assistant", "content": response})
    #         yield history, EXCEL_PATH
    #     else:
    #         history.append({"role": "assistant", "content": f"⚠️ Crew finished but Excel not found.\n\nRaw output:\n{result}"})
    #         yield history, None
    #
    # except Exception as e:
    #     history.append({"role": "assistant", "content": f"❌ **Error:** {str(e)}\n\nCheck your GROQ_API_KEY in .env file."})
    #     yield history, None


# ── Gradio UI ──────────────────────────────────────────────────
with gr.Blocks(
    title="AI QA Agent — PRD to Test Cases",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown("""
    # 🤖 AI QA Agent
    ### PRD → Structured Excel Test Cases
    Paste any Product Requirements Document and get a ready-to-use Excel test case sheet in seconds.
    """)

    with gr.Row():
        # Left Panel: Input
        with gr.Column(scale=1):
            prd_input = gr.Textbox(
                label="📄 Paste Your PRD Here",
                placeholder=(
                    "Example:\n"
                    "Feature: User Login\n"
                    "- User can log in with email & password\n"
                    "- Password must be 8+ characters\n"
                    "- After 3 failed attempts, account locks for 15 min\n"
                    "- Forgot password link sends OTP to registered email"
                ),
                lines=18,
                max_lines=30
            )
            generate_btn = gr.Button(
                "🚀 Generate Test Cases",
                variant="primary",
                size="lg"
            )
            download_output = gr.File(
                label="📥 Download Excel File",
                visible=True
            )

        # Right Panel: Chat
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(
                label="💬 Agent Activity Log",
                height=500,
                type="messages"  # Modern message format
            )

    # Wire button to function
    generate_btn.click(
        fn=generate_test_cases,
        inputs=[prd_input, chatbot],
        outputs=[chatbot, download_output]
    )

    gr.Markdown("""
    ---
    **Free tier powered by:** [Groq](https://console.groq.com) (LLaMA 3.3 70B) + CrewAI + openpyxl
    """)

# ── Launch ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Starting AI QA Agent...")
    print(f"📁 Excel output will be saved to: {EXCEL_PATH}")
    demo.launch(
        share=True,     # Creates a public URL for sharing with your QA team
        show_error=True,
    )
