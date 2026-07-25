import streamlit as st

st.set_page_config(
    page_title="Workstation Dashboard",
    page_icon="🖥️",
    layout="wide",
)

st.title("Home - Workstation Dashboard")

# Navigation Bar simulation if requested, though Streamlit provides a sidebar naturally
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.session_state.show_ai = True

with col2:
    if st.button("📄 List Records", use_container_width=True):
        st.switch_page("pages/1_List_Records.py")

with col3:
    if st.button("💬 Ask Agent", use_container_width=True):
        st.switch_page("pages/2_Ask_Agent.py")

with col4:
    if st.button("📝 System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

if st.session_state.get('show_ai', False):
    st.info("AI Agent is ready to assist you!")
