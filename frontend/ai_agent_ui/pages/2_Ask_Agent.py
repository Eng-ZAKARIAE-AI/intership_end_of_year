import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Ask Agent",
    page_icon="💬",
    layout="wide",
)

# ---------------------------------------------------------------------------
# STYLING (kept consistent with the Workstation Records page)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header banner */
    .page-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .page-header h1 {
        color: #ffffff;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .page-header p {
        color: #9ca3af;
        margin: 6px 0 0 0;
        font-size: 0.95rem;
    }

    /* Nav buttons */
    div[data-testid="column"] .stButton button {
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        color: #374151;
        font-weight: 600;
        padding: 0.6rem 0.5rem;
        transition: all 0.15s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    div[data-testid="column"] .stButton button:hover {
        border-color: #6366f1;
        color: #6366f1;
        background-color: #eef2ff;
        transform: translateY(-1px);
    }

    /* Status pill under header */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 18px;
    }
    .status-pill .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10b981;
        display: inline-block;
    }

    /* Chat message bubbles */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 4px 6px;
        margin-bottom: 4px;
    }

    /* Chat input box */
    div[data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 50px 20px;
        color: #9ca3af;
    }
    .empty-state .icon {
        font-size: 2.4rem;
        margin-bottom: 10px;
    }
    .empty-state .title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #4b5563;
        margin-bottom: 4px;
    }
    .empty-state .subtitle {
        font-size: 0.9rem;
    }

    .stButton button[kind="secondary"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="page-header">
    <h1>💬 Ask the Tech IT Agent</h1>
    <p>Ask questions about workstation health, telemetry, and diagnostics in plain language</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠  Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📄  List Records", use_container_width=True):
        st.switch_page("pages/1_List_Records.py")
with col3:
    if st.button("🤖  AI Agent", use_container_width=True):
        st.toast("AI Agent is ready to assist you!", icon="🤖")
with col4:
    if st.button("📝  System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

st.write("")
st.divider()

# ---------------------------------------------------------------------------
# STATUS + CLEAR CHAT
# ---------------------------------------------------------------------------
status_col, clear_col = st.columns([5, 1])
with status_col:
    st.markdown("""
    <div class="status-pill"><span class="dot"></span> Agent online</div>
    """, unsafe_allow_html=True)
with clear_col:
    if st.button("🗑️  Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# CHAT INTERFACE
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🤖</div>
        <div class="title">No messages yet</div>
        <div class="subtitle">Ask something like "Which workstations are low on RAM?"</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if "time" in message:
                st.caption(message["time"])

if prompt := st.chat_input("What is your question about the workstations?"):
    now = datetime.now().strftime("%H:%M")

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
        st.caption(now)
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = f"I am a simulated IT Agent. You asked: {prompt}"
        st.markdown(response)
        st.caption(datetime.now().strftime("%H:%M"))
    st.session_state.messages.append({"role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M")})