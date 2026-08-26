"""리콜체크 Streamlit 조회 화면.

실행 방법(프로젝트 루트에서):
    python -m streamlit run app/streamlit_app.py

화면은 SQLite를 읽기만 하며, 원본 CSV나 DB를 수정하지 않는다.
차량 사진은 ``assets/vehicles`` 폴더에
``제조사_차종.jpg`` 또는 ``제조사_차종.webp`` 형태로 넣으면 자동으로 찾는다.
"""

from __future__ import annotations

from datetime import date

import streamlit as st

from config import PUBLIC_AD_HIDE_COOKIE, SERVICE_LOGO_PATH, STYLES_PATH

# 다른 모듈의 @st.dialog 등록보다 먼저 페이지 설정을 호출해야 한다.
st.set_page_config(
    page_title="리콜체크 | 중고차 결함·리콜 조회",
    page_icon=str(SERVICE_LOGO_PATH),
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"<style>\n{STYLES_PATH.read_text(encoding='utf-8')}\n</style>",
    unsafe_allow_html=True,
)

from db import load_manufacturers
from ui.chrome import (
    persist_hide_public_ad_today,
    render_hero,
    render_interest_summary,
    render_public_service_ad,
    render_site_header,
)
from ui.compare import render_compare
from ui.help import render_help
from ui.search import render_dashboard, render_recall_search

try:
    load_manufacturers()
except FileNotFoundError as error:
    st.error(str(error))
    st.info("프로젝트 루트에서 `python scripts/build_database.py`를 먼저 실행하세요.")
    st.stop()

# 조회 버튼을 누른 조건을 기억한다. 상단 탭을 바꿔도 리콜 조회 결과를 유지한다.
if "search_state" not in st.session_state:
    st.session_state.search_state = None
if "interest_cars" not in st.session_state:
    st.session_state.interest_cars = []
if "compare_preview" not in st.session_state:
    st.session_state.compare_preview = None
if "public_ad_open" not in st.session_state:
    hidden_date = st.context.cookies.get(PUBLIC_AD_HIDE_COOKIE)
    st.session_state.public_ad_open = hidden_date != date.today().isoformat()

# 앱을 새로 열었을 때만 공익광고를 표시합니다.
# 우측 상단 X를 누르면 현재 세션에서는 닫힌 상태로 유지됩니다.
# "오늘 하루동안 보지않기"를 선택한 뒤 닫으면 자정까지 다시 보이지 않습니다.
if st.session_state.get("persist_hide_public_ad"):
    persist_hide_public_ad_today()
if st.session_state.get("public_ad_open", True):
    render_public_service_ad()

render_site_header()
render_hero()
with st.container(key="header-interest", horizontal=True, horizontal_alignment="right"):
    render_interest_summary()
recall_tab, compare_tab, help_tab = st.tabs([
    ":material/search: 차량 조회",
    ":material/compare_arrows: 차종 비교",
    ":material/help: 도움말",
])

with recall_tab:
    render_recall_search()
    render_dashboard()

with compare_tab:
    render_compare()

with help_tab:
    render_help()
