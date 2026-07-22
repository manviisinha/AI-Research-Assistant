import pyperclip
import streamlit as st
from src.assistant.graph import researcher
from src.assistant.utils import get_report_structures, process_uploaded_files
from dotenv import load_dotenv

load_dotenv()

# ─── Custom CSS for a polished, modern look ────────────────────────────────
CUSTOM_CSS = """
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Main header gradient ── */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}
.main-header h1 {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.main-header p {
    color: rgba(255,255,255,0.85) !important;
    font-size: 0.95rem !important;
    margin: 0.3rem 0 0 0 !important;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e0e0ff !important;
}
section[data-testid="stSidebar"] label {
    color: #b0b0d0 !important;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #9090b0 !important;
}

/* ── Progress bar styling ── */
.progress-container {
    background: #1e1e2e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    border: 1px solid #2d2d44;
}
.progress-step {
    display: flex;
    align-items: center;
    padding: 0.4rem 0;
    font-size: 0.9rem;
}
.progress-step .icon { margin-right: 0.6rem; font-size: 1.1rem; }
.progress-step.active { color: #667eea; font-weight: 600; }
.progress-step.done { color: #4ade80; }
.progress-step.waiting { color: #6b7280; }

/* ── Chat bubbles ── */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* ── Status widget ── */
[data-testid="stStatusWidget"] {
    border-radius: 10px !important;
}

/* ── Info cards ── */
.info-card {
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #b0b0d0;
}

/* ── Divider ── */
.sidebar-divider {
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1rem 0;
}
</style>
"""


def generate_response(user_input, enable_web_search, report_structure, max_search_queries):
    """
    Generate response using the researcher agent and stream steps
    with a progress bar tracking each phase.
    """
    initial_state = {
        "user_instructions": user_input,
    }

    config = {"configurable": {
        "enable_web_search": enable_web_search,
        "report_structure": report_structure,
        "max_search_queries": max_search_queries,
    }}

    # ── Define the research phases ──
    phases = [
        {"key": "generate_research_queries", "label": "Generating research queries", "icon": "🔍"},
        {"key": "search_queries", "label": "Searching & analyzing sources", "icon": "📚"},
        {"key": "generate_final_answer", "label": "Writing final report", "icon": "📝"},
    ]
    total_phases = len(phases)
    current_phase = 0

    # ── Progress bar ──
    progress_bar = st.progress(0, text="⏳ Initializing research pipeline...")

    # ── Status container with step details ──
    langgraph_status = st.status("🚀 **Research in Progress**", state="running", expanded=True)

    with langgraph_status:
        # Pre-create expanders
        generate_queries_expander = st.expander("🔍 Research Queries", expanded=False)
        search_queries_expander = st.expander("📚 Source Analysis", expanded=True)
        final_answer_expander = st.expander("📝 Final Report Generation", expanded=False)

        # Step status display
        step_placeholder = st.empty()

        steps = []
        search_count = 0

        def update_step_display(active_idx):
            """Render the step progress indicator."""
            lines = []
            for i, phase in enumerate(phases):
                if i < active_idx:
                    lines.append(f"✅ ~~{phase['label']}~~  ")
                elif i == active_idx:
                    lines.append(f"⏳ **{phase['label']}...**  ")
                else:
                    lines.append(f"⬜ {phase['label']}  ")
            step_placeholder.markdown("\n".join(lines))

        update_step_display(0)

        # ── Stream the researcher graph ──
        for output in researcher.stream(initial_state, config=config):
            for key, value in output.items():
                expander_label = key.replace("_", " ").title()

                if key == "generate_research_queries":
                    current_phase = 1
                    progress_bar.progress(
                        int((current_phase / total_phases) * 100),
                        text="🔍 Research queries generated"
                    )
                    update_step_display(current_phase)
                    with generate_queries_expander:
                        if "research_queries" in value:
                            for i, q in enumerate(value["research_queries"], 1):
                                st.markdown(f"**{i}.** {q}")
                        else:
                            st.write(value)

                elif key.startswith("search_and_summarize_query"):
                    search_count += 1
                    search_progress = min(
                        int((1 + search_count / max(max_search_queries, 1)) / total_phases * 100),
                        66
                    )
                    progress_bar.progress(
                        search_progress,
                        text=f"📚 Analyzed {search_count} source(s)..."
                    )
                    update_step_display(1)
                    with search_queries_expander:
                        with st.expander(f"📄 {expander_label}", expanded=False):
                            st.write(value)

                elif key == "search_queries":
                    # Intermediate batch node — just update display
                    update_step_display(1)

                elif key == "generate_final_answer":
                    current_phase = 2
                    progress_bar.progress(90, text="📝 Generating final report...")
                    update_step_display(current_phase)
                    with final_answer_expander:
                        st.write(value)

                steps.append({"step": key, "content": value})

    # ── Complete ──
    progress_bar.progress(100, text="✅ Research complete!")
    update_step_display(total_phases)
    langgraph_status.update(
        state="complete",
        label="✅ **Research Complete** — powered by Groq (Llama 3.3 70B)",
        expanded=False
    )

    return steps[-1]["content"] if steps else "No response generated"


def clear_chat():
    st.session_state.messages = []
    st.session_state.processing_complete = False
    st.session_state.uploader_key = 0


def main():
    st.set_page_config(
        page_title="Groq RAG Researcher",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── Session state init ──
    defaults = {
        "processing_complete": False,
        "uploader_key": 0,
        "messages": [],
        "selected_report_structure": None,
        "max_search_queries": 5,
        "files_ready": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # ── Header ──
    st.markdown("""
    <div class="main-header">
        <h1>🔬 RAG Researcher</h1>
        <p>Powered by Groq (Llama 3.3 70B) · LangGraph · ChromaDB</p>
    </div>
    """, unsafe_allow_html=True)

    # Clear chat button (top right)
    col_spacer, col_clear = st.columns([8, 1])
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, help="Clear chat history"):
            clear_chat()
            st.rerun()

    # ═══════════════════════ SIDEBAR ═══════════════════════
    with st.sidebar:
        st.markdown("## ⚙️ Research Settings")
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Report structure
        report_structures = get_report_structures()
        default_report = "standard report"
        selected_structure = st.selectbox(
            "📋 Report Structure",
            options=list(report_structures.keys()),
            index=list(map(str.lower, report_structures.keys())).index(default_report)
        )
        st.session_state.selected_report_structure = report_structures[selected_structure]

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Search config
        st.markdown("### 🔎 Search Configuration")
        st.session_state.max_search_queries = st.slider(
            "Max Search Queries",
            min_value=1,
            max_value=10,
            value=st.session_state.max_search_queries,
            help="Number of research sub-queries to generate (1–10)"
        )
        enable_web_search = st.toggle("🌐 Enable Web Search", value=False)
        if enable_web_search:
            st.markdown(
                '<div class="info-card">🌐 Web search enabled — queries will use Tavily API when RAG docs are insufficient.</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # File upload
        st.markdown("### 📁 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload documents to the knowledge base",
            type=["pdf", "txt", "csv", "md"],
            accept_multiple_files=True,
            key=f"uploader_{st.session_state.uploader_key}"
        )

        if uploaded_files:
            st.session_state.files_ready = True
            st.session_state.processing_complete = False

        if st.session_state.files_ready and not st.session_state.processing_complete:
            if st.button("⚡ Process Files", use_container_width=True, type="primary"):
                with st.status("Processing files...", expanded=True) as status:
                    progress = st.progress(0)
                    for i, f in enumerate(uploaded_files):
                        progress.progress(
                            int((i + 1) / len(uploaded_files) * 100),
                            text=f"Processing {f.name}..."
                        )
                    if process_uploaded_files(uploaded_files):
                        st.session_state.processing_complete = True
                        st.session_state.files_ready = False
                        st.session_state.uploader_key += 1
                    progress.progress(100, text="✅ All files processed!")
                    status.update(label="✅ Files processed!", state="complete")

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Model info card
        st.markdown("""
        <div class="info-card">
            <strong>🤖 Model:</strong> Llama 3.3 70B via Groq<br>
            <strong>🗄️ Vector DB:</strong> ChromaDB<br>
            <strong>🔗 Framework:</strong> LangGraph
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════ CHAT AREA ═══════════════════════

    # Display chat history
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                col_copy, col_spacer = st.columns([1, 8])
                with col_copy:
                    if st.button("📋 Copy", key=f"copy_hist_{idx}"):
                        pyperclip.copy(message["content"])
                        st.toast("✅ Copied to clipboard!", icon="📋")

    # ── Chat input ──
    if user_input := st.chat_input("💬 Ask a research question..."):
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        # Generate response
        report_structure = st.session_state.selected_report_structure["content"]
        with st.chat_message("assistant", avatar="🤖"):
            assistant_response = generate_response(
                user_input,
                enable_web_search,
                report_structure,
                st.session_state.max_search_queries
            )

            # Display final answer
            final_answer = assistant_response.get("final_answer", str(assistant_response))
            st.markdown("---")
            st.markdown("### 📄 Research Report")
            st.markdown(final_answer)

            # Copy button
            col_copy, col_spacer = st.columns([1, 8])
            with col_copy:
                if st.button("📋 Copy Report", key=f"copy_{len(st.session_state.messages)}"):
                    pyperclip.copy(final_answer)
                    st.toast("✅ Copied to clipboard!", icon="📋")

        # Store in history
        st.session_state.messages.append({"role": "assistant", "content": final_answer})


if __name__ == "__main__":
    main()