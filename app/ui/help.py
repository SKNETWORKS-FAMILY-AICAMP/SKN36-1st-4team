"""도움말 · FAQ 탭."""

from __future__ import annotations

import streamlit as st

from config import GOVERNMENT_RECALL_URL


def render_help() -> None:
    """데이터 기준과 FAQ를 설명한다."""
    st.markdown("## 도움말 · 데이터 안내")
    st.markdown("### 자주 묻는 질문")
    with st.expander("리콜 대상 차량이면 무조건 수리받을 수 있나요?", expanded=True):
        st.write("공식 리콜 대상이라면 제작사가 안내한 방법에 따라 조치받을 수 있습니다. 다만 이 서비스는 차종·생산기간 기준 정보이므로, 실제 차량의 대상 여부와 조치 완료 여부는 차량번호나 차대번호로 자동차리콜센터에서 다시 확인해야 합니다.")
        st.link_button("자동차리콜센터에서 확인", GOVERNMENT_RECALL_URL, width="stretch")
    with st.expander("리콜 조치가 완료됐는지 어떻게 확인하나요?"):
        st.write("자동차리콜센터에서 차량번호 또는 차대번호를 입력해 확인하세요. 개별 차량의 리콜 조치 여부는 제작사가 국토교통부에 보고한 진행 내역을 기준으로 제공됩니다.")
        st.link_button("리콜 대상·조치 여부 조회", "https://www.car.go.kr/ri/recall/list.do", width="stretch")
    with st.expander("소비자 신고가 많으면 결함이 확정된 건가요?"):
        st.write("아닙니다. 신고 건수는 소유자가 접수한 기록의 수일 뿐, 결함 확정이나 리콜 결정을 의미하지 않습니다. 같은 차종에서 신고가 반복되는지 확인하는 구매 전 참고 신호로 활용하세요.")
    with st.expander("중고차 판매자에게 어떤 서류를 받아야 하나요?"):
        st.write("자동차성능·상태점검기록부를 받아 실제 차량 상태와 비교해야 합니다. 자동차매매업자는 점검 내용을 기재한 기록부를 매수인에게 발급해야 하므로, 계약 전에 기록부와 특약사항을 함께 확인하세요.")
        st.link_button("관련 법령 확인", "https://www.law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0120&lsiSeq=285101&urlMode=lsScJoRltInfoR", width="stretch")
    with st.expander("구매 후 신고된 결함이 발견되면 어떻게 하나요?"):
        st.write("차량 사진, 정비내역, 판매자와 주고받은 문자, 계약서, 성능·상태점검기록부를 보관하고 판매자에게 먼저 서면으로 알리세요. 해결되지 않으면 1372 소비자상담센터에 상담을 신청할 수 있습니다.")
        st.link_button("1372 소비자상담 절차", "https://www.kca.go.kr/odr/pg/ma/cnsutInfo.do", width="stretch")
    with st.expander("소비자도 자동차 결함을 직접 신고할 수 있나요?"):
        st.write("가능합니다. 자동차리콜센터에서 결함 신고를 접수할 수 있습니다. 다만 리콜센터는 결함 정보를 수집·분석하는 기관이므로, 개인 간 판매 분쟁을 직접 해결하거나 중재하는 곳은 아닙니다.")
        st.link_button("자동차 결함신고 안내", "https://www.car.go.kr/ds/dfct/gdnc.do", width="stretch")
    st.markdown("### 공식 사이트 바로가기")
    st.markdown(
        "리콜 대상 여부와 개별 차량의 조치 완료 여부는 아래 공식 사이트에서 다시 확인할 수 있습니다.",
    )
    st.link_button("정부 자동차리콜센터 리콜 현황", GOVERNMENT_RECALL_URL, width="stretch")
    st.markdown("<div class='source-note'>데이터 출처: 한국교통안전공단 자동차리콜센터 제공 자료를 전처리한 프로젝트 DB</div>", unsafe_allow_html=True)
