import streamlit as st

st.set_page_config(
    page_title="Ask Agent",
    page_icon="💬",
    layout="wide",
)

st.title("Ask the Tech IT Agent")

# Navigation buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📄 List Records", use_container_width=True):
        st.switch_page("pages/1_List_Records.py")
with col3:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.info("AI Agent is ready to assist you!")
with col4:
    if st.button("📝 System Logs", use_container_width=True):
        st.switch_page("pages/3_Logs.py")

st.divider()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question about the workstations?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = f"I am a simulated IT Agent. You asked: {prompt}"
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
