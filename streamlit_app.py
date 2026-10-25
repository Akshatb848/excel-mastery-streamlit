"""Excel Mastery for Mac on Streamlit.

The course itself is a static website (GitHub Pages). This app shows it full screen,
adds direct links (?lesson=S07-02, ?page=functions) and offers the practice workbooks
as downloads from Streamlit, so learners can always get the files.
"""
import re
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components

try:
    SITE_URL = st.secrets["SITE_URL"]
except Exception:
    SITE_URL = "https://akshatb848.github.io/excel-mastery-course/"
HERE = Path(__file__).parent
WORKBOOKS = sorted((HERE / "workbooks").glob("*.xlsx"))
PAGES = {"course", "functions", "tips", "shortcuts", "help"}

st.set_page_config(page_title="Excel Mastery for Mac", page_icon="📗", layout="wide", initial_sidebar_state="collapsed")

# Full-bleed: hide Streamlit's own chrome so the course fills the window.
st.markdown(
    """
    <style>
      header[data-testid="stHeader"] {background: transparent; height: 0; min-height: 0; overflow: visible; z-index: 100000;}
      footer, #MainMenu {visibility: hidden; height: 0;}
      .stAppDeployButton, [data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
      [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] {
        position: fixed !important; left: 14px; bottom: 92px; top: auto !important; z-index: 1000;
        background: #0e7a4a; color: #fff; border-radius: 999px; box-shadow: 0 6px 18px -6px rgba(0,0,0,.45);}
      [data-testid="stExpandSidebarButton"] svg, [data-testid="stSidebarCollapsedControl"] svg {color: #fff; fill: #fff;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      [data-testid="stAppViewContainer"] > .main {padding: 0;}
      [data-testid="stVerticalBlock"] {gap: 0 !important;}
      iframe[title="streamlit_app.course"], iframe {display: block; width: 100%; height: 100vh !important; height: 100dvh !important; border: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def site_is_up(url: str) -> bool:
    try:
        r = requests.get(url, timeout=8)
        return r.status_code == 200 and "Excel Mastery" in r.text
    except requests.RequestException:
        return False


def start_anchor() -> str:
    q = st.query_params
    lesson = str(q.get("lesson", "")).strip().upper()
    if re.fullmatch(r"S\d{2}(-\d{2})?", lesson):
        return "#" + lesson
    page = str(q.get("page", "")).strip().lower()
    return "#" + page if page in PAGES else ""


with st.sidebar:
    st.markdown("### Practice workbooks")
    st.caption("One workbook per section. Each lesson has its own sheet, plus a finished “Done” copy to compare with.")
    for wb in WORKBOOKS:
        st.download_button(
            label=wb.stem.replace("_", " "),
            data=wb.read_bytes(),
            file_name=wb.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl-{wb.stem}",
            use_container_width=True,
        )
    st.divider()
    st.markdown(f"[Open the course in a full browser tab]({SITE_URL})")
    st.caption("Your progress is saved in this browser.")

if site_is_up(SITE_URL):
    components.iframe(SITE_URL + start_anchor(), height=900, scrolling=True)
else:
    st.markdown("## Excel Mastery for Mac")
    st.warning("The course website is not responding right now. It usually comes back within a few minutes.")
    st.markdown(f"Try opening it directly: [{SITE_URL}]({SITE_URL})")
    if st.button("Check again"):
        site_is_up.clear()
        st.rerun()
