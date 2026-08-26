"""조회·비교 화면에서 재사용하는 카드, 표, 차량 사진 UI."""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from config import (
    GOVERNMENT_RECALL_URL,
    MANUFACTURER_ICON_FILES,
    MANUFACTURER_OFFICIAL_URLS,
    MANUFACTURER_SHORT_NAMES,
    USED_CAR_MARKET_LINKS,
)
from images import brand_icon_html, find_car_image, image_file_to_data_uri


def preview_icon_svg(icon_name: str) -> str:
    """비교 차량 미리보기의 안내·지표용 선형 아이콘을 반환한다."""
    paths = {
        "shield": (
            '<path d="M12 2.5 21 5.6v7c0 5.3-3.4 9.7-9 12.1-5.6-2.4-9-6.8-9-12.1v-7L12 2.5Z"/>'
            '<path d="m8.2 13 2.4 2.4 5.3-5.5"/>'
        ),
        "report": (
            '<path d="M7 3.5h8.5L20 8v12.5H7z"/><path d="M15.5 3.5V8H20"/>'
            '<path d="M10 11h5.5M10 14.5h4"/><circle cx="17.8" cy="17.8" r="3.2"/><path d="m20.1 20.1 1.9 1.9"/>'
        ),
        "bell": (
            '<path d="M6 17.5h12l-1.5-2.2v-4.7a4.5 4.5 0 0 0-9 0v4.7z"/>'
            '<path d="M10 21h4M12 3v1.4"/>'
        ),
        "people": (
            '<circle cx="12" cy="8.2" r="3.2"/><path d="M5.4 21v-1.6a5.5 5.5 0 0 1 5.5-5.5h2.2a5.5 5.5 0 0 1 5.5 5.5V21"/>'
            '<path d="M4.4 8.8a2.6 2.6 0 0 1 2-2.5M19.6 8.8a2.6 2.6 0 0 0-2-2.5M2.5 20v-1.2a4.2 4.2 0 0 1 2.7-3.9M21.5 20v-1.2a4.2 4.2 0 0 0-2.7-3.9"/>'
        ),
    }
    return (
        '<svg viewBox="-1 -1 26 26" aria-hidden="true" focusable="false">'
        f"{paths[icon_name]}</svg>"
    )


def link_card_html(title: str, description: str, url: str | None, icon_html: str) -> str:
    """중고차·공식 사이트 이동용 카드 HTML을 만든다."""
    inner = (
        f"{icon_html}<span class='market-card-copy'>"
        f"<strong>{html.escape(title)}</strong>"
        f"<small>{html.escape(description)}</small></span>"
    )
    if url:
        return (
            f"<a class='market-card' href='{html.escape(url, quote=True)}' "
            "target='_blank' rel='noopener noreferrer'>"
            f"{inner}</a>"
        )
    return f"<span class='market-card market-card-disabled'>{inner}</span>"


def manufacturer_site_label(manufacturer: str) -> str:
    """버튼에 넣을 짧은 제조사 공식 사이트 이름을 만든다."""
    short_name = MANUFACTURER_SHORT_NAMES.get(manufacturer, manufacturer)
    return f"{short_name} 공식 사이트"


def render_official_links(manufacturer: str) -> None:
    """조회한 차량을 공식 사이트에서 다시 확인할 수 있는 카드형 링크를 표시한다."""
    recall_card = link_card_html(
        "리콜센터",
        "정부 자동차리콜센터",
        GOVERNMENT_RECALL_URL,
        brand_icon_html("recall_center.png", "🚨"),
    )
    manufacturer_url = MANUFACTURER_OFFICIAL_URLS.get(manufacturer)
    manufacturer_icon = brand_icon_html(
        MANUFACTURER_ICON_FILES.get(manufacturer, ""),
        manufacturer[:1] if manufacturer else "M",
    )
    manufacturer_card = link_card_html(
        manufacturer_site_label(manufacturer),
        "제조사 홈페이지",
        manufacturer_url,
        manufacturer_icon,
    )
    st.markdown(
        "<div class='official-grid'>" + recall_card + manufacturer_card + "</div>",
        unsafe_allow_html=True,
    )


def render_purchase_links() -> None:
    """중고차 구매 사이트를 카드형 외부 링크로 표시한다."""
    st.markdown("<div class='market-title'>중고차 매물 이어서 보기</div>", unsafe_allow_html=True)
    cards = [
        link_card_html(name, description, url, brand_icon_html(icon_path, name[:1]))
        for icon_path, name, description, url in USED_CAR_MARKET_LINKS
    ]
    st.markdown("<div class='market-grid'>" + "".join(cards) + "</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='source-note'>외부 중고차 매물 사이트로 이동합니다. "
        "매물 정보와 거래 조건은 각 사이트에서 다시 확인하세요.</div>",
        unsafe_allow_html=True,
    )


def report_heading_html(title: str, description: str, icon_name: str, tone: str = "blue") -> str:
    """조회·비교 화면에서 재사용하는 리포트형 섹션 제목을 만든다."""
    tone_class = " report-heading-report" if tone == "coral" else ""
    return (
        f"<div class='report-heading{tone_class}'>"
        f"<span class='report-heading-icon'>{preview_icon_svg(icon_name)}</span>"
        "<div>"
        f"<h3>{html.escape(title)}</h3>"
        f"<p>{html.escape(description)}</p>"
        "</div></div>"
    )


def report_table_html(data: pd.DataFrame, table_class: str) -> str:
    """가로 스크롤 없이 셀 너비를 배분하는 읽기 전용 리포트 표를 만든다."""
    headers = "".join(f"<th scope='col'>{html.escape(str(column))}</th>" for column in data.columns)
    rows: list[str] = []
    for _, row in data.iterrows():
        cells = "".join(f"<td>{html.escape(str(value))}</td>" for value in row)
        rows.append(f"<tr>{cells}</tr>")
    return (
        f"<div class='report-table-wrap'><table class='report-table {html.escape(table_class, quote=True)}'>"
        f"<thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
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


def render_vehicle_visual_overlay(
    manufacturer: str,
    model: str,
    year_text: str,
    variant: str,
) -> None:
    """차량 사진 하단에 제조사·차종 정보를 겹쳐 표시한다."""
    image_path = find_car_image(manufacturer, model)
    if image_path:
        image_uri = image_file_to_data_uri(image_path)
        if image_uri:
            st.markdown(
                f"<div class='vehicle-visual {html.escape(variant, quote=True)}' "
                f"style=\"background-image:url('{image_uri}');\">"
                "<div class='vehicle-visual-overlay'>"
                f"<span class='vehicle-visual-brand'>{html.escape(manufacturer)}</span>"
                f"<span class='vehicle-visual-title'>{html.escape(model)} · {html.escape(year_text)}</span>"
                "</div></div>",
                unsafe_allow_html=True,
            )
            return
    render_car_visual(manufacturer, model)
