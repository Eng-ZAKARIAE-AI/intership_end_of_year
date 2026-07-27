import streamlit as st
import pandas as pd
import os
import sqlite3
import json
from datetime import datetime

st.set_page_config(
    page_title="System Logs",
    page_icon="📝",
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
    div[data-testid="column"] .stButton button:disabled {
        background-color: #eef2ff;
        color: #6366f1;
        border-color: #6366f1;
        opacity: 1;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
        margin: 8px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
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

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="page-header">
    <h1>📝 System Logs</h1>
    <p>Recent system events collected across all monitored workstations</p>
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
    if st.button("💬  Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")
with col4:
    st.button("📝  System Logs", use_container_width=True, disabled=True)

st.write("")
st.divider()

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "backend", "system_event_loader", "telemetry_edge.db"
))


@st.cache_data(ttl=30)
def load_logs(limit: int = 50) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, payload FROM telemetry_buffer ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    all_logs = []
    for record_ts, payload_str in rows:
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            continue

        metrics = payload.get("metrics", {})
        hostname = metrics.get("hostname", "Unknown")
        logs = payload.get("logs", [])

        if isinstance(logs, list):
            for log in logs:
                if isinstance(log, dict) and "error" not in log:
                    all_logs.append({
                        "Record Time": record_ts,
                        "Hostname": hostname,
                        "Time Generated": log.get("timestamp") or log.get("time_generated") or "Unknown",
                        "Source": log.get("source_name") or "Unknown",
                        "Message / Type": log.get("message") or log.get("event_type") or f"Event ID: {log.get('event_id')}",
                    })

    return pd.DataFrame(all_logs)


# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
if not os.path.exists(DB_PATH):
    st.warning(f"⚠️ Database not found at `{DB_PATH}`")
else:
    try:
        df = load_logs(limit=50)
    except Exception as e:
        st.error(f"❌ Error reading database: {e}")
        df = pd.DataFrame()

    if df.empty:
        st.info("No system logs found in the database records.")
    else:
        st.markdown('<div class="section-title">📋 Recent System Events</div>', unsafe_allow_html=True)

        # --- Summary metric cards -------------------------------------
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Events</div>
                <div class="value">{len(df)}</div>
            </div>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Hosts Reporting</div>
                <div class="value">{df['Hostname'].nunique()}</div>
            </div>""", unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Distinct Sources</div>
                <div class="value">{df['Source'].nunique()}</div>
            </div>""", unsafe_allow_html=True)
        with s4:
            latest_ts = df.iloc[0]["Record Time"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Most Recent</div>
                <div class="value" style="font-size:1.05rem;">{latest_ts}</div>
            </div>""", unsafe_allow_html=True)

        st.write("")

        # --- Filters -----------------------------------------------------
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search = st.text_input("🔍 Search message", placeholder="Filter by keyword...")
        with f2:
            hosts = ["All hosts"] + sorted(df["Hostname"].unique().tolist())
            host_filter = st.selectbox("Hostname", hosts)
        with f3:
            sources = ["All sources"] + sorted(df["Source"].unique().tolist())
            source_filter = st.selectbox("Source", sources)

        filtered = df.copy()
        if search:
            filtered = filtered[filtered["Message / Type"].str.contains(search, case=False, na=False)]
        if host_filter != "All hosts":
            filtered = filtered[filtered["Hostname"] == host_filter]
        if source_filter != "All sources":
            filtered = filtered[filtered["Source"] == source_filter]

        st.write("")

        # --- Table ---------------------------------------------------------
        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
            height=480,
            column_config={
                "Record Time": st.column_config.TextColumn("Record Time", width="medium"),
                "Hostname": st.column_config.TextColumn("Hostname", width="small"),
                "Time Generated": st.column_config.TextColumn("Time Generated", width="medium"),
                "Source": st.column_config.TextColumn("Source", width="small"),
                "Message / Type": st.column_config.TextColumn("Message / Type", width="large"),
            },
        )

        st.caption(
            f"Showing {len(filtered)} of {len(df)} event(s) · refreshed at {datetime.now().strftime('%H:%M:%S')}"
        )