"""차량 조회 조건과 결과 4분할 화면."""

from __future__ import annotations

import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from config import DEFECT_CHART_START_YEAR
from db import (
    DEFECT_BY_YEAR_SQL,
    RECALLS_SQL,
    YEARS_SQL,
    complaint_count_help,
    format_date,
    format_number,
    get_summary_metrics,
    load_search_manufacturers,
    load_search_models,
    read_query,
)
from interest import add_interest_car, car_identity
from sales import sales_lookup_for_model
from ui.components import (
    preview_icon_svg,
    render_official_links,
    render_purchase_links,
    render_vehicle_visual_overlay,
    report_heading_html,
    report_table_html,
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


def render_recall_search() -> None:
    """차량 조회 페이지 본문에 제조사·차종·연식 조건을 표시한다."""
    manufacturers = load_search_manufacturers()
    if manufacturers.empty:
        st.warning("조회할 수 있는 제조사가 없습니다.")
        return

    manufacturer_names = manufacturers["manufacturer_name"].tolist()
    previous = st.session_state.get("search_state") or {}
    previous_manufacturer = previous.get("manufacturer")
    manufacturer_index = (
        manufacturer_names.index(previous_manufacturer)
        if previous_manufacturer in manufacturer_names
        else 0
    )

    with st.container(border=True, gap="small"):
        st.markdown("<div class='search-panel-title'>차량 검색 조건</div>", unsafe_allow_html=True)
        manufacturer_col, model_col, year_col, button_col = st.columns(
            [1.1, 1.35, 1, 0.8],
            vertical_alignment="bottom",
            gap="small",
        )
        with manufacturer_col:
            selected_manufacturer = st.selectbox(
                "제조사",
                manufacturer_names,
                index=manufacturer_index,
                key="recall_manufacturer",
            )

        manufacturer_row = manufacturers.loc[
            manufacturers["manufacturer_name"] == selected_manufacturer
        ]
        if manufacturer_row.empty:
            st.warning("선택한 제조사 정보를 찾지 못했습니다.")
            return
        manufacturer_id = int(manufacturer_row.iloc[0]["manufacturer_id"])
        models = load_search_models(manufacturer_id)
        if models.empty:
            st.warning("이 제조사에서 조회할 수 있는 대표 차종이 없습니다.")
            return

        model_labels = models.apply(
            lambda row: f"{row['model_name']}  ·  {row['vehicle_type'] or '차종 미분류'}", axis=1
        ).tolist()
        previous_model_id = previous.get("model_id")
        model_index = 0
        model_ids = models["model_id"].tolist()
        if previous_manufacturer == selected_manufacturer and previous_model_id in model_ids:
            model_index = model_ids.index(previous_model_id)

        with model_col:
            selected_model_label = st.selectbox(
                "대표 차종",
                model_labels,
                index=model_index,
                key="recall_model",
            )
        selected_model_index = model_labels.index(selected_model_label)
        selected_model_id = int(models.iloc[selected_model_index]["model_id"])
        selected_model_name = str(models.iloc[selected_model_index]["model_name"])

        years_df = read_query(YEARS_SQL, {"model_id": selected_model_id})
        years = [
            year
            for year in years_df["model_year"].dropna().astype(int).tolist()
            if year >= DEFECT_CHART_START_YEAR
        ]
        year_options: list[str | int] = ["전체 연식"] + years
        previous_year = previous.get("year") if previous_manufacturer == selected_manufacturer else None
        year_index = year_options.index(previous_year) if previous_year in year_options else 0
        with year_col:
            selected_year = st.selectbox(
                "모델 연도",
                year_options,
                index=year_index,
                key="recall_year",
            )

        with button_col:
            if st.button("조회하기", type="primary", width="stretch", key="recall_search_button"):
                st.session_state.search_state = {
                    "manufacturer": selected_manufacturer,
                    "model_id": selected_model_id,
                    "model_name": selected_model_name,
                    "year": selected_year,
                }
                st.rerun()

    if not st.session_state.get("search_state"):
        st.markdown(
            "<div class='source-note'>공식 리콜과 소유자 결함신고를 분리해서 보여드립니다. "
            "신고 건수는 리콜 확정 건수가 아닙니다.</div>",
            unsafe_allow_html=True,
        )


def render_recall_history(model_id: int) -> None:
    """공식 리콜 이력 표와 리콜 사유 펼쳐보기를 표시한다."""
    st.markdown(
        report_heading_html(
            "공식 리콜 이력",
            "생산기간, 리콜 개시일, 대상 대수와 리콜 사유를 확인합니다.",
            "report",
        ),
        unsafe_allow_html=True,
    )
    recalls = read_query(RECALLS_SQL, {"model_id": model_id})
    if recalls.empty:
        st.info("등록된 공식 리콜 기록이 없습니다.")
        return

    display_recalls = recalls.copy()
    display_recalls["생산기간"] = display_recalls.apply(
        lambda row: f"{format_date(row['production_start_date'])} ~ {format_date(row['production_end_date'])}",
        axis=1,
    )
    display_recalls["리콜 개시일"] = display_recalls["recall_start_date"].map(format_date)
    display_recalls["대상 대수"] = display_recalls["affected_count"].map(lambda x: f"{format_number(x)}대")
    recall_table = display_recalls[["raw_model_name", "생산기간", "리콜 개시일", "대상 대수"]].rename(
        columns={"raw_model_name": "원본 차명"}
    )
    st.markdown(report_table_html(recall_table, "recall-report-table"), unsafe_allow_html=True)
    for _, recall in recalls.iterrows():
        title = f"{format_date(recall['recall_start_date'])} · {recall['raw_model_name']}"
        with st.expander(title):
            st.write(recall["recall_reason"] or "리콜 사유가 입력되지 않았습니다.")
            st.caption(
                f"생산기간: {format_date(recall['production_start_date'])} ~ {format_date(recall['production_end_date'])}  |  "
                f"대상 대수: {format_number(recall['affected_count'])}대"
            )


COMPLAINT_BAR_COLOR = "#245ccb"
SALES_BAR_COLOR = "#2a9d8f"


def _sales_hover_label(value: object) -> str:
    if value is None or pd.isna(value):
        return "데이터 없음"
    return f"{int(value):,}대"


def render_defect_reports(model_id: int, model_name: str, year: object, complaint_count: int) -> None:
    """소유자 결함 신고 안내와 연식별 신고·판매량 막대그래프를 표시한다."""
    st.markdown(
        report_heading_html(
            "소유자 결함 신고",
            "2015년형부터 연식별 신고와 같은 해 판매량을 확인합니다.",
            "report",
            tone="coral",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='report-notice'><span class='report-notice-icon'>!</span><span>"
        "신고는 <b>건</b>, 판매량은 <b>대</b>라 단위가 다릅니다. "
        "위·아래 막대 높이를 서로 비교한 결함률이 아니며, 리콜 확정과도 다를 수 있습니다."
        "</span></div>",
        unsafe_allow_html=True,
    )
    defect_by_year = read_query(DEFECT_BY_YEAR_SQL, {"model_id": model_id})
    if defect_by_year.empty:
        st.info("모델연도가 있는 결함 신고 기록이 없습니다.")
        return

    sales_family, sales_by_year = sales_lookup_for_model(model_name)
    chart_data = defect_by_year.copy()
    chart_data["model_year"] = chart_data["model_year"].astype(int)
    chart_data = chart_data.loc[chart_data["model_year"] >= DEFECT_CHART_START_YEAR]
    if chart_data.empty:
        st.info(f"{DEFECT_CHART_START_YEAR}년형 이후 결함 신고 기록이 없습니다.")
        return
    chart_data = chart_data.sort_values("model_year")
    chart_data["year_label"] = chart_data["model_year"].map(lambda value: f"{int(value) % 100:02d}")
    # 숫자로만 된 범주(예: "06")는 Plotly 주석에서 연속형 좌표로 해석될 수 있다.
    # 내부 키를 문자 범주로 분리하고, 눈에는 기존처럼 두 자리 연도만 표시한다.
    chart_data["year_axis"] = chart_data["model_year"].map(lambda value: f"year-{int(value)}")
    chart_data["sales_volume"] = chart_data["model_year"].map(
        lambda value: sales_by_year.get(int(value))
    )
    chart_data["sales_hover"] = chart_data["sales_volume"].map(_sales_hover_label)
    sales_rows = chart_data.dropna(subset=["sales_volume"])
    has_sales_bars = not sales_rows.empty
    year_axes = chart_data["year_axis"].tolist()
    year_labels = chart_data["year_label"].tolist()
    max_count = int(chart_data["complaint_count"].max())

    axis_font = dict(color="#53627b", family="Pretendard, Noto Sans KR, sans-serif")
    category_axis = dict(
        type="category",
        categoryorder="array",
        categoryarray=year_axes,
        tickmode="array",
        tickvals=year_axes,
        ticktext=year_labels,
        tickangle=0,
        fixedrange=True,
        title=None,
        showgrid=False,
    )
    complaint_bar = go.Bar(
        x=chart_data["year_axis"],
        y=chart_data["complaint_count"],
        name="신고 건수",
        marker_color=COMPLAINT_BAR_COLOR,
        marker_line_width=0,
        width=0.55,
        customdata=chart_data[["year_label", "sales_hover"]],
        hovertemplate="연식 %{customdata[0]}<br>신고 %{y:,}건<br>판매 %{customdata[1]}<extra></extra>",
    )

    if has_sales_bars:
        max_sales = int(sales_rows["sales_volume"].max())
        chart = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.12,
            row_heights=[0.58, 0.42],
        )
        chart.add_trace(complaint_bar, row=1, col=1)
        chart.add_trace(
            go.Bar(
                x=sales_rows["year_axis"],
                y=sales_rows["sales_volume"],
                name="판매량",
                marker_color=SALES_BAR_COLOR,
                marker_line_width=0,
                width=0.55,
                customdata=sales_rows[["year_label", "complaint_count"]],
                hovertemplate="연식 %{customdata[0]}<br>판매 %{y:,}대<br>신고 %{customdata[1]:,}건<extra></extra>",
            ),
            row=2,
            col=1,
        )
        chart.update_layout(
            height=420,
            autosize=True,
            margin=dict(l=8, r=12, t=28, b=8),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            bargap=0.42,
            font=axis_font,
            showlegend=False,
        )
        chart.update_xaxes(**category_axis, showticklabels=False, row=1, col=1)
        chart.update_xaxes(**category_axis, row=2, col=1)
        chart.update_yaxes(
            title=dict(text="신고 건수 (건)", font=dict(size=11)),
            rangemode="tozero",
            range=[0, max(5, int(max_count * 1.28) + 1)],
            dtick=1 if max_count <= 10 else None,
            tickformat=",d",
            fixedrange=True,
            gridcolor="#e7edf7",
            zeroline=False,
            row=1,
            col=1,
        )
        chart.update_yaxes(
            title=dict(text="판매량 (대)", font=dict(size=11)),
            rangemode="tozero",
            range=[0, max(10, int(max_sales * 1.18))],
            tickformat=",d",
            fixedrange=True,
            gridcolor="#e7edf7",
            zeroline=False,
            row=2,
            col=1,
        )
    else:
        chart = go.Figure(data=[complaint_bar])
        chart.update_layout(
            height=320,
            autosize=True,
            margin=dict(l=12, r=12, t=24, b=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            bargap=0.42,
            font=axis_font,
            showlegend=False,
            xaxis=category_axis,
            yaxis=dict(
                title=dict(text="신고 건수 (건)", font=dict(size=11)),
                rangemode="tozero",
                range=[0, max(5, int(max_count * 1.2) + 1)],
                dtick=1 if max_count <= 10 else None,
                tickformat=",d",
                fixedrange=True,
                gridcolor="#e7edf7",
                zeroline=False,
            ),
        )

    peak = chart_data.loc[chart_data["complaint_count"].idxmax()]
    chart.add_annotation(
        x=peak["year_axis"],
        y=int(peak["complaint_count"]),
        text=f"최고 {format_number(peak['complaint_count'])}건<br>({int(peak['model_year'])}년형)",
        showarrow=True,
        arrowhead=0,
        arrowcolor="#df8e68",
        ax=42,
        ay=-34,
        bgcolor="#fff8f3",
        bordercolor="#f0b79f",
        borderwidth=1,
        borderpad=5,
        font=dict(color="#c7633d", size=11),
        align="left",
        xref="x",
        yref="y",
    )
    st.plotly_chart(chart, width="stretch", config={"displayModeBar": False, "scrollZoom": False})
    if has_sales_bars:
        legend_html = (
            "<div class='chart-legend chart-legend-dual'>"
            "<span class='chart-legend-item'><span class='chart-legend-swatch'></span>위 · 신고 건수</span>"
            "<span class='chart-legend-item'><span class='chart-legend-swatch chart-legend-swatch-sales'></span>아래 · 판매량</span>"
            "</div>"
        )
    else:
        legend_html = (
            "<div class='chart-legend'><span class='chart-legend-swatch'></span><span>신고 건수</span></div>"
        )
    st.markdown(legend_html, unsafe_allow_html=True)
    if sales_family is None:
        st.caption("그래프는 2015년형부터 표시합니다. 이 차종의 판매량 데이터가 없어 신고 건수만 보여 드립니다.")
    elif len(sales_rows) < len(chart_data):
        st.caption("그래프는 2015년형부터 표시합니다. 판매량이 없는 연식은 아래 칸이 비어 있으며, 판매량은 차종 패밀리 기준입니다.")
    else:
        st.caption("그래프는 2015년형부터 표시합니다. 판매량은 트림이 아닌 차종 패밀리 기준입니다.")
    if year != "전체 연식":
        st.info(f"현재 선택: {year}년형 · 신고 {format_number(complaint_count)}건")


def render_dashboard() -> None:
    """선택한 차종의 요약·리콜·신고를 4분할로 표시한다."""
    search = st.session_state.get("search_state")
    if not search:
        return

    model_id = int(search["model_id"])
    manufacturer = str(search["manufacturer"])
    model_name = str(search["model_name"])
    year = search["year"]
    metrics = get_summary_metrics(model_id, year)
    if metrics is None:
        st.warning("선택한 차종의 요약 정보를 찾지 못했습니다.")
        return
    _year_label, complaint_count, recall_count, affected_sum = metrics

    is_registered = any(
        car_identity(car) == car_identity(search)
        for car in st.session_state.get("interest_cars", [])
    )
    year_text = "전체 연식" if year == "전체 연식" else f"{year}년형"

    st.markdown(
        f"<div class='result-header'>"
        f"<div class='result-title'><span class='result-title-icon'>{preview_icon_svg('shield')}</span>"
        f"{html.escape(model_name)} 리콜/결함 요약</div>"
        "<div class='result-emphasis'>"
        "공식 리콜과 소유자 결함신고를 분리해서 보여드립니다. "
        "신고 건수는 리콜 확정 건수가 아닙니다."
        "</div></div>",
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns(2, gap="medium")
    with top_left:
        with st.container(
            border=True,
            height="stretch",
            key="result-top-left",
            gap="small",
        ):
            render_vehicle_visual_overlay(
                manufacturer,
                model_name,
                year_text,
                "result-vehicle-visual",
            )
            button_key = "interest-register-button-added" if is_registered else "interest-register-button"
            button_label = "관심 차량 등록됨" if is_registered else "관심 차량 등록"
            with st.container(key=button_key):
                if st.button(
                    button_label,
                    key="add_interest_car",
                    icon=":material/star:",
                    width="stretch",
                    disabled=is_registered,
                ):
                    added, message = add_interest_car(search)
                    if added:
                        st.rerun()
                    else:
                        st.warning(message)

    with top_right:
        with st.container(
            border=True,
            height="stretch",
            key="result-top-right",
            gap="small",
        ):
            st.markdown(
                "<div class='result-safety-heading'>"
                f"{preview_icon_svg('shield')}<span>구매 전 안전 요약</span></div>"
                "<div class='result-metrics'>"
                f"<div class='result-metric' title='{html.escape(complaint_count_help(year), quote=True)}'>"
                f"<span class='result-metric-icon'>{preview_icon_svg('report')}</span>"
                "<span class='result-metric-label'>누적 소비자 결함 신고수</span>"
                f"<strong class='result-metric-value'><span class='result-metric-number'>{html.escape(format_number(complaint_count))}</span>"
                "<span class='result-metric-unit'>건</span></strong></div>"
                "<div class='result-metric'>"
                f"<span class='result-metric-icon'>{preview_icon_svg('bell')}</span>"
                "<span class='result-metric-label'>공식 리콜 기록</span>"
                f"<strong class='result-metric-value'><span class='result-metric-number'>{html.escape(format_number(recall_count))}</span>"
                "<span class='result-metric-unit'>건</span></strong></div>"
                "<div class='result-metric'>"
                f"<span class='result-metric-icon'>{preview_icon_svg('people')}</span>"
                "<span class='result-metric-label'>리콜 대상 대수 합계</span>"
                f"<strong class='result-metric-value'><span class='result-metric-number'>{html.escape(format_number(affected_sum))}</span>"
                "<span class='result-metric-unit'>대</span></strong></div>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='notice'>"
                "주의: 대상 대수는 리콜 기록별 합계입니다. "
                "개별 차량 조치 여부는 차대번호로 확인하세요."
                "</div>",
                unsafe_allow_html=True,
            )
            render_official_links(manufacturer)
            render_purchase_links()

    st.markdown(
        "<section class='result-interpretation' aria-label='조회 결과 해석 안내'>"
        "<div class='result-interpretation-intro'>"
        "<div class='result-interpretation-kicker'>"
        f"{preview_icon_svg('shield')}<span>조회 결과 안내</span></div>"
        "<div class='result-interpretation-title'>두 정보는 서로 다른 기준으로 확인하세요</div>"
        "<div class='result-interpretation-caution'>신고 건수만으로 리콜 또는 결함이 확정되지는 않습니다.</div>"
        "</div>"
        "<div class='result-interpretation-card'>"
        f"<span class='result-interpretation-icon'>{preview_icon_svg('bell')}</span>"
        "<div><strong>공식 리콜 이력</strong>"
        "<p>제조사 또는 관계 기관이 진행한 안전 조치 정보를 확인합니다.</p></div>"
        "</div>"
        "<div class='result-interpretation-card result-interpretation-card-report'>"
        f"<span class='result-interpretation-icon'>{preview_icon_svg('report')}</span>"
        "<div><strong>소유자 결함 신고</strong>"
        "<p>구매 전 참고할 수 있는 소비자 반복 신고 흐름을 살펴봅니다.</p></div>"
        "</div>"
        "</section>",
        unsafe_allow_html=True,
    )

    bottom_left, bottom_right = st.columns(2, gap="medium")
    with bottom_left:
        with st.container(border=True, key="recall-report-panel"):
            render_recall_history(model_id)
    with bottom_right:
        with st.container(border=True, key="defect-report-panel"):
            render_defect_reports(model_id, model_name, year, complaint_count)
