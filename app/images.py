"""차량 사진, 아이콘, data URI 변환."""

from __future__ import annotations

import base64
import html
import re
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st

from config import (
    ICON_DIR,
    ICON_MIME_TYPES,
    IMAGE_ALIAS_PATH,
    IMAGE_DIR,
    SERVICE_LOGO_PATH,
)


def clean_key(value: str) -> str:
    """사진 파일을 찾을 때 사용할 비교용 문자열."""
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"[^0-9a-z가-힣]+", "", text)


@st.cache_data(show_spinner=False)
def load_image_aliases() -> list[dict[str, str]]:
    """차종 변형이 대표 사진을 함께 쓰도록 매핑표를 읽는다."""
    if not IMAGE_ALIAS_PATH.exists():
        return []

    aliases = pd.read_csv(IMAGE_ALIAS_PATH, encoding="utf-8-sig").fillna("")
    required = {"manufacturer_name", "model_pattern", "image_filename"}
    if not required.issubset(aliases.columns):
        return []

    return [
        {
            "manufacturer_key": clean_key(row["manufacturer_name"]),
            "model_pattern_key": clean_key(row["model_pattern"]),
            "image_filename": str(row["image_filename"]).strip(),
        }
        for _, row in aliases.iterrows()
        if clean_key(row["manufacturer_name"])
        and clean_key(row["model_pattern"])
        and str(row["image_filename"]).strip()
    ]


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

    # 같은 기본 차종의 하이브리드·구동방식·트림은 대표 사진을 함께 사용한다.
    # 실제로 다른 차종인 경우에는 매핑 CSV에 행을 추가하지 않는다.
    for alias in load_image_aliases():
        if (
            alias["manufacturer_key"] == manufacturer_key
            and alias["model_pattern_key"] in model_key
        ):
            alias_path = IMAGE_DIR / alias["image_filename"]
            if alias_path.is_file() and alias_path.suffix.lower() in extensions:
                return alias_path
    return None


def resolve_icon_path(relative_stem: str) -> str:
    """png/svg 등 실제 존재하는 아이콘 파일 경로를 고른다."""
    if not relative_stem:
        return ""
    stem = Path(relative_stem)
    if stem.suffix.lower() in ICON_MIME_TYPES:
        return relative_stem if (ICON_DIR / relative_stem).is_file() else ""
    for extension in (".png", ".svg", ".webp", ".jpg", ".jpeg"):
        relative_path = f"{relative_stem}{extension}"
        if (ICON_DIR / relative_path).is_file():
            return relative_path
    return ""


def file_to_data_uri(relative_path: str) -> str:
    """아이콘 파일을 카드 HTML에 넣을 data URI로 바꾼다."""
    if not relative_path:
        return ""
    path = ICON_DIR / relative_path
    mime = ICON_MIME_TYPES.get(path.suffix.lower(), "")
    if not mime or not path.is_file():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def image_file_to_data_uri(path: Path) -> str:
    """차량 사진 파일을 목록 HTML에 넣을 data URI로 바꾼다."""
    mime = ICON_MIME_TYPES.get(path.suffix.lower(), "")
    if not mime or not path.is_file():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def shield_car_icon_html(class_name: str = "service-logo-icon") -> str:
    """공통 헤더에 표시할 서비스 로고를 반환한다."""
    logo_uri = image_file_to_data_uri(SERVICE_LOGO_PATH)
    if logo_uri:
        return (
            f"<img class='{html.escape(class_name, quote=True)}' src='{logo_uri}' "
            "alt='자동차 리콜·결함 조회 서비스 로고'>"
        )
    return ""


def brand_icon_html(relative_stem: str, fallback: str) -> str:
    """로고 파일이 있으면 이미지로, 없으면 글자 아이콘으로 표시한다."""
    uri = file_to_data_uri(resolve_icon_path(relative_stem))
    if uri:
        return (
            "<span class='market-icon market-icon-image'>"
            f"<img src='{uri}' alt=''></span>"
        )
    return f"<span class='market-icon'>{html.escape(fallback)}</span>"
