"""연식별 판매량 CSV를 앱 대표 차종 이름과 연결한다."""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

from config import SALES_BY_YEAR_PATH

# 판매량 표기는 짧은 차종명, 앱은 트림명이라 한글/영문 별칭이 필요하다.
SALES_ALIASES = {
    "시에나": ["sienna"],
    "오딧세이": ["odyssey", "오디세이"],
    "익스플로러": ["explorer"],
    "M클래스": ["ML350"],
    "QM3/캡처": ["QM3", "CAPTUR"],
    "XM3/아르카나": ["XM3", "ARKANA"],
    "그랑 콜레오스": ["KOLEOS"],
    "알파드": ["Alphard"],
}


def clean_key(value: object) -> str:
    """판매량 차종명과 앱 차종명을 같은 비교 문자열로 맞춘다."""
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"[^0-9a-z가-힣]+", "", text)


def load_sales_frame() -> pd.DataFrame:
    """연도·모델·판매량 표. 파일이 없으면 빈 표."""
    if not SALES_BY_YEAR_PATH.exists():
        return pd.DataFrame(columns=["year", "sales_model", "units"])

    frame = pd.read_csv(SALES_BY_YEAR_PATH, encoding="utf-8-sig")
    rename = {"연도": "year", "모델": "sales_model", "판매량": "units"}
    frame = frame.rename(columns=rename)
    missing = {"year", "sales_model", "units"} - set(frame.columns)
    if missing:
        return pd.DataFrame(columns=["year", "sales_model", "units"])

    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["units"] = pd.to_numeric(frame["units"], errors="coerce")
    frame["sales_model"] = frame["sales_model"].fillna("").astype(str)
    return frame.dropna(subset=["year", "sales_model", "units"])


def _sales_name_keys(sales_model: str) -> list[str]:
    keys = [clean_key(sales_model)]
    for alias in SALES_ALIASES.get(sales_model, []):
        keys.append(clean_key(alias))
    return [key for key in keys if key]


def _token_haystack(model_name: str) -> str:
    # 하이픈은 "E-PACE"처럼 코드명 중간에 붙는 경우가 많아, 띄어쓰기로 갈라지지 않도록
    # 다른 구두점보다 먼저 통째로 지운다.
    text = unicodedata.normalize("NFKC", str(model_name)).casefold().replace("-", "")
    return re.sub(r"[^0-9a-z가-힣]+", " ", text)


def _key_in_model(model_name: str, needle: str) -> bool:
    """영문·숫자 코드는 단어 시작 기준으로, 한글 차종명은 부분 문자열로 맞춘다.

    "GLC" -> "GLC350", "XC90" -> "XC90B6"처럼 코드 뒤에 엔진·트림 표기가
    붙어 있는 경우가 많아 뒤쪽 경계는 확인하지 않는다.
    """
    if re.fullmatch(r"[0-9a-z]+", needle):
        haystack = _token_haystack(model_name)
        pattern = rf"(?<![0-9a-z]){re.escape(needle)}"
        return re.search(pattern, haystack) is not None
    return needle in clean_key(model_name)


def match_sales_model(model_name: str, sales_models: list[str]) -> str | None:
    """앱 대표 차종명에 들어 있는 판매량 차종명을 고른다. 더 긴 이름을 우선한다."""
    if not clean_key(model_name):
        return None

    ranked: list[tuple[int, str]] = []
    for sales_model in sales_models:
        keys = _sales_name_keys(sales_model)
        matched_keys = [key for key in keys if _key_in_model(model_name, key)]
        if matched_keys:
            ranked.append((max(len(key) for key in matched_keys), sales_model))
    if not ranked:
        return None
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[0][1]


def sales_volume_by_year(sales: pd.DataFrame, sales_model: str) -> dict[int, int]:
    """한 판매량 차종의 연도별 대수."""
    rows = sales.loc[sales["sales_model"] == sales_model]
    return {int(row.year): int(row.units) for row in rows.itertuples(index=False)}


def sales_lookup_for_model(model_name: str) -> tuple[str | None, dict[int, int]]:
    """대표 차종에 대응하는 판매량 패밀리명과 연도별 대수."""
    sales = load_sales_frame()
    if sales.empty:
        return None, {}
    sales_models = sales["sales_model"].drop_duplicates().tolist()
    family = match_sales_model(model_name, sales_models)
    if family is None:
        return None, {}
    return family, sales_volume_by_year(sales, family)


def missing_sales_year_rows(
    models: pd.DataFrame,
    defect_years: pd.DataFrame,
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """결함 신고 연식은 있는데 같은 해 판매량이 없는 행."""
    sales_models = sales["sales_model"].drop_duplicates().tolist() if not sales.empty else []
    rows: list[dict[str, object]] = []
    for model in models.itertuples(index=False):
        family = match_sales_model(str(model.model_name), sales_models)
        year_units = sales_volume_by_year(sales, family) if family else {}
        model_years = defect_years.loc[defect_years["model_id"] == model.model_id]
        for year_row in model_years.itertuples(index=False):
            year = int(year_row.model_year)
            if year in year_units:
                continue
            rows.append(
                {
                    "제조사": model.manufacturer_name,
                    "차종": model.model_name,
                    "연식": year,
                    "신고건수": int(year_row.complaint_count),
                    "사유": "차종 판매량 없음" if family is None else "해당 연식 판매량 없음",
                }
            )
    return pd.DataFrame(rows)
