# 🔬 RAG Researcher — Powered by Groq + LangGraph

> An **adaptive RAG research agent** that reads your documents, reasons over them, and generates structured research reports — powered by **Groq's ultra-fast LLMs** and **LangGraph**.

<div align="center">
  <img src="https://github.com/user-attachments/assets/5dc34341-3a2f-461c-b66d-46b134fe5bd9" alt="Demo of RAG Researcher with LangGraph & Groq">
</div>

---

## ✨ What It Does

Upload any PDF, TXT, CSV, or Markdown file, ask a research question, and the agent will:

1. **Generate Research Queries** — Breaks your question into focused sub-queries
2. **Retrieve Relevant Documents** — Searches your uploaded files via a local **ChromaDB** vector store
3. **Evaluate Relevance** — Scores each retrieved document against the query
4. **Web Search Fallback** — Optionally searches the web via **Tavily** if documents aren't sufficient
5. **Summarize Findings** — Extracts key insights from all gathered information
6. **Write Final Report** — Produces a well-structured, detailed research report

---

## 🏗️ System Architecture

```
User Question
     │
     ▼
┌─────────────────────┐
│  Generate Research  │  ← Groq LLM (llama-3.3-70b)
│      Queries        │
└────────┬────────────┘
         │ (parallel per query)
         ▼
┌─────────────────────┐     ┌──────────────────┐
│  Retrieve from RAG  │────▶│ Evaluate Relevance│  ← Groq LLM
│  (ChromaDB)         │     └────────┬─────────┘
└─────────────────────┘              │
                              Relevant? ──No──▶ Web Search (Tavily)
                                  │
                                  ▼ Yes
                         ┌────────────────┐
                         │  Summarize     │  ← Groq LLM
                         │  Findings      │
                         └───────┬────────┘
                                 ▼
                         ┌────────────────┐
                         │  Write Final   │  ← Groq LLM
                         │  Report        │
                         └────────────────┘
```

<div align="center">
  <img src="https://github.com/user-attachments/assets/5e06e948-c853-47d1-b25e-e3c5ca96b60d" alt="LangGraph RAG Researcher Flowchart">
</div>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | [Groq](https://console.groq.com) — `llama-3.3-70b-versatile` (free tier) |
| **Agent Framework** | [LangGraph](https://www.langchain.com/langgraph) |
| **Vector Database** | [ChromaDB](https://docs.trychroma.com/) |
| **Embeddings** | [HuggingFace](https://huggingface.co/) — `all-MiniLM-L6-v2` (local, free) |
| **Web Search** | [Tavily](https://tavily.com/) (optional) |
| **UI** | [Streamlit](https://docs.streamlit.io/) |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/kaymen99/local-rag-researcher-deepseek
cd local-rag-researcher-deepseek
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install sentence-transformers langchain-groq
```

### 4. Configure API Keys

Copy the example env file and fill in your keys:
```bash
cp .env.example .env
```

Edit `.env`:
```ini
# Required — get free key at https://console.groq.com
GROQ_API_KEY="gsk_your_key_here"

# Optional — only needed if enabling web search
TAVILY_API_KEY="tvly-your_key_here"

# Optional — for LangSmith monitoring
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your_langsmith_key"
LANGCHAIN_PROJECT="RAG Researcher"
```

### 5. Launch the App
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📖 How to Use

1. **Upload Documents** — Use the sidebar to upload PDF, TXT, CSV, or Markdown files
2. **Click "Process Files"** — The app embeds your documents into ChromaDB
   > ⚠️ *First run downloads the embedding model (~90MB). This takes 1–3 minutes but only happens once.*
3. **Select a Report Structure** — Choose from the dropdown (Standard, Academic, etc.)
4. **Set Search Queries Limit** — Control how many sub-queries the agent generates (1–10)
5. **Enable Web Search** *(optional)* — Tick the checkbox to allow Tavily web fallback
6. **Ask Your Research Question** — Type in the chat box and hit Enter

### 💡 Example Prompts
```
Summarize the key findings and conclusions of this document.

What are the main arguments made and what evidence supports them?

Give me a detailed report on the methodology used in this research.

What are the limitations and future work mentioned in this paper?
```

---

## 🗂️ Project Structure

```
local-rag-researcher-deepseek/
├── app.py                      # Streamlit UI
├── run_researcher.py           # CLI script to run without UI
├── requirements.txt
├── .env                        # Your API keys (not committed)
├── .env.example                # Template for .env
├── files/                      # Drop your documents here
├── database/                   # ChromaDB vector store (auto-created)
├── report_structures/          # Custom report format templates
└── src/
    └── assistant/
        ├── graph.py            # LangGraph agent definition
        ├── state.py            # Agent state schemas
        ├── configuration.py    # Configurable parameters
        ├── prompts.py          # LLM prompts
        ├── utils.py            # LLM helpers (Groq, OpenRouter, Ollama)
        └── vector_db.py        # ChromaDB setup & document ingestion
```

---

## ⚙️ Customization

### Switch LLM Provider

The codebase supports **three LLM backends** — just edit `src/assistant/graph.py`:

| Provider | Function | Setup |
|----------|----------|-------|
| **Groq** *(default)* | `invoke_groq()` | Free API key at [console.groq.com](https://console.groq.com) |
| **OpenRouter** | `invoke_llm()` | API key at [openrouter.ai](https://openrouter.ai) — access GPT-4o, Claude, Gemini |
| **Ollama** *(local)* | `invoke_ollama()` | Install [Ollama](https://ollama.com) + `ollama pull deepseek-r1:7b` |

### Add Custom Report Structures

Drop a `.md` or `.txt` file in the `report_structures/` folder. It will automatically appear in the UI's report structure dropdown.

### Adjust Processing Parameters

In the sidebar or `configuration.py`:
- `max_search_queries` — Number of research sub-queries (default: 5)
- `enable_web_search` — Toggle Tavily web fallback
- `report_structure` — Report format/template

---

## 🔧 Optional: Visualize Agent in LangGraph Studio

```bash
pip install -U "langgraph-cli[inmem]"
langgraph dev
```

---

## 📚 Resources

- [LangChain: Building a local deep researcher with DeepSeek-R1](https://www.youtube.com/watch?v=sGUjmyfof4Q)
- [LangChain: Local research assistant with Ollama](https://www.youtube.com/watch?v=XGuTzHoqlj8)
- [LangGraph Template: Multi-Agent RAG Research](https://www.youtube.com/watch?v=JLDLANs_m_w)
- [LangGraph Adaptive RAG implementation](https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_adaptive_rag_local.ipynb)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📬 Contact

Have questions or suggestions? Open an issue on the [GitHub repository](https://github.com/manviisinha/AI-Research-Assistant/issues).