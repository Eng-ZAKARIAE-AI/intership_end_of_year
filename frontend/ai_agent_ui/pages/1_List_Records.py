import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Workstation Records",
    page_icon="📄",
    layout="wide",
)

st.title("Workstation Records")

# Navigation buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.info("AI Agent is ready to assist you!")
with col3:
    if st.button("💬 Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")
with col4:
    if st.button("📝 System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

st.divider()

if st.button("Show Records", type="primary"):
    st.subheader("Principal Workstation Information")
    
    # Read from SQLite Database
    import os
    import sqlite3
    import json
    
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "system_event_loader", "telemetry_edge.db"))
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, payload, synced FROM telemetry_buffer ORDER BY timestamp DESC LIMIT 10")
            rows = cursor.fetchall()
            
            parsed_data = []
            for row in rows:
                record_id, ts, payload_str, synced = row
                try:
                    payload = json.loads(payload_str)
                    metrics = payload.get("metrics", {})
                    peripherals = payload.get("peripherals", {})
                    
                    # Process GPUs
                    gpus = metrics.get("gpus", [])
                    gpu_info = ", ".join([g.get("name", "GPU") for g in gpus]) if isinstance(gpus, list) and gpus else "None"
                    
                    # Process Printers
                    printers = peripherals.get("printers", [])
                    printer_count = len(printers) if isinstance(printers, list) else 0
                    
                    # Process USB Devices
                    usbs = peripherals.get("usb_devices", [])
                    usb_count = len(usbs) if isinstance(usbs, list) else 0

                    parsed_data.append({
                        "ID": record_id,
                        "Timestamp": ts,
                        "Hostname": metrics.get("hostname", "Unknown"),
                        "OS": metrics.get("platform", "Unknown"),
                        "CPU (%)": metrics.get("cpu", {}).get("usage_percent", ""),
                        "RAM (%)": metrics.get("memory", {}).get("used_percent", ""),
                        "GPUs": gpu_info,
                        "Printers": printer_count,
                        "USB Devices": usb_count,
                        "Synced": "Yes" if synced else "No"
                    })
                except json.JSONDecodeError:
                    continue
            conn.close()
            
            if parsed_data:
                df = pd.DataFrame(parsed_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No records found in the database.")
        except Exception as e:
            st.error(f"Error reading database: {e}")
    else:
        st.warning(f"Database not found at {db_path}")
