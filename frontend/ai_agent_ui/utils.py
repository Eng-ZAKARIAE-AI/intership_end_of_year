import os
import sqlite3
import streamlit as st
from functools import lru_cache


@lru_cache(maxsize=1)
def get_db_path() -> str:
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "backend",
            "system_event_loader",
            "telemetry_edge.db",
        )
    )


@st.cache_resource
def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def close_connection(conn: sqlite3.Connection) -> None:
    try:
        conn.close()
    except Exception:
        pass


PAGES = {
    "Home": "app.py",
    "List Records": "pages/1_List_Records.py",
    "Ask Agent": "pages/2_Ask_Agent.py",
    "System Logs": "pages/3_Logs.py",
}

NAV_ICONS = {
    "Home": "🏠",
    "List Records": "📄",
    "Ask Agent": "🤖",
    "System Logs": "📝",
}


def render_navigation(current: str) -> None:
    labels = list(PAGES.keys())
    cols = st.columns(len(labels), gap="small")
    for col, label in zip(cols, labels):
        with col:
            target = PAGES[label]
            disabled = target == "app.py" and current != "Home"
            if st.button(
                f"{NAV_ICONS[label]} {label}",
                use_container_width=True,
                disabled=disabled,
                key=f"nav_{label}",
            ):
                if label == "Ask Agent":
                    st.session_state.show_ai = True
                else:
                    st.switch_page(target)
