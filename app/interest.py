"""관심 차량 목록 추가·삭제·식별. 화면 위젯은 두지 않는다."""

from __future__ import annotations

import streamlit as st


def car_identity(car: dict[str, object]) -> tuple[int, str]:
    """관심·비교 목록에서 같은 차량인지 비교할 때 쓴다."""
    year = car.get("year", car.get("model_year"))
    return (int(car["model_id"]), str(year))


def car_tag_label(car: dict[str, object]) -> str:
    """비교 화면에 붙일 짧은 차종 태그 문구."""
    year = car.get("year", car.get("model_year"))
    year_label = "전체" if year == "전체 연식" else f"{year}년형"
    return f"{car['model_name']} · {year_label} ×"


def add_interest_car(search: dict[str, object]) -> tuple[bool, str]:
    """조회한 차량을 중복 없이 최대 5대까지 관심 목록에 추가한다."""
    saved = st.session_state.get("interest_cars", [])
    candidate_key = car_identity(search)
    existing_keys = {car_identity(car) for car in saved}
    if candidate_key in existing_keys:
        return False, "이미 등록한 차량입니다."
    if len(saved) >= 5:
        return False, "관심 차량은 최대 5대까지 등록할 수 있습니다."
    st.session_state.interest_cars = [*saved, dict(search)]
    return True, "관심 차량에 등록했습니다."


def remove_interest_car(model_id: int, year: object) -> None:
    """관심 차량 태그에서 해당 차종을 뺀다."""
    target = (int(model_id), str(year))
    st.session_state.interest_cars = [
        car for car in st.session_state.get("interest_cars", [])
        if car_identity(car) != target
    ]
