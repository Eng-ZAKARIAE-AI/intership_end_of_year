import streamlit as st
import os
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Workstation Dashboard",
    page_icon="🖥️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# STYLING (kept consistent with the other pages)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero banner */
    .page-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 16px;
        padding: 36px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    .page-header::after {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, rgba(99,102,241,0) 70%);
        border-radius: 50%;
    }
    .page-header h1 {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .page-header p {
        color: #9ca3af;
        margin: 8px 0 0 0;
        font-size: 1rem;
        max-width: 560px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: rgba(16,185,129,0.12);
        color: #34d399;
        border: 1px solid rgba(52,211,153,0.35);
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 16px;
    }
    .status-pill .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #34d399;
        display: inline-block;
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
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
        margin: 28px 0 16px 0;
    }

    /* Metric cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-card .label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #111827;
    }

    /* Feature cards */
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 22px 22px 18px 22px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.15s ease;
        }
    .feature-card:hover {
        border-color: #c7d2fe;
        box-shadow: 0 6px 18px rgba(99,102,241,0.12);
        transform: translateY(-2px);
    }
    .feature-card .icon-badge {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 12px;
    }
    .feature-card .icon-badge.blue { background-color: #eef2ff; }
    .feature-card .icon-badge.green { background-color: #ecfdf5; }
    .feature-card .icon-badge.amber { background-color: #fffbeb; }
    .feature-card h3 {
        font-size: 1.05rem;
        font-weight: 700;
        color: #111827;
        margin: 0 0 6px 0;
    }
    .feature-card p {
        font-size: 0.88rem;
        color: #6b7280;
        margin: 0 0 14px 0;
        line-height: 1.4;
        min-height: 54px;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown("""
<div class="page-header">
    <h1>🖥️ Workstation Dashboard</h1>
    <p>Monitor telemetry, review system logs, and chat with the IT agent across every managed workstation from one place.</p>
    <div class="status-pill"><span class="dot"></span> System operational</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠  Home", use_container_width=True):
        st.rerun()
with col2:
    if st.button("📄  List Records", use_container_width=True):
        st.switch_page("pages/1_List_Records.py")
with col3:
    if st.button("💬  Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")
with col4:
    if st.button("📝  System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

if st.session_state.get("show_ai", False):
    st.toast("AI Agent is ready to assist you!", icon="🤖")
    st.session_state.show_ai = False

st.write("")
st.divider()

# ---------------------------------------------------------------------------
# QUICK STATS
# ---------------------------------------------------------------------------
DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "backend", "system_event_loader", "telemetry_edge.db"
))


def get_quick_stats():
    stats = {"records": 0, "hosts": 0, "synced": 0, "last_update": "N/A"}
    if not os.path.exists(DB_PATH):
        return stats
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM telemetry_buffer")
        stats["records"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM telemetry_buffer WHERE synced = 1")
        stats["synced"] = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(timestamp) FROM telemetry_buffer")
        last = cursor.fetchone()[0]
        stats["last_update"] = last if last else "N/A"
        conn.close()
    except Exception:
        pass
    return stats


stats = get_quick_stats()

st.markdown('<div class="section-title">📊 Quick Overview</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Total Records</div>
        <div class="value">{stats['records']}</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Synced Records</div>
        <div class="value">{stats['synced']}</div>
    </div>""", unsafe_allow_html=True)
with m3:
    pct = f"{(stats['synced'] / stats['records'] * 100):.0f}%" if stats["records"] else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Sync Rate</div>
        <div class="value">{pct}</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Last Update</div>
        <div class="value" style="font-size:1.05rem;">{stats['last_update']}</div>
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FEATURE CARDS
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">🚀 What would you like to do?</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-badge blue">📄</div>
        <h3>List Records</h3>
        <p>Browse the latest workstation telemetry snapshots including CPU, RAM, GPU, and peripheral data.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Records →", use_container_width=True, key="open_records"):
        st.switch_page("pages/1_List_Records.py")

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-badge green">💬</div>
        <h3>Ask Agent</h3>
        <p>Chat with the IT agent to ask natural-language questions about workstation health and status.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Chat →", use_container_width=True, key="open_chat"):
        st.switch_page("pages/2_Ask_Agent.py")

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-badge amber">📝</div>
        <h3>System Logs</h3>
        <p>Review recent system events collected across all monitored workstations, with search and filters.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Logs →", use_container_width=True, key="open_logs"):
        st.switch_page("pages/3_Logs.py")

st.write("")
st.caption(f"Dashboard loaded at {datetime.now().strftime('%H:%M:%S')}")
