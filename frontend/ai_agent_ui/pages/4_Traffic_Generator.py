import streamlit as st
import requests
import time
import random

st.set_page_config(page_title="Traffic Generator", page_icon="🚦", layout="wide")

st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 16px;
        padding: 36px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .page-header h1 {
        color: #ffffff;
        font-size: 2.1rem;
        margin: 0;
    }
    .page-header p {
        color: #9ca3af;
        margin: 8px 0 0 0;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>🚦 Traffic & Load Generator</h1>
    <p>Generate realistic API traffic to test Prometheus metrics and Grafana dashboards.</p>
</div>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"

endpoints = [
    ("GET", "/api/health", 200),
    ("GET", "/api/telemetry", 200),
    ("POST", "/api/resource", 200),
    ("GET", "/api/slow", 200),
    ("GET", "/api/error", 500),
    ("GET", "/api/not-found", 404)
]
weights = [0.4, 0.3, 0.1, 0.1, 0.05, 0.05]

def make_request(method, endpoint):
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            return requests.get(url, timeout=5).status_code
        elif method == "POST":
            return requests.post(url, json={"data": "test"}, timeout=5).status_code
    except Exception as e:
        return "Error"

if "continuous" not in st.session_state:
    st.session_state.continuous = False

if "total_reqs" not in st.session_state:
    st.session_state.total_reqs = 0

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔄 Continuous Traffic")
    st.write("Automatically send background HTTP requests to simulate active users.")
    
    if not st.session_state.continuous:
        if st.button("▶️ Start Continuous Traffic", type="primary"):
            st.session_state.continuous = True
            st.rerun()
    else:
        if st.button("⏹️ Stop Traffic", type="secondary"):
            st.session_state.continuous = False
            st.rerun()
        
        # Make one request per loop
        method, endpoint, _ = random.choices(endpoints, weights=weights, k=1)[0]
        status = make_request(method, endpoint)
        st.session_state.total_reqs += 1
        
        st.info(f"**Running...** Total requests sent: {st.session_state.total_reqs}")
        st.write(f"Last request: `{method} {endpoint}` -> Status: `{status}`")
        
        time.sleep(0.5)  # 2 requests per second
        st.rerun()

with col2:
    st.subheader("🚀 Manual Batch Generation")
    st.write("Send a fixed number of requests immediately.")
    num_requests = st.slider("Requests to send", 1, 200, 20)
    
    if st.button("Send Batch", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = {}
        
        for i in range(num_requests):
            method, endpoint, _ = random.choices(endpoints, weights=weights, k=1)[0]
            status = make_request(method, endpoint)
            results[status] = results.get(status, 0) + 1
            
            progress_bar.progress((i + 1) / num_requests)
            status_text.text(f"Sent {i + 1}/{num_requests} requests...")
            time.sleep(0.05)
            
        st.success("Batch complete!")
        st.write("### Results Summary")
        for stat, count in results.items():
            st.write(f"- Status `{stat}`: {count} times")

st.divider()
st.subheader("🧪 Test Individual Endpoints")
cols = st.columns(3)
for idx, (method, endpoint, expected) in enumerate(endpoints):
    with cols[idx % 3]:
        if st.button(f"Test {method} {endpoint}", key=f"btn_{idx}"):
            start_time = time.time()
            status = make_request(method, endpoint)
            elapsed = time.time() - start_time
            if status == expected:
                st.success(f"Status: {status} ({elapsed:.2f}s)")
            else:
                st.error(f"Status: {status} ({elapsed:.2f}s)")
