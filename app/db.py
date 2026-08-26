"""SQLite 연결, 조회 SQL, 요약 숫자."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from config import DB_PATH, DEFECT_CHART_START_YEAR

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

VISIBLE_DEFECT_YEARS_SQL = """
SELECT model_id, model_year
FROM defect_reports
WHERE model_year IS NOT NULL AND model_year >= :start_year
GROUP BY model_id, model_year
"""

# 이 대표 차종으로 접수된 신고의 모델연도가 전부 2015년 이전이면,
# 지금은 팔지 않는 옛 세대·구형 트림으로 본다.
OLD_MODEL_YEAR_ONLY_SQL = """
SELECT model_id
FROM defect_reports
WHERE model_year IS NOT NULL
GROUP BY model_id
HAVING MAX(model_year) < :start_year
"""


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


def load_manufacturers() -> pd.DataFrame:
    """제조사 목록을 읽는다. import 시점이 아니라 호출할 때만 DB를 연다."""
    return read_query(MANUFACTURERS_SQL)


@st.cache_data(ttl=300)
def load_visible_search_model_ids() -> tuple[int, ...]:
    """2015년 이후 신고와 판매량이 둘 다 없는 차종, 신고가 전부 2015년 이전인 옛 트림은 조회 목록에서 뺀다."""
    from sales import sales_lookup_for_model

    models = read_query(ALL_MODELS_SQL)
    years = read_query(VISIBLE_DEFECT_YEARS_SQL, {"start_year": DEFECT_CHART_START_YEAR})
    models_with_recent_reports = set(years["model_id"].astype(int))
    old_only = read_query(OLD_MODEL_YEAR_ONLY_SQL, {"start_year": DEFECT_CHART_START_YEAR})
    models_with_only_old_reports = set(old_only["model_id"].astype(int))

    visible: list[int] = []
    for row in models.itertuples(index=False):
        model_id = int(row.model_id)
        has_reports = model_id in models_with_recent_reports
        family, _sales_by_year = sales_lookup_for_model(str(row.model_name))
        # 판매량은 차종 패밀리 단위라, 신고가 전부 2015년 이전인 단종 트림까지
        # 지금 팔리는 차종의 판매량을 근거로 노출시키지 않는다.
        has_current_sales = family is not None and model_id not in models_with_only_old_reports
        if has_reports or has_current_sales:
            visible.append(model_id)
    return tuple(visible)


def load_search_manufacturers() -> pd.DataFrame:
    """조회 탭에 보여줄 제조사. 숨긴 차종만 있는 제조사는 빼 둔다."""
    manufacturers = load_manufacturers()
    visible_ids = set(load_visible_search_model_ids())
    models = read_query(ALL_MODELS_SQL)
    keep_names = set(models.loc[models["model_id"].isin(visible_ids), "manufacturer_name"])
    return manufacturers.loc[manufacturers["manufacturer_name"].isin(keep_names)].reset_index(drop=True)


def load_search_models(manufacturer_id: int) -> pd.DataFrame:
    """조회 탭에 보여줄 대표 차종."""
    models = read_query(MODELS_SQL, {"manufacturer_id": manufacturer_id})
    visible_ids = set(load_visible_search_model_ids())
    return models.loc[models["model_id"].isin(visible_ids)].reset_index(drop=True)


def format_number(value: object) -> str:
    """숫자를 화면용 천 단위 구분 문자열로 표시한다."""
    if value is None or pd.isna(value):
        return "0"
    return f"{int(value):,}"


def format_date(value: object) -> str:
    if value is None or pd.isna(value) or str(value) in {"", "None"}:
        return "-"
    return str(value).replace("-", ".")


def complaint_count_help(year: object) -> str:
    """신고 건수 카드에 붙는 설명을 연식 선택에 맞게 반환한다."""
    if year == "전체 연식":
        return "선택한 대표 차종의 모든 모델연도에 접수된 소비자 결함 신고 행의 누적 건수입니다."
    return f"선택한 {year}년형에 접수된 소비자 결함 신고 행의 수입니다."


def get_summary_metrics(model_id: int, year: object) -> tuple[str, int, int, int] | None:
    """조회·비교 팝업에 쓸 요약 숫자를 가져온다."""
    overview = read_query(OVERVIEW_SQL, {"model_id": model_id})
    if overview.empty:
        return None
    summary = overview.iloc[0]
    if year == "전체 연식":
        complaint_count = int(summary["complaint_count"])
        year_label = "누적 소비자 결함 신고수"
    else:
        year_count = read_query(
            DEFECT_COUNT_BY_YEAR_SQL,
            {"model_id": model_id, "model_year": int(year)},
        )
        complaint_count = int(year_count.iloc[0]["complaint_count"])
        year_label = f"{year}년형 신고"
    return (
        year_label,
        complaint_count,
        int(summary["recall_record_count"]),
        int(summary["affected_count_sum"]),
    )
