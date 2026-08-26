"""공통 헤더, 히어로, 관심 차량, 공익광고."""

from __future__ import annotations

import html
from datetime import date, datetime, time, timedelta

import streamlit as st

from config import AD_IMAGE_PATH, HERO_IMAGE_PATH, PUBLIC_AD_HIDE_COOKIE
from images import find_car_image, image_file_to_data_uri, shield_car_icon_html


def render_site_header() -> None:
    """앱 전체에서 공통으로 보이는 서비스 제목을 표시한다."""
    st.markdown(
        f"""
        <div class="top-brand">
          <div class="top-brand-mark">{shield_car_icon_html()}</div>
          <div>
            <div class="top-brand-title">자동차 리콜·결함 조회 서비스</div>
            <div class="top-brand-subtitle">중고차 구매 전 리콜 이력과 소유자 결함 신고를 확인하세요.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """현재 페이지의 공통 안내 배너를 표시한다."""
    hero_uri = image_file_to_data_uri(HERO_IMAGE_PATH)
    hero_style = (
        "background-image: linear-gradient(90deg, rgba(10, 27, 52, .98) 0%, "
        "rgba(10, 27, 52, .94) 22%, rgba(10, 27, 52, .72) 43%, "
        "rgba(10, 27, 52, .34) 61%, rgba(10, 27, 52, .08) 80%, transparent 100%), "
        f"url('{hero_uri}');"
        if hero_uri
        else "background: linear-gradient(115deg, #10213d 0%, #473d54 65%, #e98666 100%);"
    )
    st.markdown(
        f"""
        <div class="hero" style="{hero_style}">
          <div class="hero-inner">
            <div class="eyebrow">USED CAR SAFETY CHECK</div>
            <h1>중고차 구매 전, 리콜과 결함을 한눈에</h1>
            <p>가족과 함께할 차, 더 안심하고 골라보세요.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_interest_summary() -> None:
    """관심 차량 버튼을 탭과 같은 줄 오른쪽에 두고, 목록에 사진을 함께 보여준다."""
    saved = st.session_state.get("interest_cars", [])
    with st.popover(f"☆ 관심 차량 {len(saved)}/5", width="content"):
        if saved:
            cards = []
            for car in saved:
                image_path = find_car_image(str(car["manufacturer"]), str(car["model_name"]))
                if image_path:
                    uri = image_file_to_data_uri(image_path)
                    photo = (
                        f"<img class='interest-item-photo' src='{uri}' alt=''>"
                        if uri
                        else "<span class='interest-item-photo interest-item-photo-empty'>🚙</span>"
                    )
                else:
                    photo = "<span class='interest-item-photo interest-item-photo-empty'>🚙</span>"
                cards.append(
                    "<div class='interest-item'>"
                    "<div class='interest-item-text'>"
                    f"<strong>{html.escape(str(car['model_name']))}</strong>"
                    f"<small>{html.escape(str(car['manufacturer']))} · {html.escape(str(car['year']))}</small>"
                    f"</div>{photo}</div>"
                )
            st.markdown("".join(cards), unsafe_allow_html=True)
            if st.button("목록 비우기", key="clear_interest_cars", width="stretch"):
                st.session_state.interest_cars = []
                st.rerun()
        else:
            st.caption("차량 조회나 차종 비교에서 등록하면 비교 대상 태그로 표시됩니다.")


def dismiss_public_ad() -> None:
    """광고 모달의 우측 상단 X를 눌렀을 때 다시 자동으로 열리지 않게 한다."""
    st.session_state.public_ad_open = False
    if st.session_state.get("hide_public_ad_today"):
        st.session_state.persist_hide_public_ad = True


def persist_hide_public_ad_today() -> None:
    """오늘 하루 배너를 숨기도록 브라우저 쿠키를 남긴다."""
    today = date.today().isoformat()
    now = datetime.now()
    midnight = datetime.combine(now.date() + timedelta(days=1), time.min)
    max_age = max(60, int((midnight - now).total_seconds()))
    st.html(
        f'<script>document.cookie="{PUBLIC_AD_HIDE_COOKIE}={today};path=/;max-age={max_age};SameSite=Lax";</script>',
        unsafe_allow_javascript=True,
    )


@st.dialog(
    "차량 안전 안내",
    width="small",
    dismissible=True,
    on_dismiss=dismiss_public_ad,
)
def render_public_service_ad() -> None:
    """앱 시작 시 표시하는 자동차 리콜 공익광고 모달."""
    with st.container(key="public-ad-dialog"):
        if AD_IMAGE_PATH.exists():
            st.image(str(AD_IMAGE_PATH), width="stretch")
        else:
            st.warning("공익광고 이미지를 찾지 못했습니다.")
        st.checkbox("오늘 하루동안 보지않기", key="hide_public_ad_today")
