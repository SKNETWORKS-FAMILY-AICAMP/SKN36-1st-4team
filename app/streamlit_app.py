"""리콜체크 Streamlit 조회 화면.

실행 방법(프로젝트 루트에서):
    streamlit run app/streamlit_app.py

화면은 SQLite를 읽기만 하며, 원본 CSV나 DB를 수정하지 않는다.
차량 사진은 나중에 ``assets/vehicles`` 폴더에
``제조사_차종.jpg`` 또는 ``제조사_차종.webp`` 형태로 넣으면 자동으로 찾는다.
"""

from __future__ import annotations

import html
import re
import sqlite3
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# 프로젝트 경로와 기본 화면 설정
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "processed" / "database" / "recall_checker.sqlite3"
IMAGE_DIR = PROJECT_ROOT / "assets" / "vehicles"

# 공식 확인 링크
# 정부 자동차리콜센터는 모든 조회 결과에서 공통으로 안내하고,
# 선택한 제조사는 공식 홈페이지의 고객지원 메뉴로 이동할 수 있게 한다.
GOVERNMENT_RECALL_URL = "https://car.go.kr/ri/stat/list.do?menuId=0203010000"
MANUFACTURER_OFFICIAL_URLS = {
    "KG 모빌리티": "https://www.kg-mobility.com/",
    "BMW": "https://www.bmw.co.kr/",
    "기아": "https://www.kia.com/kr/",
    "르노코리아": "https://www.renault.co.kr/",
    "메르세데스 벤츠": "https://www.mercedes-benz.co.kr/",
    "볼보": "https://www.volvocars.com/kr/",
    "토요타": "https://www.toyota.co.kr/",
    "재규어랜드로버": "https://www.jaguarkorea.co.kr/",
    "포드": "https://www.ford.co.kr/",
    "현대자동차": "https://www.hyundai.com/kr/ko",
    "혼다코리아": "https://www.hondakorea.co.kr/",
}

st.set_page_config(
    page_title="리콜체크 | 중고차 결함·리콜 조회",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# 화면 스타일
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --navy: #14213d;
        --blue: #2f6fce;
        --sky: #eef5ff;
        --line: #dce7f5;
        --muted: #71809a;
        --green: #208567;
        --orange: #e78932;
    }
    .stApp { background: #f7faff; }
    section[data-testid="stSidebar"] {
        width: 420px !important;
        min-width: 420px !important;
        max-width: 460px !important;
        background: #ffffff;
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] > div:first-child {
        width: 420px !important;
        padding-top: 1.5rem;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.06rem !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        min-height: 54px;
        font-size: 1.04rem;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        font-size: 1.02rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: .18rem 0;
    }
    section[data-testid="stSidebar"] [data-testid="stButton"] button {
        min-height: 54px;
        font-size: 1.06rem;
    }
    div[role="listbox"] * { font-size: 1rem !important; }
    /* 본문 비교 화면의 제조사·차종·연식 선택 상자도 같은 크기로 맞춘다. */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.04rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        min-height: 52px;
        font-size: 1rem;
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] * {
        font-size: 1rem !important;
    }
    /* FAQ와 리콜 사유는 긴 문장을 읽는 영역이므로 일반 본문보다 크게 표시한다. */
    [data-testid="stExpander"] summary p {
        font-size: 1.08rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
        font-size: 1rem !important;
        line-height: 1.75 !important;
    }
    .link-note {
        color: var(--muted); font-size: .86rem; line-height: 1.6;
        margin: .35rem 0 .65rem;
    }
    .brand { display:flex; align-items:center; gap:.65rem; margin-bottom:.2rem; }
    .brand-mark {
        width: 38px; height: 38px; border-radius: 12px;
        display:flex; align-items:center; justify-content:center;
        background: linear-gradient(135deg, #2f6fce, #62a5ff);
        color:white; font-size: 1.25rem;
        box-shadow: 0 8px 20px rgba(47,111,206,.25);
    }
    .brand-title { font-size: 1.35rem; font-weight: 800; color: var(--navy); }
    .brand-subtitle { color: var(--muted); font-size: .78rem; margin: .1rem 0 1.2rem 3.05rem; }
    .hero {
        padding: 2.1rem 2.25rem; border-radius: 24px;
        background: linear-gradient(115deg, #14213d 0%, #24599d 65%, #4d93e8 100%);
        color: white; margin-bottom: 1.35rem;
        box-shadow: 0 15px 35px rgba(37, 82, 145, .18);
    }
    .hero h1 { font-size: 2.1rem; letter-spacing: -.04em; margin: 0 0 .5rem; }
    .hero p { color: #dbeaff; margin: 0; font-size: 1rem; }
    .eyebrow { font-size: .78rem; letter-spacing: .12em; color: #9fc7ff; font-weight: 700; margin-bottom: .65rem; }
    .section-title { color: var(--navy); font-size: 1.25rem; font-weight: 800; margin: .2rem 0 .2rem; }
    .section-caption { color: var(--muted); font-size: .9rem; margin: 0 0 .8rem; }
    .card {
        background: #fff; border: 1px solid var(--line); border-radius: 18px;
        padding: 1.25rem 1.35rem; box-shadow: 0 8px 26px rgba(26, 71, 125, .05);
    }
    .car-card {
        min-height: 235px; border-radius: 18px; overflow: hidden;
        background: linear-gradient(145deg, #eff5ff, #dceaff);
        display:flex; align-items:center; justify-content:center;
        border: 1px solid var(--line);
    }
    .car-placeholder { text-align:center; color:#4d78aa; }
    .car-placeholder .emoji { font-size: 4.1rem; display:block; margin-bottom:.3rem; }
    .metric-label { color: var(--muted); font-size: .82rem; margin-bottom: .25rem; }
    .metric-value { color: var(--navy); font-size: 1.65rem; font-weight: 800; }
    .metric-note { color: var(--muted); font-size: .73rem; margin-top:.25rem; }
    .notice {
        border-left: 4px solid var(--orange); background: #fff8ef;
        color: #80501f; padding: .85rem 1rem; border-radius: 10px;
        font-size: .86rem; margin: .6rem 0 1rem;
    }
    .source-note { color: var(--muted); font-size: .76rem; margin-top: 1rem; }
    .empty-state { text-align:center; padding: 4rem 1rem; color:var(--muted); }
    .empty-state .emoji { font-size: 3rem; display:block; margin-bottom:.6rem; }
    div[data-testid="stMetric"] {
        background: #fff; border: 1px solid var(--line); border-radius: 15px;
        padding: .8rem 1rem;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--blue); border-color: var(--blue); border-radius: 10px;
        font-weight: 700;
    }
    .small-pill {
        display:inline-block; background:#e9f2ff; color:#2f6fce; border-radius:999px;
        padding:.25rem .65rem; font-size:.75rem; font-weight:700; margin-right:.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# SQLite 공통 함수
# ---------------------------------------------------------------------------
@st.cache_resource
def get_connection() -> sqlite3.Connection:
    """앱이 실행되는 동안 재사용할 SQLite 연결을 연다."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite DB를 찾지 못했습니다: {DB_PATH}")
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


@st.cache_data(ttl=300)
def read_query(query: str, params: tuple | dict = ()) -> pd.DataFrame:
    """읽기 전용 SQL을 실행하고 DataFrame으로 돌려준다."""
    connection = get_connection()
    return pd.read_sql_query(query, connection, params=params)


def clean_key(value: str) -> str:
    """사진 파일을 찾을 때 사용할 비교용 문자열."""
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"[^0-9a-z가-힣]+", "", text)


def find_car_image(manufacturer: str, model: str) -> Path | None:
    """assets/vehicles에서 제조사·차종에 맞는 첫 번째 사진을 찾는다."""
    if not IMAGE_DIR.exists():
        return None

    manufacturer_key = clean_key(manufacturer)
    model_key = clean_key(model)
    extensions = {".jpg", ".jpeg", ".png", ".webp"}

    # 파일 이름 전체에 제조사와 차종이 들어간 경우를 우선 찾는다.
    candidates = sorted(
        path for path in IMAGE_DIR.rglob("*") if path.is_file() and path.suffix.lower() in extensions
    )
    for path in candidates:
        key = clean_key(path.stem)
        if manufacturer_key in key and model_key in key:
            return path

    # 제조사 폴더 안에 차종 파일을 넣는 방식도 지원한다.
    for path in candidates:
        if model_key in clean_key(path.stem) and manufacturer_key in clean_key(path.parent.name):
            return path
    return None


def format_number(value: object) -> str:
    """숫자를 화면용 천 단위 구분 문자열로 표시한다."""
    if value is None or pd.isna(value):
        return "0"
    return f"{int(value):,}"


def format_date(value: object) -> str:
    if value is None or pd.isna(value) or str(value) in {"", "None"}:
        return "-"
    return str(value).replace("-", ".")


def render_official_links(manufacturer: str) -> None:
    """조회한 차량을 공식 사이트에서 다시 확인할 수 있는 링크를 표시한다."""
    st.markdown("### 공식 확인 링크")
    st.markdown(
        "<div class='link-note'>이 화면은 차종·생산기간 기준의 참고 정보입니다. "
        "개별 차량의 리콜 조치 완료 여부는 차대번호로 공식 사이트에서 확인하세요.</div>",
        unsafe_allow_html=True,
    )
    link_cols = st.columns(2)
    with link_cols[0]:
        st.link_button("정부 자동차리콜센터", GOVERNMENT_RECALL_URL, width="stretch")
    manufacturer_url = MANUFACTURER_OFFICIAL_URLS.get(manufacturer)
    if manufacturer_url:
        with link_cols[1]:
            st.link_button(f"{manufacturer} 공식 사이트", manufacturer_url, width="stretch")


# ---------------------------------------------------------------------------
# 조회 SQL
# ---------------------------------------------------------------------------
MANUFACTURERS_SQL = """
SELECT manufacturer_id, manufacturer_name
FROM manufacturers
ORDER BY manufacturer_name
"""

MODELS_SQL = """
SELECT model_id, model_name, vehicle_type
FROM vehicle_models
WHERE manufacturer_id = :manufacturer_id
ORDER BY model_name
"""

YEARS_SQL = """
SELECT DISTINCT model_year
FROM defect_reports
WHERE model_id = :model_id AND model_year IS NOT NULL
ORDER BY model_year DESC
"""

OVERVIEW_SQL = """
SELECT model_id, manufacturer_name, model_name, vehicle_type,
       complaint_count, latest_report_date, recall_record_count,
       affected_count_sum, latest_recall_date
FROM model_overview
WHERE model_id = :model_id
"""

RECALLS_SQL = """
SELECT recall_id, raw_model_name, production_start_date, production_end_date,
       recall_start_date, affected_count, recall_reason
FROM recalls
WHERE model_id = :model_id
ORDER BY recall_start_date DESC, recall_id DESC
"""

DEFECT_BY_YEAR_SQL = """
SELECT model_year, COUNT(*) AS complaint_count
FROM defect_reports
WHERE model_id = :model_id AND model_year IS NOT NULL
GROUP BY model_year
ORDER BY model_year
"""

DEFECT_COUNT_SQL = """
SELECT COUNT(*) AS complaint_count
FROM defect_reports
WHERE model_id = :model_id
"""

DEFECT_COUNT_BY_YEAR_SQL = """
SELECT COUNT(*) AS complaint_count
FROM defect_reports
WHERE model_id = :model_id AND model_year = :model_year
"""

VARIANTS_SQL = """
SELECT variant_id, variant_name
FROM vehicle_variants
WHERE model_id = :model_id
ORDER BY variant_name
"""

ALL_MODELS_SQL = """
SELECT vm.model_id, vm.model_name, m.manufacturer_name,
       vm.vehicle_type, mo.complaint_count, mo.recall_record_count,
       mo.affected_count_sum
FROM vehicle_models vm
JOIN manufacturers m ON m.manufacturer_id = vm.manufacturer_id
JOIN model_overview mo ON mo.model_id = vm.model_id
ORDER BY m.manufacturer_name, vm.model_name
"""


# ---------------------------------------------------------------------------
# 사이드바: 제조사 → 차종 → 모델연도 순서의 조회 조건
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    '<div class="brand"><div class="brand-mark">✓</div><div class="brand-title">리콜체크</div></div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown('<div class="brand-subtitle">중고차 구매 전 결함·리콜 확인</div>', unsafe_allow_html=True)

try:
    manufacturers = read_query(MANUFACTURERS_SQL)
except FileNotFoundError as error:
    st.error(str(error))
    st.info("프로젝트 루트에서 `python scripts/build_database.py`를 먼저 실행하세요.")
    st.stop()

menu = st.sidebar.radio("메뉴", ["리콜 조회", "차종 비교", "도움말"], label_visibility="collapsed")
st.sidebar.divider()

manufacturer_names = manufacturers["manufacturer_name"].tolist()
selected_manufacturer = st.sidebar.selectbox("제조사", manufacturer_names)
manufacturer_id = int(
    manufacturers.loc[
        manufacturers["manufacturer_name"] == selected_manufacturer, "manufacturer_id"
    ].iloc[0]
)

models = read_query(MODELS_SQL, {"manufacturer_id": manufacturer_id})
if models.empty:
    st.sidebar.warning("이 제조사에 등록된 차종이 없습니다.")
    selected_model_id = None
    selected_model_name = ""
else:
    model_labels = models.apply(
        lambda row: f"{row['model_name']}  ·  {row['vehicle_type'] or '차종 미분류'}", axis=1
    ).tolist()
    selected_model_label = st.sidebar.selectbox("대표 차종", model_labels)
    selected_model_index = model_labels.index(selected_model_label)
    selected_model_id = int(models.iloc[selected_model_index]["model_id"])
    selected_model_name = str(models.iloc[selected_model_index]["model_name"])

years = (
    read_query(YEARS_SQL, {"model_id": selected_model_id})["model_year"].astype(int).tolist()
    if selected_model_id is not None
    else []
)
year_options: list[str | int] = ["전체 연식"] + years
selected_year = st.sidebar.selectbox("모델연도", year_options)

search_clicked = st.sidebar.button("조회하기", type="primary", width="stretch")
st.sidebar.markdown(
    "<div class='source-note'>공식 리콜과 소유자 결함신고를 분리해서 보여드립니다.<br>신고 건수는 리콜 확정 건수가 아닙니다.</div>",
    unsafe_allow_html=True,
)

# 조회 버튼을 누른 조건을 기억한다. 메뉴를 바꿔도 선택한 결과를 유지한다.
if "search_state" not in st.session_state:
    st.session_state.search_state = None
if search_clicked and selected_model_id is not None:
    st.session_state.search_state = {
        "manufacturer": selected_manufacturer,
        "model_id": selected_model_id,
        "model_name": selected_model_name,
        "year": selected_year,
    }

search = st.session_state.search_state


# ---------------------------------------------------------------------------
# 공통 헤더
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">USED CAR SAFETY CHECK</div>
      <h1>중고차 구매 전, 리콜과 결함을 한눈에</h1>
      <p>제조사가 진행한 공식 리콜과 소유자가 접수한 결함 신고를 구분해 확인하세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def render_empty() -> None:
    st.markdown(
        """
        <div class="card empty-state">
          <span class="emoji">🚘</span>
          <h3>확인할 차량을 선택해 주세요</h3>
          <p>왼쪽에서 제조사와 대표 차종을 고른 뒤 <b>조회하기</b>를 누르면<br>
          공식 리콜 이력과 소비자 결함 신고를 함께 보여드립니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_car_visual(manufacturer: str, model: str) -> None:
    """사진이 있으면 출력하고, 없으면 나중에 사진을 넣을 위치를 보여준다."""
    image_path = find_car_image(manufacturer, model)
    if image_path:
        st.image(str(image_path), width="stretch")
        return
    st.markdown(
        f"""
        <div class="car-card">
          <div class="car-placeholder">
            <span class="emoji">🚙</span>
            <b>{html.escape(model)}</b><br>
            <small>차량 사진을 assets/vehicles에 추가할 수 있습니다</small>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    """선택한 차종의 요약·리콜·신고·세부차명을 표시한다."""
    if not search:
        render_empty()
        return

    model_id = int(search["model_id"])
    manufacturer = str(search["manufacturer"])
    model_name = str(search["model_name"])
    year = search["year"]
    overview = read_query(OVERVIEW_SQL, {"model_id": model_id})
    if overview.empty:
        st.warning("선택한 차종의 요약 정보를 찾지 못했습니다.")
        return
    summary = overview.iloc[0]

    st.markdown(f"<div class='section-caption'>홈 〉 리콜 조회 〉 {html.escape(model_name)}</div>", unsafe_allow_html=True)
    left, right = st.columns([1.05, 2.4], gap="large")
    with left:
        render_car_visual(manufacturer, model_name)
        st.caption("사진은 선택 사항이며, 현재 데이터 조회에는 영향을 주지 않습니다.")
    with right:
        st.markdown(
            f"<span class='small-pill'>{html.escape(manufacturer)}</span>"
            f"<span class='small-pill'>{html.escape(str(summary['vehicle_type'] or '패밀리카'))}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"## {html.escape(model_name)} 리콜·결함 요약")
        if year == "전체 연식":
            complaint_count = int(summary["complaint_count"])
            year_label = "전체 모델연도"
        else:
            year_count = read_query(
                DEFECT_COUNT_BY_YEAR_SQL,
                {"model_id": model_id, "model_year": int(year)},
            )
            complaint_count = int(year_count.iloc[0]["complaint_count"])
            year_label = f"{year}년형 신고"
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric(year_label, format_number(complaint_count), help="소유자가 접수한 원본 신고 행 수입니다.")
        with metric_cols[1]:
            st.metric("공식 리콜 기록", f"{format_number(summary['recall_record_count'])}건")
        with metric_cols[2]:
            st.metric("리콜 대상 대수 합계", f"{format_number(summary['affected_count_sum'])}대")
        st.markdown(
            "<div class='notice'>주의: 리콜 대상 대수는 리콜 기록별 합계입니다. 개별 차량의 조치 완료 여부는 차대번호 조회가 필요합니다.</div>",
            unsafe_allow_html=True,
        )
        render_official_links(manufacturer)

    st.divider()
    tab_recall, tab_defect, tab_variants = st.tabs(["공식 리콜 이력", "소유자 결함 신고", "원본 차명 보기"])

    with tab_recall:
        st.markdown('<div class="section-title">제작사가 진행한 공식 시정조치</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">생산기간, 리콜 개시일, 대상 대수와 리콜 사유를 확인합니다.</div>', unsafe_allow_html=True)
        recalls = read_query(RECALLS_SQL, {"model_id": model_id})
        if recalls.empty:
            st.info("등록된 공식 리콜 기록이 없습니다.")
        else:
            display_recalls = recalls.copy()
            display_recalls["생산기간"] = display_recalls.apply(
                lambda row: f"{format_date(row['production_start_date'])} ~ {format_date(row['production_end_date'])}", axis=1
            )
            display_recalls["리콜 개시일"] = display_recalls["recall_start_date"].map(format_date)
            display_recalls["대상 대수"] = display_recalls["affected_count"].map(lambda x: f"{format_number(x)}대")
            st.dataframe(
                display_recalls[["raw_model_name", "생산기간", "리콜 개시일", "대상 대수"]].rename(
                    columns={"raw_model_name": "원본 차명"}
                ),
                width="stretch",
                hide_index=True,
                column_config={"원본 차명": st.column_config.TextColumn(width="large")},
            )
            for _, recall in recalls.iterrows():
                title = f"{format_date(recall['recall_start_date'])} · {recall['raw_model_name']}"
                with st.expander(title):
                    st.write(recall["recall_reason"] or "리콜 사유가 입력되지 않았습니다.")
                    st.caption(
                        f"생산기간: {format_date(recall['production_start_date'])} ~ {format_date(recall['production_end_date'])}  |  "
                        f"대상 대수: {format_number(recall['affected_count'])}대"
                    )
            st.markdown(
                "<div class='source-note'>출처: 한국교통안전공단 차종별 리콜대수 데이터 · 공식 리콜 여부를 확인하는 참고 정보입니다.</div>",
                unsafe_allow_html=True,
            )

    with tab_defect:
        st.markdown('<div class="section-title">소유자 결함 신고 현황</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="notice">신고 건수는 소유자가 접수한 기록의 개수입니다. 결함 확정이나 리콜 대상 판정을 의미하지 않으며, 판매량이 없는 단순 건수 비교입니다.</div>',
            unsafe_allow_html=True,
        )
        defect_by_year = read_query(DEFECT_BY_YEAR_SQL, {"model_id": model_id})
        if defect_by_year.empty:
            st.info("모델연도가 있는 결함 신고 기록이 없습니다.")
        else:
            defect_by_year["model_year"] = defect_by_year["model_year"].astype(int).astype(str)
            chart = px.bar(
                defect_by_year,
                x="model_year",
                y="complaint_count",
                labels={"model_year": "모델연도", "complaint_count": "신고 건수"},
                color_discrete_sequence=["#4b8fe8"],
            )
            chart.update_layout(
                height=320,
                margin=dict(l=10, r=10, t=25, b=10),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                bargap=0.78,
            )
            # 연도 하나만 있을 때 2013.974처럼 소수 눈금이 생기지 않도록
            # x축을 숫자가 아닌 범주형 연도로 고정한다.
            chart.update_xaxes(type="category")
            max_count = int(defect_by_year["complaint_count"].max())
            chart.update_yaxes(
                rangemode="tozero",
                range=[0, max(5, int(max_count * 1.2) + 1)],
                dtick=1 if max_count <= 10 else None,
                tickformat=",d",
            )
            chart.update_traces(width=0.36)
            st.plotly_chart(chart, width="stretch", config={"displayModeBar": False})
            if year != "전체 연식":
                st.info(f"현재 선택: {year}년형 · 신고 {format_number(complaint_count)}건")

    with tab_variants:
        st.markdown('<div class="section-title">원본 데이터에 기록된 세부 차명</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">대표 차종 아래에 연결된 원본 표기를 확인할 수 있습니다.</div>', unsafe_allow_html=True)
        variants = read_query(VARIANTS_SQL, {"model_id": model_id})
        if variants.empty:
            st.info("세부 차명이 없습니다.")
        else:
            st.dataframe(variants[["variant_name"]].rename(columns={"variant_name": "원본 차명"}), width="stretch", hide_index=True)


def render_compare() -> None:
    """제조사·대표 차종·모델연도를 고른 차량을 비교한다."""
    st.markdown("## 차종 비교")
    st.markdown(
        "제조사와 대표 차종을 먼저 고른 뒤 모델연도까지 지정해서 비교합니다. "
        "판매량을 반영한 결함률은 아닙니다."
    )

    compare_count = int(
        st.number_input(
            "비교할 차량 수",
            min_value=2,
            max_value=5,
            value=2,
            step=1,
            help="2대부터 5대까지 비교할 수 있습니다.",
        )
    )

    selected_cars: list[dict[str, object]] = []
    for index in range(compare_count):
        st.markdown(f"### 비교 차량 {index + 1}")
        manufacturer_col, model_col, year_col = st.columns([1, 1.25, 1])

        with manufacturer_col:
            manufacturer = st.selectbox(
                "제조사",
                manufacturers["manufacturer_name"].tolist(),
                key=f"compare_manufacturer_{index}",
            )
        manufacturer_id = int(
            manufacturers.loc[
                manufacturers["manufacturer_name"] == manufacturer,
                "manufacturer_id",
            ].iloc[0]
        )
        models = read_query(MODELS_SQL, {"manufacturer_id": manufacturer_id})

        with model_col:
            if models.empty:
                st.warning("차종 없음")
                continue
            model_labels = models["model_name"].tolist()
            model_label = st.selectbox(
                "대표 차종",
                model_labels,
                key=f"compare_model_{index}",
            )
        model_row = models.loc[models["model_name"] == model_label].iloc[0]
        model_id = int(model_row["model_id"])

        model_years = read_query(YEARS_SQL, {"model_id": model_id})["model_year"].tolist()
        year_options: list[str | int] = ["전체 연식"] + [int(year) for year in model_years]
        with year_col:
            year = st.selectbox(
                "모델연도",
                year_options,
                key=f"compare_year_{index}",
            )

        selected_cars.append(
            {
                "manufacturer": manufacturer,
                "model_id": model_id,
                "model_name": model_label,
                "model_year": year,
            }
        )

    st.markdown(
        "<div class='notice'>모델연도는 소유자 신고 건수에 적용됩니다. 공식 리콜은 생산기간 기준이라 선택한 모델연도로 억지로 나누지 않고 차종 전체 리콜을 보여줍니다.</div>",
        unsafe_allow_html=True,
    )
    compare_clicked = st.button("선택한 차량 비교하기", type="primary", width="stretch")
    if not compare_clicked:
        st.info("각 차량의 조건을 고른 뒤 비교하기를 눌러 주세요.")
        return

    comparison_rows: list[dict[str, object]] = []
    for car in selected_cars:
        model_id = int(car["model_id"])
        overview = read_query(OVERVIEW_SQL, {"model_id": model_id})
        if overview.empty:
            continue
        summary = overview.iloc[0]
        model_year = car["model_year"]
        if model_year == "전체 연식":
            complaint_count = int(summary["complaint_count"])
        else:
            complaint_result = read_query(
                DEFECT_COUNT_BY_YEAR_SQL,
                {"model_id": model_id, "model_year": int(model_year)},
            )
            complaint_count = int(complaint_result.iloc[0]["complaint_count"])
        year_label = "전체" if model_year == "전체 연식" else f"{model_year}년형"
        comparison_rows.append(
            {
                "model_id": model_id,
                "display_name": f"{car['manufacturer']} · {car['model_name']} ({year_label})",
                "manufacturer_name": car["manufacturer"],
                "model_name": car["model_name"],
                "model_year": year_label,
                "complaint_count": complaint_count,
                "recall_record_count": int(summary["recall_record_count"]),
                "affected_count_sum": int(summary["affected_count_sum"]),
            }
        )

    comparison = pd.DataFrame(comparison_rows)
    if comparison.empty:
        st.warning("선택한 조건으로 비교할 데이터를 찾지 못했습니다.")
        return

    chart_data = comparison.melt(
        id_vars=["display_name"],
        value_vars=["complaint_count", "recall_record_count"],
        var_name="지표",
        value_name="건수",
    )
    chart_data["지표"] = chart_data["지표"].map({"complaint_count": "소유자 신고", "recall_record_count": "공식 리콜 기록"})
    # 긴 제조사·차종명은 축에서 짧게 보여주고, 전체 이름은 마우스를 올렸을 때 표시한다.
    chart_data["chart_label"] = chart_data["display_name"].map(
        lambda value: value if len(str(value)) <= 22 else f"{str(value)[:21]}…"
    )
    chart = px.bar(
        chart_data,
        x="chart_label",
        y="건수",
        color="지표",
        barmode="group",
        hover_name="display_name",
        labels={"chart_label": "선택 차량", "건수": "건수", "지표": ""},
        color_discrete_map={"소유자 신고": "#4b8fe8", "공식 리콜 기록": "#f0a15b"},
    )
    chart.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=25, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.35,
    )
    chart.update_xaxes(
        type="category",
        tickangle=0,
        automargin=True,
        tickfont=dict(size=11),
    )
    chart.update_yaxes(rangemode="tozero", tickformat=",d")
    chart.update_traces(width=0.32)
    st.plotly_chart(chart, width="stretch", config={"displayModeBar": False})
    st.dataframe(
        comparison.rename(
            columns={
                "manufacturer_name": "제조사", "model_name": "대표 차종", "model_year": "모델연도",
                "complaint_count": "소유자 신고수", "recall_record_count": "공식 리콜 기록",
                "affected_count_sum": "리콜 대상 대수 합계",
            }
        ).drop(columns=["model_id"]),
        width="stretch",
        hide_index=True,
    )


def render_help() -> None:
    """데이터 기준과 FAQ를 설명한다."""
    st.markdown("## 도움말 · 데이터 안내")
    st.markdown("조회 결과를 어떻게 읽어야 하는지 간단히 정리했습니다.")
    st.markdown("### 자주 묻는 질문")
    with st.expander("공식 리콜과 소유자 결함 신고는 어떻게 다른가요?", expanded=True):
        st.write("공식 리콜은 제작사가 진행한 시정조치 기록입니다. 소유자 결함 신고는 차량 소유자가 접수한 기록으로, 신고만으로 결함 확정이나 리콜을 의미하지 않습니다.")
    with st.expander("리콜 대상 대수는 실제 차량 한 대의 조치 완료 여부인가요?"):
        st.write("아닙니다. 리콜 기록별 대상 대수를 합한 값입니다. 개별 차량의 조치 완료 여부는 차대번호를 이용해 제작사 또는 자동차리콜센터에서 확인해야 합니다.")
    with st.expander("모델연도와 리콜 생산기간은 왜 따로 보여주나요?"):
        st.write("신고 데이터의 모델연도와 리콜 데이터의 생산기간은 기록 기준이 다릅니다. 따라서 임의로 연도끼리 연결하지 않고 각각의 원본 기준을 그대로 표시합니다.")
    coverage = read_query("SELECT dataset_name, start_date, end_date, row_count, note FROM data_coverage ORDER BY coverage_id")
    if not coverage.empty:
        st.markdown("### 현재 데이터 범위")
        coverage = coverage.rename(columns={"dataset_name": "데이터", "start_date": "시작일", "end_date": "종료일", "row_count": "행 수", "note": "기준"})
        coverage["행 수"] = coverage["행 수"].map(format_number)
        st.dataframe(coverage, width="stretch", hide_index=True)
    st.markdown("### 공식 사이트 바로가기")
    st.markdown(
        "리콜 대상 여부와 개별 차량의 조치 완료 여부는 아래 공식 사이트에서 다시 확인할 수 있습니다.",
    )
    st.link_button("정부 자동차리콜센터 리콜 현황", GOVERNMENT_RECALL_URL, width="stretch")
    st.markdown("<div class='source-note'>데이터 출처: 한국교통안전공단 자동차리콜센터 제공 자료를 전처리한 프로젝트 DB</div>", unsafe_allow_html=True)


if menu == "리콜 조회":
    render_dashboard()
elif menu == "차종 비교":
    render_compare()
else:
    render_help()


