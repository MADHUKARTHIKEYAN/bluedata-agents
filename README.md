# 🌊 BlueData Agent

> **AI-powered conversational intelligence platform for marine and ocean data**

BlueData Agent is a multi-agent AI system designed to make marine and oceanographic information easier to access through natural-language conversations.

The system combines **LangGraph**, **LLMs, marine data tools, weather information, and safety intelligence** to understand user queries, decide which tools are required, execute the appropriate tasks, and generate a useful response.

---

## 🚀 Features

* 🤖 **AI-powered conversational interface**
* 🧠 **LangGraph-based agent orchestration**
* 🌊 Marine and ocean data analysis
* 🌦️ Weather information retrieval
* 🛟 Marine safety intelligence
* 🔀 AI model routing
* 🔗 Modular tool architecture
* 🧩 Separate service layer for AI providers
* 🧪 Local graph testing using `test_graph.py`
* ⚡ FastAPI backend support

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      User Query     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangGraph Agent   │
                         │   Orchestrator      │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   Intent / Planning │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             ┌───────────┐   ┌───────────┐   ┌───────────┐
             │   Marine  │   │  Weather  │   │   Safety  │
             │   Tool    │   │   Tool    │   │   Tool    │
             └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │   AI Model Layer    │
                         │ Gemini / Groq /      │
                         │ Sarvam               │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Final AI Response  │
                         └─────────────────────┘
```

---

## 📁 Project Structure

```text
bluagents/
│
├── app/
│   ├── api.py
│   ├── main.py
│   ├── test_graph.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai.py
│   │   ├── ai_router.py
│   │   ├── gemini.py
│   │   ├── groq.py
│   │   └── sarvam.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── marine.py
│       ├── safety.py
│       └── weather.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 Agent Workflow

BlueData uses a graph-based architecture rather than a single LLM call.

The general workflow is:

```text
User Input
    ↓
Intent Detection
    ↓
Planning / Orchestration
    ↓
Select Required Tool
    ↓
Execute Tool
    ↓
Process Data
    ↓
AI Reasoning
    ↓
Generate Response
```

This architecture makes it easier to add additional marine-data tools and AI capabilities without rewriting the entire application.

---

## 🛠️ Tech Stack

| Component              | Technology             |
| ---------------------- | ---------------------- |
| Language               | Python                 |
| Agent Framework        | LangGraph              |
| API Framework          | FastAPI                |
| AI Models              | Gemini / Groq / Sarvam |
| Environment Management | python-dotenv          |
| Marine Tools           | Custom Python tools    |
| Weather Tools          | Custom Python tools    |
| Safety Tools           | Custom Python tools    |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/MADHUKARTHIKEYAN/bluedata-agents.git
cd bluedata-agents
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

Only add the API keys for the providers you are actually using.

### ⚠️ Important

**Never commit ****`.env`**** to GitHub.**

Make sure your `.gitignore` contains:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 🧪 Test the LangGraph Agent

The easiest way to test the agent locally is:

```text
app/test_graph.py
```

Run it from the **project root**:

```powershell
python -u app/test_graph.py
```

Or, if your package imports require module execution:

```powershell
python -u -m app.test_graph
```

---

## 🔎 What `test_graph.py` Does

The test script invokes the BlueData LangGraph workflow with a user query.

Example:

```python
from app.graph.workflow import app_graph

print("🚀 Starting LangGraph + Live Ocean test...")

result = app_graph.invoke({
    "user_input": "Where is a good fishing zone?",
    "intent": "",
    "response": "",
})

print("✅ Graph executed")

print("\n==============================")
print("FINAL RESULT")
print("==============================")
print(result)
```

You can change:

```python
"user_input": "Where is a good fishing zone?"
```

to test different queries.

For example:

```python
"user_input": "What is the weather today?"
```

or:

```python
"user_input": "Is it safe to go fishing today?"
```

---

# 🌊 Example Test Queries

### Marine

```text
Where is a good fishing zone?
```

### Weather

```text
What is the weather today?
```

### Safety

```text
Is it safe to go fishing today?
```

### General marine query

```text
Give me information about the current ocean conditions.
```

The exact response depends on the tools, APIs, model configuration, and available data.

---

# 🌐 Running the FastAPI Server

To start the backend:

```powershell
python -m app.main
```

If the application starts successfully, the API will normally be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation can be accessed through:

```text
http://localhost:8000/docs
```

---

# 🧩 Project Modules

## `app/graph/`

Contains the LangGraph workflow.

### `state.py`

Defines the state passed between nodes in the agent graph.

### `workflow.py`

Defines the agent workflow and orchestration logic.

---

## `app/services/`

Contains AI provider integrations.

```text
ai.py
ai_router.py
gemini.py
groq.py
sarvam.py
```

The service layer allows the application to separate AI-provider logic from the main agent workflow.

---

## `app/tools/`

Contains tools used by the agent.

### `marine.py`

Marine and ocean-related functionality.

### `weather.py`

Weather-related functionality.

### `safety.py`

Marine safety-related functionality.

---

# 🔄 Adding a New Tool

A new tool can be added under:

```text
app/tools/
```

For example:

```text
app/tools/satellite.py
```

The tool can then be connected to the LangGraph workflow in:

```text
app/graph/workflow.py
```

This modular architecture makes it possible to expand BlueData with additional capabilities such as:

* 🛰️ Satellite data
* 🌡️ Sea surface temperature
* 🌿 Chlorophyll concentration
* 🌊 Ocean currents
* 🌪️ Cyclone information
* 🎣 Fishing-zone intelligence
* 🚢 Maritime route information
* 🛟 Emergency alerts

---

# 🎯 Vision

BlueData aims to bridge the gap between complex marine datasets and people who need actionable ocean intelligence.

Instead of requiring users to understand complicated datasets, APIs, or scientific terminology, the platform allows them to interact with marine information using **natural language**.

```text
Complex Marine Data
        ↓
   AI + Agents
        ↓
Simple Conversation
        ↓
Actionable Intelligence
```

---

# 🚧 Future Improvements

* [ ] Integrate live satellite data
* [ ] Add ISRO Earth Observation datasets
* [ ] Improve fishing-zone prediction
* [ ] Add multilingual support
* [ ] Add voice interaction
* [ ] Add real-time marine alerts
* [ ] Add visualization of ocean conditions
* [ ] Add mobile application
* [ ] Add researcher dashboard
* [ ] Improve agent reflection and planning
* [ ] Add automated evaluation tests

---

# 👥 Team

**BlueData Agent**

An AI and marine-data project developed for exploring intelligent solutions for ocean and maritime applications.

---

## 📜 License

This project is currently intended for educational, research, and hackathon development purposes.
