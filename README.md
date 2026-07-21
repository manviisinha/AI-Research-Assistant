# 🔬 AI Research Assistant

> An intelligent **adaptive RAG (Retrieval-Augmented Generation) research agent** that reads your documents, thinks deeply about your question, and produces a structured, detailed research report — powered by **Groq's blazing-fast LLMs**, **LangGraph**, and a local **ChromaDB** vector database.

---

## 👩‍💻 Team Members

| Name | Role |
|------|------|
| **Manvi Sinha** | Project Lead & Backend Integration |
| **Kavya Jain** | LangGraph Agent Design |
| **Lakshita Aggarwal** | Vector DB & Embeddings |
| **Lavanya Sharma** | Streamlit UI & UX |
| **Divya Yadav** | Prompt Engineering & Testing |

---

## 📌 What Is This Project?

This project is an **AI-powered research assistant** that lets you:

- 📄 Upload your own documents (PDFs, text files, CSVs, Markdown)
- 🧠 Ask any research question about those documents
- 🔍 Optionally search the web for additional context
- 📝 Receive a **well-structured, detailed research report** in seconds

Instead of manually reading through dozens of pages, you just ask — and the AI agent does the heavy lifting.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📂 **Multi-format Document Support** | Upload PDF, TXT, CSV, and Markdown files |
| 🤖 **Groq-Powered LLM** | Uses `llama-3.3-70b-versatile` — ultra-fast, free-tier eligible |
| 🔍 **Smart RAG Retrieval** | Searches your documents using semantic similarity via ChromaDB |
| ⚖️ **Relevance Evaluation** | Automatically checks if retrieved documents actually answer the query |
| 🌐 **Optional Web Search** | Falls back to Tavily web search when documents are insufficient |
| 📊 **Structured Report Output** | Generates reports in Standard, Financial, or custom templates |
| 🔄 **Parallel Query Processing** | Processes multiple research sub-queries simultaneously |
| 💻 **Streamlit Web UI** | Clean, interactive browser interface — no command line needed |

---

## 🏗️ How It Works — Step by Step

When you upload documents and ask a question, the agent follows this pipeline:

```
Your Question
      │
      ▼
┌─────────────────────────┐
│  1. Generate Research   │  The LLM breaks your question into
│     Sub-Queries         │  focused, searchable sub-questions
└──────────┬──────────────┘
           │  (processes up to 5 queries in parallel batches)
           ▼
┌─────────────────────────┐
│  2. Retrieve Documents  │  Searches ChromaDB vector store using
│     from ChromaDB       │  semantic similarity matching
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  3. Evaluate Relevance  │  LLM checks: "Do these documents
│                         │  actually answer this sub-query?"
└──────────┬──────────────┘
           │
     ┌─────┴──────┐
     │            │
  Relevant?    Not Relevant?
     │            │
     │            ▼
     │   ┌─────────────────┐
     │   │  Web Search via │  (only if "Enable Web Search"
     │   │  Tavily API     │   is turned on in the sidebar)
     │   └────────┬────────┘
     │            │
     └────────────┘
           │
           ▼
┌─────────────────────────┐
│  4. Summarize Findings  │  Extracts key insights from each
│                         │  retrieved document or web result
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  5. Write Final Report  │  Combines all summaries into one
│                         │  structured, formatted research report
└─────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | [Groq](https://console.groq.com) — `llama-3.3-70b-versatile` | Query generation, evaluation, summarization, report writing |
| **Agent Framework** | [LangGraph](https://www.langchain.com/langgraph) | Defines the agent workflow and state machine |
| **Vector Database** | [ChromaDB](https://docs.trychroma.com/) | Stores and retrieves document embeddings locally |
| **Embeddings** | [HuggingFace](https://huggingface.co/) — `all-MiniLM-L6-v2` | Converts text to vectors for semantic search |
| **Web Search** | [Tavily](https://tavily.com/) | Optional real-time web search fallback |
| **UI** | [Streamlit](https://docs.streamlit.io/) | Interactive browser-based user interface |

---

## 🗂️ Project Structure

```
AI-Research-Assistant/
│
├── app.py                        # 🖥️  Main Streamlit web application
├── run_researcher.py             # ⌨️  CLI script (run without UI)
├── requirements.txt              # 📦 Python dependencies
├── .env.example                  # 🔑 Template for API keys
│
├── files/                        # 📁 Drop your documents here before uploading
├── database/                     # 🗄️  ChromaDB vector store (auto-created)
│
├── report_structures/            # 📝 Report format templates
│   ├── standard report.md        #    General purpose report format
│   └── financial report.md       #    Finance-specific report format
│
└── src/
    └── assistant/
        ├── graph.py              # 🔗 LangGraph agent — full pipeline definition
        ├── state.py              # 📋 Data models for agent state
        ├── configuration.py      # ⚙️  Configurable parameters (queries, structure)
        ├── prompts.py            # 💬 All LLM prompt templates
        ├── utils.py              # 🛠️  LLM helpers: invoke_groq, invoke_llm, parse_output
        └── vector_db.py          # 🔍 ChromaDB setup and document ingestion
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- A free [Groq API key](https://console.groq.com) (takes 30 seconds to get)
- *(Optional)* A free [Tavily API key](https://tavily.com) for web search

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/manviisinha/AI-Research-Assistant.git
cd AI-Research-Assistant
```

---

### Step 2 — Create and Activate Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
pip install sentence-transformers langchain-groq
```

> ⚠️ `sentence-transformers` downloads the embedding model (~90MB) on first use. This is a one-time download.

---

### Step 4 — Set Up API Keys

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Open `.env` and add:

```ini
# Required — get your free key at https://console.groq.com
GROQ_API_KEY="gsk_your_key_here"

# Optional — only needed if you enable web search in the sidebar
TAVILY_API_KEY="tvly-your_key_here"

# Optional — for LangSmith debugging/monitoring
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your_langsmith_key"
LANGCHAIN_PROJECT="AI Research Assistant"
```

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

Then open your browser at: **http://localhost:8501**

---

## 📖 How to Use the App

### 1️⃣ Upload Your Documents
- In the **left sidebar**, click **"Upload New Documents"**
- Supported formats: `PDF`, `TXT`, `CSV`, `MD`
- You can upload multiple files at once

### 2️⃣ Process the Files
- After uploading, click the **"Process Files"** button
- The app will embed your documents into ChromaDB
- ⏳ *First time takes 1–3 minutes (downloads the embedding model once)*
- ✅ *Subsequent uploads are much faster*

### 3️⃣ Configure Research Settings
In the sidebar, you can adjust:
- **Report Structure** — Choose between Standard, Financial, or any custom template
- **Max Search Queries** — How many sub-queries to generate (1–10, default: 5)
- **Enable Web Search** — Toggle Tavily web search fallback on/off

### 4️⃣ Ask Your Research Question
Type your question in the chat box at the bottom and press Enter.

---

## 💡 Example Prompts

```
Summarize the key findings and main conclusions of this document.
```
```
What methodology was used in this research and what are its limitations?
```
```
Give me a detailed report comparing the different approaches mentioned in this paper.
```
```
What are the key risks and recommendations outlined in this report?
```
```
Explain the technical concepts in this document in simple, easy-to-understand language.
```

---

## ⚙️ Customization

### Switch the LLM Provider

The codebase supports **three LLM backends**. Edit `src/assistant/graph.py` to switch:

| Provider | Function | Notes |
|----------|----------|-------|
| **Groq** *(current default)* | `invoke_groq()` | Free API at [console.groq.com](https://console.groq.com) — very fast |
| **OpenRouter** | `invoke_llm()` | Access GPT-4o, Claude, Gemini via [openrouter.ai](https://openrouter.ai) |
| **Ollama** *(local/offline)* | `invoke_ollama()` | Fully offline — install [Ollama](https://ollama.com) + `ollama pull deepseek-r1:7b` |

### Add Custom Report Structures

1. Create a new `.md` or `.txt` file in the `report_structures/` folder
2. Write your desired report format/structure inside it
3. It will automatically appear in the **Report Structure** dropdown in the UI

### Adjust Default Parameters

Edit `src/assistant/configuration.py`:
- `max_search_queries` — Default number of sub-queries (currently `5`)
- `enable_web_search` — Default web search state (currently `False`)

---

## 📚 Resources & References

- [LangChain: Building a deep researcher with DeepSeek-R1](https://www.youtube.com/watch?v=sGUjmyfof4Q)
- [LangChain: Local research assistant from scratch with Ollama](https://www.youtube.com/watch?v=XGuTzHoqlj8)
- [LangGraph Template: Multi-Agent RAG Research](https://www.youtube.com/watch?v=JLDLANs_m_w)
- [LangGraph Adaptive RAG implementation](https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_adaptive_rag_local.ipynb)
- [Groq API Documentation](https://console.groq.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an [issue](https://github.com/manviisinha/AI-Research-Assistant/issues) for bugs or feature requests
- Submit a pull request with improvements

---

## 📬 Contact

Have questions or suggestions? Open an issue on the [GitHub repository](https://github.com/manviisinha/AI-Research-Assistant/issues).