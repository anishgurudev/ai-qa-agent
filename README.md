# 🤖 AI QA Agent — PRD to Excel Test Cases

An Agentic AI assistant built with **CrewAI + Groq + Gradio** that reads a
Product Requirements Document (PRD) and automatically generates structured,
downloadable Excel test cases through a simple chat interface.

---

## 🧠 How It Works

```
User pastes PRD → 3 AI Agents collaborate → Excel file downloaded
```

| Agent | Role | Job |
|---|---|---|
| 🔍 PRD Analyst | Business Analyst | Extracts all testable requirements |
| 🧪 Test Case Designer | QA Engineer | Designs positive, negative & boundary tests |
| 📊 Excel Formatter | Doc Specialist | Writes structured `.xlsx` file |

---

## 🆓 100% Free Stack

| Tool | Purpose | Cost |
|---|---|---|
| [CrewAI](https://crewai.com) | Agent orchestration | Free & Open Source |
| [Groq API](https://console.groq.com) | LLM (LLaMA 3.3 70B) | Free tier |
| [Gradio](https://gradio.app) | Chat UI | Free & Open Source |
| [openpyxl](https://openpyxl.readthedocs.io) | Excel writer | Free & Open Source |

---

## 📁 Project Structure

```
ai-qa-agent/
├── main.py           ← Gradio chat UI (run this)
├── agents.py         ← 3 CrewAI agent definitions
├── tasks.py          ← 3 task definitions with context chain
├── crew.py           ← Crew assembly & kickoff
├── tools/
│   └── excel_tool.py ← Custom agent tool for writing Excel
├── config/
│   └── settings.py   ← Centralized config (model, paths)
├── output/           ← Generated Excel files saved here
├── tests/
│   └── test_crew.py  ← Unit tests
├── .env              ← API keys (never commit!)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone / Download the project
```bash
git clone <your-repo-url>
cd ai-qa-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your FREE Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up → API Keys → Create API Key

### 4. Add your key to `.env`
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app
```bash
python main.py
```

Open the URL printed in your terminal (e.g., `http://127.0.0.1:7860`).
Use `share=True` URL to share with your QA team.

---

## 📊 Excel Output Columns

| Test ID | Module | Test Scenario | Test Steps | Expected Result | Priority | Test Type |
|---|---|---|---|---|---|---|
| TC_001 | Login | Valid login | 1. Open app... | Dashboard shown | 🔴 High | Functional |
| TC_002 | Login | Wrong password | 1. Open app... | Error message | 🔴 High | Negative |

---

## ✅ Running Tests

```bash
python tests/test_crew.py
```

---

## 🔧 Configuration

Edit `config/settings.py` to:
- Switch LLM model (e.g., `groq/mixtral-8x7b-32768`)
- Change output Excel file path
- Toggle agent verbose logging

---

## 📌 Requirements

- Python 3.10+
- Free Groq API key
- Internet connection (calls Groq API)

---

## 👨‍💻 Built For

QA teams who want to **accelerate test coverage** during requirement analysis
without manually writing every test case from scratch.

---

*Built with ❤️ using CrewAI + Groq + Gradio*
