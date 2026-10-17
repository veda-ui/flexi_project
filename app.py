"""
Streamlit UI — Autonomous Multi-Agent Research Summarizer
Entry point: streamlit run app.py

Architecture: Pipeline runs in a background thread, writing status messages
into a thread-safe queue stored in session_state. The UI polls via
st.rerun() only while running=True.
"""

import queue
import threading
import time

import streamlit as st

from pipeline import run_pipeline

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Summarizer",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Autonomous Multi-Agent Research Summarizer")
st.caption("Powered by LangChain · gpt-oss:20b via Ollama · DuckDuckGo Search")

# ── Session State Init ────────────────────────────────────────────────────────
defaults = {
    "log_lines": [],
    "report": None,
    "running": False,
    "error": None,
    "msg_queue": None,
    "thread": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Layout ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("🤖 Live Agent Feed")
    feed_box = st.empty()

with col_right:
    st.subheader("📄 Final Briefing Report")
    report_box = st.empty()

# ── Render Helpers ────────────────────────────────────────────────────────────
def render_feed():
    if st.session_state.log_lines:
        feed_box.code("\n".join(st.session_state.log_lines), language=None)
    else:
        feed_box.info("Agent activity will appear here once you start research.")

def render_report():
    if st.session_state.error:
        report_box.error(f"Pipeline error:\n\n{st.session_state.error}")
    elif st.session_state.report:
        report_box.markdown(st.session_state.report)
    else:
        report_box.info("The final briefing report will appear here after the pipeline completes.")

render_feed()
render_report()

# ── Input Controls ────────────────────────────────────────────────────────────
st.divider()
topic = st.text_input(
    "Enter your research topic:",
    placeholder='e.g. "Latest advancements in solid-state batteries"',
    disabled=st.session_state.running,
    key="topic_input",
)
run_button = st.button(
    "🚀 Start Research",
    disabled=st.session_state.running or not (topic or "").strip(),
    type="primary",
)

# ── Start Pipeline ────────────────────────────────────────────────────────────
if run_button and topic.strip() and not st.session_state.running:
    # Reset all state
    st.session_state.log_lines = []
    st.session_state.report = None
    st.session_state.error = None
    st.session_state.running = True
    st.session_state.msg_queue = queue.Queue()

    def _run(t, q):
        def cb(msg):
            q.put(("log", msg))
        try:
            result = run_pipeline(t, status_callback=cb)
            q.put(("done", result["report"]))
        except Exception as exc:
            q.put(("error", str(exc)))

    st.session_state.thread = threading.Thread(
        target=_run,
        args=(topic.strip(), st.session_state.msg_queue),
        daemon=True,
    )
    st.session_state.thread.start()
    st.rerun()

# ── Polling Loop (only when pipeline is active) ───────────────────────────────
if st.session_state.running and st.session_state.msg_queue is not None:
    q = st.session_state.msg_queue

    # Drain all messages currently in the queue
    updated = False
    while True:
        try:
            kind, payload = q.get_nowait()
            if kind == "log":
                st.session_state.log_lines.append(payload)
                updated = True
            elif kind == "done":
                st.session_state.report = payload
                st.session_state.running = False
                updated = True
                break
            elif kind == "error":
                st.session_state.error = payload
                st.session_state.running = False
                updated = True
                break
        except queue.Empty:
            break

    # Re-render with fresh data
    render_feed()
    render_report()

    if st.session_state.running:
        # Still going — wait briefly then trigger another render cycle
        time.sleep(0.5)
        st.rerun()
    else:
        # Pipeline finished
        if st.session_state.report:
            st.success("Research complete! Your briefing is ready.")
            st.download_button(
                label="Download Report (.md)",
                data=st.session_state.report,
                file_name=f"briefing_{topic[:40].replace(' ', '_')}.md",
                mime="text/markdown",
            )
        st.rerun()  # final rerun to unlock input controls
