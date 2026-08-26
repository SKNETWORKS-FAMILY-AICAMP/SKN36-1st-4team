"""경로, 외부 링크, 제조사 표시 이름처럼 화면과 무관한 설정값."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "processed" / "database" / "recall_checker.sqlite3"
IMAGE_DIR = PROJECT_ROOT / "assets" / "vehicles"
ICON_DIR = PROJECT_ROOT / "assets" / "icons"
IMAGE_ALIAS_PATH = PROJECT_ROOT / "data" / "mappings" / "vehicle_image_aliases.csv"
AD_IMAGE_PATH = PROJECT_ROOT / "assets" / "recall_public_service_ad.png"
HERO_IMAGE_PATH = PROJECT_ROOT / "assets" / "hero" / "korean-family-suv-sunrise-v2.png"
SERVICE_LOGO_PATH = PROJECT_ROOT / "assets" / "brand" / "recall-check-logo-v1.png"
STYLES_PATH = Path(__file__).with_name("styles.css")
PUBLIC_AD_HIDE_COOKIE = "recall_ad_hide_date"

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
MANUFACTURER_SHORT_NAMES = {
    "현대자동차": "현대",
    "혼다코리아": "혼다",
    "르노코리아": "르노",
    "메르세데스 벤츠": "벤츠",
    "KG 모빌리티": "KGM",
}
MANUFACTURER_ICON_FILES = {
    "KG 모빌리티": "manufacturers/kgm",
    "BMW": "manufacturers/bmw",
    "기아": "manufacturers/kia",
    "르노코리아": "manufacturers/renault",
    "메르세데스 벤츠": "manufacturers/mercedes",
    "볼보": "manufacturers/volvo",
    "토요타": "manufacturers/toyota",
    "재규어랜드로버": "manufacturers/jaguarlandrover",
    "포드": "manufacturers/ford",
    "현대자동차": "manufacturers/hyundai",
    "혼다코리아": "manufacturers/honda",
}

# 조회한 차량을 실제 매물 사이트에서 다시 찾아볼 수 있는 외부 링크
USED_CAR_MARKET_LINKS = [
    ("markets/heydealer", "헤이딜러", "내 차 시세·중고차", "https://www.heydealer.com/"),
    ("markets/danawa", "다나와 자동차", "중고차 매물 검색", "https://auto.danawa.com/usedcar/"),
    ("markets/encar", "엔카", "국내 중고차 매물", "https://www.encar.com/"),
    ("markets/kbchachacha", "KB차차차", "중고차 검색·시세", "https://www.kbchachacha.com/public/search/main.kbc"),
    ("markets/kcar", "K Car", "직영 중고차", "https://www.kcar.com/"),
]
ICON_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}
