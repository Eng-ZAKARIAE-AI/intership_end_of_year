import streamlit as st
import pandas as pd
import os
import sqlite3
import json

st.set_page_config(
    page_title="System Logs",
    page_icon="📝",
    layout="wide",
)

st.title("System Logs")

# Navigation buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📄 List Records", use_container_width=True):
        st.switch_page("pages/1_List_Records.py")
with col3:
    if st.button("💬 Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")
with col4:
    st.button("📝 System Logs", use_container_width=True, disabled=True)

st.divider()

st.subheader("Recent System Events")

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "system_event_loader", "telemetry_edge.db"))

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, payload FROM telemetry_buffer ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()
        
        all_logs = []
        for row in rows:
            record_ts, payload_str = row
            try:
                payload = json.loads(payload_str)
                metrics = payload.get("metrics", {})
                hostname = metrics.get("hostname", "Unknown")
                
                logs = payload.get("logs", [])
                if isinstance(logs, list):
                    for log in logs:
                        if isinstance(log, dict) and not "error" in log:
                            log_entry = {
                                "Record Time": record_ts,
                                "Hostname": hostname,
                                "Time Generated": log.get("timestamp") or log.get("time_generated") or "Unknown",
                                "Source": log.get("source_name") or "Unknown",
                                "Message / Type": log.get("message") or log.get("event_type") or f"Event ID: {log.get('event_id')}",
                            }
                            all_logs.append(log_entry)
            except json.JSONDecodeError:
                continue
        conn.close()
        
        if all_logs:
            df = pd.DataFrame(all_logs)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No system logs found in the database records.")
    except Exception as e:
        st.error(f"Error reading database: {e}")
else:
    st.warning(f"Database not found at {db_path}")
