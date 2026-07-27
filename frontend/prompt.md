# TASK: Replace the Streamlit frontend files with the exact code below

You are working inside an existing project with this structure:

```
<repo-root>/
├── backend/
│   └── system_event_loader/
│       └── telemetry_edge.db
├── frontend/
│   └── ai_agent_ui/
│       ├── app.py
│       ├── utils.py
│       ├── requirements.txt
│       └── pages/
│           ├── 1_List_Records.py
│           ├── 2_Ask_Agent.py
│           └── 3_Logs.py
├── main.py
├── Makefile
└── pyproject.toml
```

Your job is to **overwrite 4 files** with the exact code given below. Do not summarize, do not "improve," do not rename variables, do not reformat — copy the code exactly as written into each file. These files already work and were tested; the only thing that can break them is you changing something.

Follow these steps **in this exact order**. Do not skip a step. Do not combine steps.

---

## STEP 0 — Locate the project root

Before touching anything, find the folder that contains both `backend/` and `frontend/` as direct children. That folder is `<repo-root>` for every path below. If you cannot find both `backend/` and `frontend/` under a common parent, STOP and ask the user where the backend database lives — do not guess.

---

## STEP 1 — Overwrite `frontend/ai_agent_ui/app.py`

Delete the entire existing content of this file and replace it with exactly this:

```python
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
```

**Why the DB_PATH matters:** `app.py` lives at `frontend/ai_agent_ui/app.py`. To reach `backend/system_event_loader/telemetry_edge.db`, the code must go up 2 directories (`ai_agent_ui` → `frontend` → repo root), then down into `backend/`. That is exactly what `"..", ".."` does. Do not add or remove a `".."` — if you do, the database will not be found.

---

## STEP 2 — Overwrite `frontend/ai_agent_ui/pages/1_List_Records.py`

Delete the entire existing content of this file and replace it with exactly this:

```python
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
```

**Why the DB_PATH matters:** this file lives at `frontend/ai_agent_ui/pages/1_List_Records.py`, one folder deeper than `app.py`. It must go up **3** directories (`pages` → `ai_agent_ui` → `frontend` → repo root). Do not change this to 2 `".."` — that would point one folder too high and the database won't be found.

---

## STEP 3 — Overwrite `frontend/ai_agent_ui/pages/2_Ask_Agent.py`

Delete the entire existing content of this file and replace it with exactly this:

```python
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
```

**Note:** the assistant reply is currently a hardcoded placeholder (`f"I am a simulated IT Agent. You asked: {prompt}"`). This file does **not** call any real AI model. If a real backend/agent endpoint exists (check `utils.py` and `main.py` for something like `call_agent()`, `ask_agent()`, or an HTTP client), STOP after this step and tell the user what function you found so they can decide how to wire it in — do not invent an API call yourself.

---

## STEP 4 — Overwrite `frontend/ai_agent_ui/pages/3_Logs.py`

Delete the entire existing content of this file and replace it with exactly this:

```python
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
```

**Why the DB_PATH matters:** same as Step 2 — this file is also inside `pages/`, so it needs 3 `".."` to reach the repo root.

---

## STEP 5 — Check `requirements.txt`

Open `frontend/ai_agent_ui/requirements.txt`. Make sure it contains at least these packages (add any that are missing, do not remove anything already there for other features):

```
streamlit
pandas
```

`os`, `sqlite3`, `json`, and `datetime` are Python standard library — do NOT add them to requirements.txt.

---

## STEP 6 — Do NOT touch these files

Do not modify, rename, or delete:
- `frontend/ai_agent_ui/utils.py`
- `backend/system_event_loader/telemetry_edge.db`
- `main.py`
- `Makefile`
- `pyproject.toml`
- `.gitignore`, `.python-version`, `docker-compose.yml`, `LICENSE`

If any of these files need to change to make the app work (for example, `utils.py` needs a new function), STOP and describe exactly what you think needs to change and why, before making the edit.

---

## STEP 7 — Verify the database table exists

Run this command from the repo root to confirm the table name and columns match what the code expects (`telemetry_buffer` with columns `id, timestamp, payload, synced`):

```bash
sqlite3 backend/system_event_loader/telemetry_edge.db ".schema telemetry_buffer"
```

If the table or any of those column names differ, STOP and report the actual schema — do not silently rename columns in the Python code to match, since that could break other parts of the system (e.g. `system_event_loader`) that also write to this table.

---

## STEP 8 — Run the app and verify

From the repo root:

```bash
cd frontend/ai_agent_ui
pip install -r requirements.txt
streamlit run app.py
```

Then check ALL of the following manually in the browser (do not assume — actually click through):

1. **Home page (`app.py`)** loads with a dark hero banner titled "Workstation Dashboard" and 4 nav buttons at the top.
2. Quick Overview cards show real numbers (Total Records, Synced Records, Sync Rate, Last Update) — NOT all zeros/N/A, unless the database is genuinely empty.
3. Clicking **"List Records"** (either the nav button or the feature card) navigates to the Records page.
4. On the Records page, clicking **"🔄 Show Records"** displays a table with 10 rows and 4 metric cards above it.
5. Clicking **"Ask Agent"** navigates to the chat page; typing a message and pressing enter shows both the user bubble and a simulated agent reply.
6. Clicking **"🗑️ Clear"** on the chat page empties the conversation.
7. Clicking **"System Logs"** navigates to the logs page; the table loads, and typing in the search box or changing the Hostname/Source dropdowns filters the visible rows.
8. On every page, clicking **"🏠 Home"** returns to `app.py`.

If any step fails, report the exact error message and which step it happened on. Do not attempt to fix it by changing the DB_PATH `".."` count unless you have re-confirmed the actual file locations with `pwd` and `find`.

---

## ACCEPTANCE CHECKLIST (must all be true when done)

- [ ] All 4 files above were overwritten with the exact code given, no modifications
- [ ] `app.py` DB_PATH uses `"..", ".."` (2 levels)
- [ ] `pages/1_List_Records.py` DB_PATH uses `"..", "..", ".."` (3 levels)
- [ ] `pages/2_Ask_Agent.py` has no DB_PATH (it doesn't need the database)
- [ ] `pages/3_Logs.py` DB_PATH uses `"..", "..", ".."` (3 levels)
- [ ] `streamlit run app.py` starts with no errors
- [ ] All 8 manual checks in Step 8 pass
- [ ] No file outside the 4 listed in Steps 1–4 was modified