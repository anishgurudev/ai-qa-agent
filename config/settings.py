# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Configuration ─────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "❌ GROQ_API_KEY not found in environment variables.\n"
        "Please ensure you have a .env file with GROQ_API_KEY=your_key_here"
    )

# ✅ Use crewai.LLM instead of langchain_groq.ChatGroq
from crewai import LLM

# groq_llm = LLM(
#     model="groq/llama-3.3-70b-versatile",
#     api_key=GROQ_API_KEY,
#     temperature=0.7,
#     max_tokens=2000,
#     timeout=120,
#     max_retries=3,

groq_llm = LLM(
    model="ollama/llama3.2",              # ✅ runs locally, zero cost
    # model="ollama/llama3.1:8b",   # Much better quality & speed
    base_url="http://localhost:11434",    # Ollama default port
    temperature=0.7,
    max_tokens=1500,
    timeout=7200,
)

# ── File Paths ─────────────────────────────────────────────────
OUTPUT_DIR = "output"
EXCEL_FILENAME = "test_cases.xlsx"
EXCEL_PATH = f"{OUTPUT_DIR}/{EXCEL_FILENAME}"

# ── Agent Behaviour ────────────────────────────────────────────
AGENT_VERBOSE = True
MAX_ITERATIONS = 10
