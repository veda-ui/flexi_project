# Autonomous Multi-Agent Research Summarizer

## Project Overview
This project is a multi-agent AI application designed to take a broad user topic (e.g., "Latest advancements in solid-state batteries") and autonomously research, extract, standardize, and summarize the information into a cohesive briefing document. The system relies on four specialized agents working in a pipeline. 

A critical requirement of this project is **UI Transparency**: the user interface must display the real-time communication, thought processes, and hand-offs between the agents.

## Architecture & Agent Specifications

The system utilizes a sequential multi-agent workflow. The application should use an OpenAI-compatible API (specifically targeting a local/cloud instance of `gpt-oss-20b` via Ollama).

### Agent 1: The Query Formulator
*   **Role:** Analyzes the user's broad topic and generates precise, targeted search queries.
*   **Input:** User's initial prompt/topic.
*   **Output:** A list of optimal search queries (e.g., JSON array of strings).
*   **Behavior:** Loops through a planning sequence to ensure queries cover different facets of the main topic before passing them to the next agent.

### Agent 2: The Researcher & Extractor
*   **Role:** Executes the searches and scrapes raw data from the web.
*   **Input:** Search queries from Agent 1.
*   **Tools Required:** Web Search API (e.g., Tavily, DuckDuckGo) and Webpage Scraper (e.g., BeautifulSoup, Trafilatura).
*   **Output:** Raw extracted text and relevant metadata (URLs, titles) from the top search results.
*   **Behavior:** Filters out irrelevant pages and extracts the core textual content from the useful ones.

### Agent 3: The Standardizer
*   **Role:** Cleans and structures the raw data.
*   **Input:** Raw extracted text from Agent 2.
*   **Output:** A structured, standardized JSON or Markdown format mapping facts to their sources.
*   **Behavior:** Removes duplicate information, formats citations, corrects broken text encoding, and organizes the findings into logical categories.

### Agent 4: The Summarizer
*   **Role:** Drafts the final briefing document.
*   **Input:** Standardized data from Agent 3.
*   **Output:** A cohesive, easy-to-read Markdown report.
*   **Behavior:** Synthesizes the information, highlights key takeaways, ensures a professional tone, and presents the final response to the user.

## User Interface (UI) Requirements

*   **Real-time Agent Communication:** The UI must feature a live feed or terminal-like window that displays what each agent is doing. 
    *   *Example:* 
        *   `[Agent 1] Generating queries: ["solid state battery timeline 2024", "solid state battery energy density breakthroughs"]`
        *   `[Agent 2] Searching web for "solid state battery timeline 2024"... Extracted 3000 words from 3 sources.`
        *   `[Agent 3] Cleaning data... Removed duplicates. Grouping into "Timeline" and "Technical Specs".`
        *   `[Agent 4] Drafting final summary...`
*   **Final Output Window:** A dedicated space to render the final Markdown report beautifully once Agent 4 is finished.

## Technical Stack Recommendations (For CLI Tool)
*   **Backend / Orchestration:** Python with CrewAI, LangChain, or AutoGen (to manage the multi-agent state).
*   **LLM Integration:** Standard OpenAI Python SDK configured to point to an Ollama instance endpoint (`base_url`).
*   **Frontend:** Streamlit or Gradio for rapid UI development with built-in streaming/status-updating capabilities, or Next.js/React for a custom web app.
*   **APIs:** Tavily API or DuckDuckGo Search tool.

## Execution Flow (Developer Instructions)
1. Initialize the UI and accept the user prompt.
2. Instantiate the 4 agents with their specific system prompts defining their roles.
3. Pass the user prompt to Agent 1. Stream its output to the UI.
4. Pass Agent 1's output to Agent 2. Execute tools. Stream progress to the UI.
5. Pass Agent 2's output to Agent 3. Stream data structuring progress to the UI.
6. Pass Agent 3's output to Agent 4. Stream the final generated markdown to the UI.