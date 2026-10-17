# 🔬 Autonomous Multi-Agent Research Summarizer

A multi-agent AI application that takes a broad research topic and autonomously researches, extracts, standardizes, and summarizes information into a cohesive briefing document — with a real-time UI showing each agent's activity as it happens.

---

## 🖥️ Demo

> Enter any research topic → watch 4 agents collaborate in real time → get a polished Markdown briefing

**Live Agent Feed (left panel):**
```
─── Agent 1: Query Formulator ───
[Agent 1] Analyzing topic: "Latest advancements in solid-state batteries"...
[Agent 1] Generated 5 queries: ["solid state battery breakthroughs 2025", ...]

─── Agent 2: Researcher & Extractor ───
[Agent 2] Searching web for: "solid state battery breakthroughs 2025"...
[Agent 2] ✓ Extracted 3821 chars from https://example.com/article

─── Agent 3: Standardizer ───
[Agent 3] Standardizing 6 sources...
[Agent 3] Cleaning data... removing duplicates and organizing categories...

─── Agent 4: Summarizer ───
[Agent 4] Drafting final summary...
[Agent 4] ✓ Final briefing document ready!
```

---

## 🏗️ Architecture

```
User Prompt
    │
    ▼
┌─────────────────────┐
│  Agent 1            │  Analyzes topic → outputs JSON array of search queries
│  Query Formulator   │
└────────┬────────────┘
         │ queries[]
         ▼
┌─────────────────────┐
│  Agent 2            │  DuckDuckGo search + Trafilatura scrape (tool-calling loop)
│  Researcher &       │
│  Extractor          │
└────────┬────────────┘
         │ raw [{url, title, content}]
         ▼
┌─────────────────────┐
│  Agent 3            │  Deduplicates, categorizes, formats citations
│  Standardizer       │
└────────┬────────────┘
         │ structured Markdown
         ▼
┌─────────────────────┐
│  Agent 4            │  Writes final professional briefing document
│  Summarizer         │
└────────┬────────────┘
         │
         ▼
    Final Markdown Report
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Agent Orchestration** | [LangChain](https://github.com/langchain-ai/langchain) |
| **LLM** | `gpt-oss:20b` via [Ollama](https://ollama.com) (OpenAI-compatible API) |
| **Web Search** | DuckDuckGo (free, no API key needed) |
| **Web Scraping** | [Trafilatura](https://trafilatura.readthedocs.io/) |
| **UI** | [Streamlit](https://streamlit.io/) |
| **Config** | `python-dotenv` |

---

## 📁 Project Structure

```
flexi_project/
├── app.py                      # Streamlit UI entry point
├── pipeline.py                 # Orchestrates all 4 agents sequentially
├── requirements.txt
├── .env.example                # Environment variable template
├── agents/
│   ├── query_formulator.py     # Agent 1: generates targeted search queries
│   ├── researcher.py           # Agent 2: search + scrape tool-calling loop
│   ├── standardizer.py         # Agent 3: cleans & structures raw data
│   └── summarizer.py           # Agent 4: writes final briefing document
├── tools/
│   ├── search_tool.py          # DuckDuckGo search LangChain tool
│   └── scraper_tool.py         # Trafilatura scraper LangChain tool
└── utils/
    └── llm_config.py           # Shared LLM config (Ollama endpoint)
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/veda-ui/flexi_project.git
cd flexi_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your Ollama credentials:

```env
OLLAMA_BASE_URL="https://ollama.com/v1"
OLLAMA_API_KEY="your_ollama_api_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ⚙️ How It Works

### Agent 1 — Query Formulator
Receives the user's broad topic and uses the LLM to decompose it into **4–5 precise, faceted search queries** (returned as a JSON array). No external tools — pure LLM reasoning.

### Agent 2 — Researcher & Extractor
Implements a **LangChain agentic tool-calling loop**: the LLM iteratively calls `web_search` (DuckDuckGo) and `scrape_page` (Trafilatura) until it has collected sufficient content. Returns a list of `{url, title, content}` dicts.

### Agent 3 — Standardizer
Takes all raw scraped content and instructs the LLM to **deduplicate, categorize into logical sections, and attach source citations** — producing clean structured Markdown.

### Agent 4 — Summarizer
Writes the **final professional briefing document** from the structured data: executive summary, organized sections, key takeaways, and a conclusion.

### UI — Real-Time Agent Feed
Streamlit UI runs the pipeline in a **background thread**, writing status updates into a `queue.Queue` stored in `st.session_state`. The UI polls every 0.5s via `st.rerun()` to display live updates without blocking.

---

## 📋 Requirements

- Python 3.10+
- An [Ollama](https://ollama.com) account with API access
- Internet connection (for DuckDuckGo search)

---

## 📄 License

MIT