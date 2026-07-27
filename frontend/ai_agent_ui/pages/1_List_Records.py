import streamlit as st
import pandas as pd
import os
import sqlite3
import json
from datetime import datetime

st.set_page_config(
    page_title="Workstation Records",
    page_icon="📄",
    layout="wide",
)

# ---------------------------------------------------------------------------
# STYLING
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Overall page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hide default Streamlit chrome that clutters the look */
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

    /* Primary "Show Records" button */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.6rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
        transition: all 0.15s ease;
    }
    .stButton button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.45);
    }

    /* Section subheader */
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

    /* Dataframe container polish */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Info / warning / error boxes */
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
    <h1>📄 Workstation Records</h1>
    <p>Live telemetry snapshot pulled directly from the edge database</p>
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
    if st.button("🤖  AI Agent", use_container_width=True):
        st.toast("AI Agent is ready to assist you!", icon="🤖")
with col3:
    if st.button("💬  Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")
with col4:
    if st.button("📝  System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

st.write("")
st.divider()

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "backend", "system_event_loader", "telemetry_edge.db"
))


def load_records(limit: int = 10) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, timestamp, payload, synced FROM telemetry_buffer "
        "ORDER BY timestamp DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    parsed = []
    for record_id, ts, payload_str, synced in rows:
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            continue

        metrics = payload.get("metrics", {})
        peripherals = payload.get("peripherals", {})

        gpus = metrics.get("gpus", [])
        gpu_info = ", ".join(g.get("name", "GPU") for g in gpus) if isinstance(gpus, list) and gpus else "None"

        printers = peripherals.get("printers", [])
        printer_count = len(printers) if isinstance(printers, list) else 0

        usbs = peripherals.get("usb_devices", [])
        usb_count = len(usbs) if isinstance(usbs, list) else 0

        parsed.append({
            "ID": record_id,
            "Timestamp": ts,
            "Hostname": metrics.get("hostname", "Unknown"),
            "OS": metrics.get("platform", "Unknown"),
            "CPU (%)": metrics.get("cpu", {}).get("usage_percent", None),
            "RAM (%)": metrics.get("memory", {}).get("used_percent", None),
            "GPUs": gpu_info,
            "Printers": printer_count,
            "USB Devices": usb_count,
            "Synced": "Yes" if synced else "No",
        })

    return pd.DataFrame(parsed)


# ---------------------------------------------------------------------------
# ACTION
# ---------------------------------------------------------------------------
if "show_records" not in st.session_state:
    st.session_state.show_records = False

trigger_col, _ = st.columns([1, 5])
with trigger_col:
    if st.button("🔄  Show Records", type="primary", use_container_width=True):
        st.session_state.show_records = True

if st.session_state.show_records:

    if not os.path.exists(DB_PATH):
        st.warning(f"⚠️ Database not found at `{DB_PATH}`")
    else:
        try:
            df = load_records(limit=10)
        except Exception as e:
            st.error(f"❌ Error reading database: {e}")
            df = pd.DataFrame()

        if df.empty:
            st.info("No records found in the database.")
        else:
            st.markdown('<div class="section-title">🖥️ Principal Workstation Information</div>', unsafe_allow_html=True)

            # --- Summary metric cards -------------------------------------
            latest = df.iloc[0]
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">Latest Host</div>
                    <div class="value">{latest['Hostname']}</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                cpu_val = latest["CPU (%)"]
                cpu_display = f"{cpu_val:.1f}%" if isinstance(cpu_val, (int, float)) else "N/A"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">CPU Usage</div>
                    <div class="value">{cpu_display}</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                ram_val = latest["RAM (%)"]
                ram_display = f"{ram_val:.1f}%" if isinstance(ram_val, (int, float)) else "N/A"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">RAM Usage</div>
                    <div class="value">{ram_display}</div>
                </div>""", unsafe_allow_html=True)
            with m4:
                synced_count = (df["Synced"] == "Yes").sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">Synced Records</div>
                    <div class="value">{synced_count} / {len(df)}</div>
                </div>""", unsafe_allow_html=True)

            st.write("")

            # --- Styled data table ------------------------------------------
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                    "Hostname": st.column_config.TextColumn("Hostname", width="medium"),
                    "OS": st.column_config.TextColumn("OS", width="small"),
                    "CPU (%)": st.column_config.ProgressColumn(
                        "CPU (%)", min_value=0, max_value=100, format="%.1f%%"
                    ),
                    "RAM (%)": st.column_config.ProgressColumn(
                        "RAM (%)", min_value=0, max_value=100, format="%.1f%%"
                    ),
                    "GPUs": st.column_config.TextColumn("GPUs", width="large"),
                    "Printers": st.column_config.NumberColumn("Printers", width="small"),
                    "USB Devices": st.column_config.NumberColumn("USB Devices", width="small"),
                    "Synced": st.column_config.TextColumn("Synced", width="small"),
                },
            )

            st.caption(f"Showing {len(df)} most recent record(s) · refreshed at {datetime.now().strftime('%H:%M:%S')}")