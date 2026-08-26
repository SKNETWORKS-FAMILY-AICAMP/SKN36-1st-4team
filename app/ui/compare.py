"""차종 비교 탭과 비교 차량 미리보기."""

from __future__ import annotations

import html

import pandas as pd
import plotly.express as px
import streamlit as st

from db import (
    MODELS_SQL,
    YEARS_SQL,
    complaint_count_help,
    format_number,
    get_summary_metrics,
    load_manufacturers,
    read_query,
)
from interest import add_interest_car, car_identity, car_tag_label, remove_interest_car
from ui.components import (
    preview_icon_svg,
    render_vehicle_visual_overlay,
    report_heading_html,
    report_table_html,
)


def dismiss_compare_preview() -> None:
    """비교 조회 팝업을 닫으면 다시 자동으로 열리지 않게 한다."""
    st.session_state.compare_preview = None


@st.dialog(
    "비교 차량 미리보기",
    width="small",
    dismissible=True,
    on_dismiss=dismiss_compare_preview,
)
def render_compare_preview_dialog() -> None:
    """비교할 차종의 사진과 안전 요약을 사진 중심 팝업으로 보여준다."""
    preview = st.session_state.get("compare_preview")
    if not preview:
        return

    manufacturer = str(preview["manufacturer"])
    model_name = str(preview["model_name"])
    year = preview["year"]
    metrics = get_summary_metrics(int(preview["model_id"]), year)
    is_registered = any(
        car_identity(car) == car_identity(preview)
        for car in st.session_state.get("interest_cars", [])
    )
    year_text = "전체 연식" if year == "전체 연식" else f"{year}년형"

    with st.container(key="compare-preview-dialog", gap="small"):
        render_vehicle_visual_overlay(
            manufacturer,
            model_name,
            year_text,
            "preview-vehicle-visual",
        )
        if metrics is None:
            st.warning("선택한 차종의 요약 정보를 찾지 못했습니다.")
        else:
            year_label, complaint_count, recall_count, affected_sum = metrics
            st.markdown(
                "<div class='preview-safety-callout'>"
                f"<span class='preview-safety-badge'>{preview_icon_svg('shield')}</span>"
                "<div><span class='preview-safety-title'>구매 전 안전 정보를 함께 살펴보세요</span>"
                "<span class='preview-safety-copy'>결함 신고는 리콜 확정 여부와 다를 수 있어요.</span></div>"
                "</div>"
                "<div class='preview-metrics'>"
                f"<div class='preview-metric' title='{html.escape(complaint_count_help(year), quote=True)}'>"
                f"<span class='preview-metric-icon'>{preview_icon_svg('report')}</span>"
                "<span class='preview-metric-label'>소비자 결함 신고</span>"
                f"<span class='preview-metric-context'>{html.escape(year_label)}</span>"
                f"<strong class='preview-metric-value'>{html.escape(format_number(complaint_count))}건</strong>"
                "</div>"
                "<div class='preview-metric'>"
                f"<span class='preview-metric-icon'>{preview_icon_svg('bell')}</span>"
                "<span class='preview-metric-label'>공식 리콜 기록</span>"
                "<span class='preview-metric-context'>제조사 안전 조치</span>"
                f"<strong class='preview-metric-value'>{html.escape(format_number(recall_count))}건</strong>"
                "</div>"
                "<div class='preview-metric'>"
                f"<span class='preview-metric-icon'>{preview_icon_svg('people')}</span>"
                "<span class='preview-metric-label'>리콜 대상 대수</span>"
                "<span class='preview-metric-context'>공식 리콜 기준</span>"
                f"<strong class='preview-metric-value'>{html.escape(format_number(affected_sum))}대</strong>"
                "</div></div>",
                unsafe_allow_html=True,
            )
        button_key = "compare-register-button-added" if is_registered else "compare-register-button"
        button_label = "비교차량 등록됨" if is_registered else "비교차량 등록"
        with st.container(key=button_key):
            if st.button(
                button_label,
                key="add_compare_car",
                icon=":material/star:",
                width="stretch",
                disabled=is_registered,
            ):
                added, message = add_interest_car(preview)
                if added:
                    st.session_state.compare_preview = None
                    st.rerun()
                else:
                    st.warning(message)
        if is_registered:
            with st.container(key="compare-list-link"):
                if st.button(
                    "비교 목록 확인하기",
                    key="open_compare_list",
                    type="secondary",
                    width="stretch",
                ):
                    st.session_state.compare_preview = None
                    st.rerun()


def render_compare() -> None:
    """관심 차량 태그와 한 줄 조회로 차종을 비교한다."""
    st.markdown("## 차종 비교")
    st.markdown(
        "관심 차량을 태그로 모아 비교합니다. 아래에서 차종을 조회해 비교 대상을 추가할 수 있습니다. "
        "판매량을 반영한 결함률은 아닙니다."
    )

    saved = st.session_state.get("interest_cars", [])
    st.markdown("<div class='search-panel-title'>관심 차량</div>", unsafe_allow_html=True)
    if saved:
        with st.container(key="compare-tag-list", horizontal=True, gap="small"):
            for car in saved:
                model_id = int(car["model_id"])
                year = car["year"]
                if st.button(
                    car_tag_label(car),
                    key=f"remove_interest_tag_{model_id}_{year}",
                    type="secondary",
                ):
                    remove_interest_car(model_id, year)
                    st.rerun()
    else:
        st.caption("등록된 관심 차량이 없습니다. 아래에서 차종을 조회해 추가할 수 있습니다.")

    manufacturers = load_manufacturers()
    if manufacturers.empty:
        st.warning("등록된 제조사 데이터가 없습니다.")
        return

    with st.container(border=True, gap="small"):
        st.markdown("<div class='search-panel-title'>비교 차량 추가 하기</div>", unsafe_allow_html=True)
        manufacturer_col, model_col, year_col, button_col = st.columns(
            [1.1, 1.35, 1, 0.8],
            vertical_alignment="bottom",
            gap="small",
        )
        manufacturer_options = manufacturers["manufacturer_name"].tolist()
        with manufacturer_col:
            if st.session_state.get("compare_lookup_manufacturer") not in manufacturer_options:
                st.session_state.compare_lookup_manufacturer = manufacturer_options[0]
            manufacturer = st.selectbox(
                "제조사",
                manufacturer_options,
                key="compare_lookup_manufacturer",
            )
        manufacturer_id = int(
            manufacturers.loc[
                manufacturers["manufacturer_name"] == manufacturer,
                "manufacturer_id",
            ].iloc[0]
        )
        models = read_query(MODELS_SQL, {"manufacturer_id": manufacturer_id})
        lookup_ready = not models.empty
        with model_col:
            if not lookup_ready:
                st.warning("이 제조사에 등록된 대표 차종이 없습니다.")
                model_label = ""
                model_id = 0
            else:
                model_labels = models["model_name"].tolist()
                if st.session_state.get("compare_lookup_model") not in model_labels:
                    st.session_state.compare_lookup_model = model_labels[0]
                model_label = st.selectbox(
                    "대표 차종",
                    model_labels,
                    key="compare_lookup_model",
                )
                model_row = models.loc[models["model_name"] == model_label].iloc[0]
                model_id = int(model_row["model_id"])
        year_options: list[str | int] = ["전체 연식"]
        if lookup_ready:
            model_years = read_query(YEARS_SQL, {"model_id": model_id})["model_year"].tolist()
            year_options = ["전체 연식"] + [int(year) for year in model_years]
        with year_col:
            if st.session_state.get("compare_lookup_year") not in year_options:
                st.session_state.compare_lookup_year = year_options[0]
            year = st.selectbox(
                "모델 연도",
                year_options,
                key="compare_lookup_year",
            )
        with button_col:
            if st.button(
                "조회",
                type="primary",
                width="stretch",
                key="compare_lookup_button",
                disabled=not lookup_ready,
            ):
                st.session_state.compare_preview = {
                    "manufacturer": manufacturer,
                    "model_id": model_id,
                    "model_name": model_label,
                    "year": year,
                }
                st.rerun()

    if st.session_state.get("compare_preview") and not st.session_state.get("public_ad_open"):
        render_compare_preview_dialog()

    st.markdown(
        "<div class='notice'>모델연도는 소유자 신고 건수에 적용됩니다. "
        "공식 리콜은 생산기간 기준이라 선택한 모델연도로 억지로 나누지 않고 차종 전체 리콜을 보여줍니다.</div>",
        unsafe_allow_html=True,
    )
    if len(saved) < 2:
        st.info("비교하려면 관심 차량을 2대 이상 등록해 주세요.")
        return

    comparison_rows: list[dict[str, object]] = []
    for car in saved:
        model_id = int(car["model_id"])
        metrics = get_summary_metrics(model_id, car["year"])
        if metrics is None:
            continue
        _year_label, complaint_count, recall_count, affected_sum = metrics
        year_text = "전체" if car["year"] == "전체 연식" else f"{car['year']}년형"
        comparison_rows.append(
            {
                "model_id": model_id,
                "display_name": f"{car['manufacturer']} · {car['model_name']} ({year_text})",
                "manufacturer_name": car["manufacturer"],
                "model_name": car["model_name"],
                "model_year": year_text,
                "complaint_count": complaint_count,
                "recall_record_count": recall_count,
                "affected_count_sum": affected_sum,
            }
        )

    comparison = pd.DataFrame(comparison_rows)
    if comparison.empty:
        st.warning("선택한 조건으로 비교할 데이터를 찾지 못했습니다.")
        return

    chart_data = comparison.melt(
        id_vars=["display_name", "model_name"],
        value_vars=["complaint_count", "recall_record_count"],
        var_name="지표",
        value_name="건수",
    )
    chart_data["지표"] = chart_data["지표"].map({"complaint_count": "소유자 신고", "recall_record_count": "공식 리콜 기록"})
    chart_data["chart_label"] = chart_data["model_name"].map(
        lambda value: value if len(str(value)) <= 14 else f"{str(value)[:13]}…"
    )
    chart = px.bar(
        chart_data,
        x="chart_label",
        y="건수",
        color="지표",
        barmode="group",
        hover_name="display_name",
        labels={"chart_label": "선택 차량", "건수": "건수", "지표": ""},
        color_discrete_map={"소유자 신고": "#245ccb", "공식 리콜 기록": "#e98666"},
    )
    chart.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.35,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    chart.update_xaxes(
        type="category",
        tickangle=0,
        automargin=True,
        tickfont=dict(size=11),
    )
    chart.update_yaxes(rangemode="tozero", tickformat=",d")
    chart.update_traces(width=0.32)

    used_names: set[str] = set()
    transposed_columns: dict[str, list[str]] = {}
    for _, row in comparison.iterrows():
        column_name = str(row["model_name"])
        if column_name in used_names:
            column_name = f"{row['manufacturer_name']} {row['model_name']}"
        suffix = 2
        unique_name = column_name
        while unique_name in used_names:
            unique_name = f"{column_name} {suffix}"
            suffix += 1
        used_names.add(unique_name)
        transposed_columns[unique_name] = [
            str(row["manufacturer_name"]),
            str(row["model_name"]),
            str(row["model_year"]),
            format_number(row["complaint_count"]),
            f"{format_number(row['recall_record_count'])}건",
            f"{format_number(row['affected_count_sum'])}대",
        ]
    comparison_table = pd.DataFrame(
        transposed_columns,
        index=["제조사", "대표 차종", "모델연도", "소유자 신고수", "공식 리콜 기록", "리콜 대상 대수 합계"],
    ).rename_axis("항목").reset_index()

    st.markdown(
        "<div class='comparison-report-intro'>"
        "동일한 기준으로 수치를 비교합니다. 소유자 신고 건수는 결함 확정이나 판매량을 반영한 비율이 아닙니다."
        "</div>",
        unsafe_allow_html=True,
    )
    table_col, chart_col = st.columns([1.08, 0.92], gap="medium")
    with table_col:
        with st.container(border=True, key="compare-table-report"):
            st.markdown(
                report_heading_html(
                    "비교 안전 요약",
                    "선택한 차량의 신고·리콜 정보를 같은 기준으로 비교합니다.",
                    "report",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                report_table_html(comparison_table, "comparison-report-table"),
                unsafe_allow_html=True,
            )

    with chart_col:
        with st.container(border=True, key="compare-chart-report"):
            st.markdown(
                report_heading_html(
                    "신고·리콜 비교 그래프",
                    "차종별 신고 기록과 공식 리콜 기록의 건수를 함께 확인합니다.",
                    "report",
                    tone="coral",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='report-notice'><span class='report-notice-icon'>!</span><span>"
                "두 지표는 성격이 다릅니다. 신고 건수만으로 특정 차량의 결함이나 리콜 여부를 판단하지 마세요."
                "</span></div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(chart, width="stretch", config={"displayModeBar": False})
