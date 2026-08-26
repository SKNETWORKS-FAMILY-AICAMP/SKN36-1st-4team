---
marp: true
theme: default
paginate: false
size: 16:9
html: true
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
  :root { --navy:#102b66; --blue:#1769e8; --sky:#eaf3ff; --cyan:#11b9e8; --orange:#ff9f1c; --ink:#17233c; --muted:#63708a; --cream:#fbfaf6; }
  * { box-sizing:border-box; }
  section {
    position:relative; width:1280px; height:720px; padding:54px 70px;
    font-family:'Noto Sans KR','Apple SD Gothic Neo',sans-serif;
    color:var(--ink); background:var(--cream); overflow:hidden;
  }
  section::before { content:""; position:absolute; left:0; top:0; width:9px; height:100%; background:var(--blue); }
  section::after { content:""; position:absolute; right:-80px; bottom:-145px; width:340px; height:250px; border:22px solid #dceaff; border-radius:50%; opacity:.85; }
  h1,h2,h3,p { margin:0; }
  h1 { color:var(--navy); font-size:48px; line-height:1.25; font-weight:800; }
  h2 { color:var(--navy); font-size:34px; line-height:1.3; font-weight:800; }
  h3 { color:var(--navy); font-size:23px; line-height:1.35; font-weight:700; }
  p,li { font-size:18px; line-height:1.65; }
  ul { margin:14px 0 0; padding-left:24px; }
  strong { color:var(--blue); }
  .titleline { display:flex; align-items:center; gap:14px; margin-bottom:34px; }
  .num { display:inline-grid; place-items:center; min-width:38px; height:38px; padding:0 10px; border-radius:9px; background:var(--blue); color:white; font-weight:800; font-size:20px; }
  .rule { height:2px; flex:1; background:linear-gradient(90deg,var(--blue),transparent); }
  .kicker { color:var(--blue); font-weight:800; letter-spacing:.08em; font-size:15px; text-transform:uppercase; }
  .subtitle { color:var(--muted); margin-top:12px; font-size:20px; }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:28px; }
  .grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:22px; }
  .card { background:white; border:1px solid #dce5f2; border-radius:18px; padding:24px 26px; box-shadow:0 8px 22px rgba(29,74,145,.06); }
  .soft { background:var(--sky); border:none; }
  .darkcard { background:var(--navy); color:white; border:none; }
  .pill { display:inline-block; padding:7px 15px; border-radius:999px; background:var(--blue); color:#fff; font-weight:700; font-size:15px; }
  .icon { display:inline-grid; place-items:center; width:50px; height:50px; border-radius:14px; background:var(--sky); color:var(--blue); font-size:25px; }
  .metric { font-size:52px; font-weight:800; color:var(--blue); line-height:1; }
  .metric-sm { font-size:38px; font-weight:800; color:var(--blue); }
  .label { color:var(--muted); font-size:15px; margin-top:8px; }
  .center { text-align:center; }
  .middle { height:100%; display:flex; flex-direction:column; justify-content:center; }
  .dark { background:#101827; color:white; }
  .dark::before { background:#2779f4; }
  .dark::after { border-color:#20375d; }
  .dark h1,.dark h2,.dark h3 { color:white; }
  .dark .subtitle,.dark .label { color:#a9b7cd; }
  .accent { color:var(--blue); }
  .orange { color:var(--orange); }
  .quote { border-left:5px solid var(--blue); padding:15px 22px; background:white; border-radius:0 14px 14px 0; font-size:22px; font-weight:700; color:var(--navy); }
  .flow { display:flex; align-items:center; justify-content:center; gap:12px; margin-top:30px; }
  .node { min-width:150px; padding:20px 16px; text-align:center; background:white; border:1px solid #d9e4f2; border-radius:14px; font-weight:700; }
  .node.blue { background:var(--blue); color:white; border-color:var(--blue); }
  .node.navy { background:var(--navy); color:white; border-color:var(--navy); }
  .arrow { color:#98a8c0; font-size:28px; }
  .barrow { display:grid; grid-template-columns:150px 1fr 70px; gap:14px; align-items:center; margin:16px 0; }
  .track { height:14px; background:#e5ebf4; border-radius:999px; overflow:hidden; }
  .fill { height:100%; background:linear-gradient(90deg,#8fc5ff,var(--blue)); border-radius:999px; }
  .table { width:100%; border-collapse:separate; border-spacing:0; overflow:hidden; border:1px solid #dbe4ef; border-radius:14px; background:white; font-size:16px; }
  .table th { background:var(--blue); color:white; padding:11px 14px; text-align:left; }
  .table td { padding:10px 14px; border-bottom:1px solid #e8edf4; }
  .table tr:last-child td { border-bottom:none; }
  .steps { display:flex; align-items:flex-start; justify-content:space-between; margin-top:38px; }
  .step { width:155px; text-align:center; position:relative; }
  .step b { display:grid; place-items:center; width:46px; height:46px; margin:0 auto 12px; background:var(--sky); color:var(--blue); border-radius:50%; }
  .step:not(:last-child)::after { content:"→"; position:absolute; right:-24px; top:8px; color:#9cabc0; font-size:28px; }
  .footer { position:absolute; left:70px; bottom:28px; color:#9ba7b8; font-size:13px; letter-spacing:.08em; }
  .section-cover h1 { font-size:54px; }
  .section-cover .mini-rule { width:130px; height:4px; background:var(--blue); margin:24px auto 0; border-radius:4px; }
  .persona { display:grid; grid-template-columns:320px 1fr 1fr; gap:18px; }
  .persona li { font-size:14px; line-height:1.55; margin-bottom:9px; }
  .persona ul { margin-top:18px; }
  .avatar { width:76px; height:76px; display:grid; place-items:center; border-radius:50%; background:var(--sky); font-size:40px; margin-bottom:16px; }
  .tiny { font-size:14px; line-height:1.5; color:var(--muted); }
  .check { color:#17a86b; font-weight:800; }
  .chart { display:flex; align-items:flex-end; justify-content:center; gap:34px; height:280px; padding:30px 35px 0; border-bottom:2px solid #dce4ef; }
  .col { width:90px; text-align:center; }
  .column { width:100%; border-radius:8px 8px 0 0; background:#aebdce; display:flex; align-items:flex-start; justify-content:center; padding-top:8px; color:white; font-weight:700; }
  .col:last-child .column { background:var(--blue); }
  .col span { display:block; margin-top:9px; font-size:14px; color:var(--muted); }
  .erd { display:flex; flex-direction:column; gap:26px; align-items:center; margin-top:28px; }
  .erd-row { display:flex; gap:70px; align-items:center; }
  .entity { min-width:220px; padding:18px; border-radius:12px; background:white; border:2px solid #dbe5f1; text-align:center; }
  .entity.primary { background:var(--blue); color:white; border-color:var(--blue); }
  .entity.fact { background:#eef8ff; border-color:#a9dff3; }
  .mutedbox { background:#f3f6fa; border-radius:11px; padding:14px 18px; color:#59677f; }
  .two-line { display:flex; gap:28px; align-items:center; }
  .bigq { font-size:92px; font-weight:800; color:#d5e8ff; line-height:1; }
---

<!-- _class: section-cover -->
<div class="middle center">
  <div class="kicker">TEAM 4 · 신기범 · 장반석 · 주민혁 · 장선아</div>
  <h1 style="margin-top:26px">중고차 리콜·결함신고<br>통합 조회 시스템</h1>
  <div class="mini-rule"></div>
</div>

---

<div class="titleline"><span class="num">0</span><h2>목차</h2><span class="rule"></span></div>
<div class="grid2" style="margin-top:35px">
  <div class="card"><span class="icon">⌕</span><h3 style="margin-top:14px">문제 정의</h3><p class="tiny">왜 리콜 정보만으로 충분하지 않은가</p></div>
  <div class="card"><span class="icon">◫</span><h3 style="margin-top:14px">서비스 핵심 기능</h3><p class="tiny">통합 조회·비교·해석 가이드</p></div>
  <div class="card"><span class="icon">✓</span><h3 style="margin-top:14px">프로젝트 사전 데이터 타당성 검증</h3><p class="tiny">신고가 리콜의 조기 신호인지 확인</p></div>
  <div class="card"><span class="icon">↗</span><h3 style="margin-top:14px">데이터가 연결되는 과정</h3><p class="tiny">전처리·ERD·조회 흐름</p></div>
  <div class="card" style="grid-column:1/3"><span class="icon">▣</span><h3 style="margin-top:14px">화면 설계 및 구현</h3><p class="tiny">사용자 흐름을 반영한 Streamlit 화면</p></div>
</div>

---

<!-- _class: section-cover -->
<div class="middle center"><h1>문제 정의</h1><div class="mini-rule"></div></div>

---

<div class="titleline"><span class="num">1</span><h2>문제 정의 · 현상 발견</h2><span class="rule"></span></div>
<div class="grid2">
  <div class="card soft">
    <div class="icon">!</div>
    <h3 style="margin-top:18px">차량 결함이 제기되더라도</h3>
    <p style="margin-top:15px">제조사 측에서 리콜을 인정해주지 않는 경우가 다수 발생합니다.</p>
  </div>
  <div class="card">
    <h3>대표 사례</h3>
    <ul>
      <li>벤츠 골프채 훼손 사건</li>
      <li>도요타 가속페달·급가속 관련 대규모 리콜</li>
    </ul>
  </div>
</div>
<div class="quote center" style="margin-top:38px">리콜 건수만으로는 차량의 잠재적 위험을 온전히 파악하기 어렵다</div>

---

<div class="titleline">
  <span class="num">1</span>
  <h2>문제 정의 · 현상 발견</h2>
  <span class="rule"></span>
</div>

<div style="text-align:center;">
<img
  src="중고차고려항목.png"
  alt="중고차 구매 고려사항"
  style="
    display:block;
    width:100px;
    max-height:400px;
    object-fit:contain;
    margin:0 auto;
  "
>
</div>

<div class="card soft center" style="margin-top:20px; padding:18px 30px;">
  <p>
    중고차를 선택하는 주된 동기가 저렴한 가격인 것은 사실이나,
  </p>

  <h3 style="margin-top:8px;">
    실제 차량 선택 시 중요하게 고려하는 요인은 차량의 품질
  </h3>
</div>

---

<div class="titleline">
  <span class="num">1</span>
  <h2>문제 정의 · 현상 발견</h2>
  <span class="rule"></span>
</div>

<!-- 화면 전체를 좌우 2개 grid로 분할 -->
<div class="grid2">

  <!-- 왼쪽 grid -->
  <div>
    <div class="card">
      <h3>
        가족과 함께 타려고 구매하는 패밀리카의 경우<br>
        안전에 대한 염려가 더 크지 않을까?
      </h3>

  <span class="pill" style="margin-top:20px;">
        True
      </span>

  <p style="margin-top:16px;">
        직영중고차 플랫폼 케이카에서 진행한 패밀리카 인식 조사에서
        가장 중요하게 고려하는 사항으로
        <strong>안전성</strong>이 꼽혔습니다.
      </p>
    </div>

  <div class="card soft" style="margin-top:18px;">
      <h3>더불어, 높아져가는 패밀리카에 대한 수요</h3>

  <p style="margin-top:16px;">
        모빌리티 서비스 전문 기업 오토핸즈의 2025년 상반기 거래
        실적에 따르면 신차와 중고차 시장에서 모두 가족 단위의
        이동이 가능한
        <strong>패밀리카 선호 경향이 뚜렷하게 나타났습니다.</strong>
      </p>
    </div>
  </div>

  <!-- 오른쪽 grid -->
  <div
    class="card"
    style="
      display:flex;
      align-items:center;
      justify-content:center;
      min-height:450px;
      overflow:hidden;
    "
  >
    <img
      src="패밀리카_시장.png"
      alt="패밀리카 관련 이미지"
      style="
        display:block;
        width:100%;
        max-height:410px;
        object-fit:contain;
      "
    >
  </div>

</div>

---

<div class="titleline"><span class="num">1</span><h2>문제 정의</h2><span class="rule"></span></div>
<div class="card" style="padding:34px 40px">
  <span class="pill">Broad Pain Point</span>
  <div class="two-line" style="margin-top:30px">
    <div class="icon" style="width:76px;height:76px;font-size:36px">⌕</div>
    <div>
      <p>차량에 결함이 존재하더라도 즉시 공식 리콜로 이어지는 것은 아니므로, <strong>공식 리콜 이력만으로는 차량의 잠재적 안전 위험을 충분히 파악하기 어렵습니다.</strong></p>
      <p style="margin-top:18px">특히 가족의 탑승을 전제로 안전성을 우선적으로 고려하는 패밀리카 중고차 수요자에게 이러한 정보의 공백은 구매 의사결정의 불확실성을 높입니다.</p>
    </div>
  </div>
</div>

---

<div class="titleline">
  <span class="num">1</span>
  <h2>타겟 정의</h2>
  <span class="rule"></span>
</div>

<div
  style="
    width:100%;
    height:520px;
    display:flex;
    align-items:center;
    justify-content:center;
  "
>
  <img
    src="./타겟.png"
    alt="타겟 정의"
    style="
      display:block;
      width:auto;
      height:auto;
      max-width:90%;
      max-height:500px;
      object-fit:contain;
      margin:0 auto;
    "
  >
</div>

---

<div class="titleline"><span class="num">2</span><h2>경쟁자 분석</h2><span class="rule"></span></div>
<table class="table" style="font-size:14px">
  <thead><tr><th>서비스</th><th>주요 기능</th><th>강점</th><th>남는 공백</th></tr></thead>
  <tbody>
    <tr><td><strong>자동차365</strong></td><td>검사·정비·자동차 정보 열람 등 종합 민원 조회</td><td>현 차량의 다양한 행정정보 제공</td><td>정보는 현 차량·구매 위험을 체계적으로 예측해주는 기능은 상대적으로 약함</td></tr>
    <tr><td><strong>카히스토리</strong></td><td>사고·침수·전손·도난·소유자 변경 등 조회</td><td>중고차의 과거 사고이력 확인에 강점</td><td>제조결함·정비 리콜·위험정보 등 과거 사고이력 중심</td></tr>
    <tr><td><strong>KB차차차</strong></td><td>중고차 매물, 공식 리콜 조회 및 알림</td><td>구매 과정에서 리콜 여부를 쉽게 확인 가능</td><td>공식 리콜 정보 중심이며 유사 연식·동일 모델의 잠재 결함 패턴 분석은 제한적</td></tr>
    <tr><td><strong>K Car</strong></td><td>매물 검색에서 대출·할부·검수 등 차량 이력 제공</td><td>대출·할부·검수 측면에서 보는 위험성 분석 가능</td><td>개별 차주의 결함·확인된 상태 중심</td></tr>
    <tr><td><strong>헤이딜러</strong></td><td>정비·수리·기타이력 등 차량 이력 조회</td><td>차량번호 기반 총위·호가를 파악·분석</td><td>유사 차량 데이터를 활용한 잠재 리스크 탐지 기능은 미흡</td></tr>
  </tbody>
</table>
<div class="quote" style="margin-top:18px">기존 서비스의 사각지대: 개별 매물의 과거 사고 이력과 공식 리콜 여부 확인에 초점이 맞춰져 있어, <strong>구매 의사결정 초기 단계에서 특정 차종·연식의 잠재적 안전 위험 신호를 파악하기 어려움</strong></div>

---

<div class="titleline"><span class="num">3</span><h2>페르소나 설정 · #1 김민준</h2><span class="rule"></span></div>
<div class="persona">
  <div class="card soft"><div class="avatar">👨</div><h3>김민준 · 35세 남성</h3><p class="tiny">둘째 아이 태어남 · 4인 가족</p><p class="tiny" style="margin-top:15px"><strong>상황</strong> 두 번째 자녀 출산 이후 카시트, 유모차 등 육아용품 적재로 기존 준중형 세단의 공간적 한계를 체감하면서, 자녀의 안전성과 충분한 적재·탑승 공간을 확보할 수 있는 패밀리카로의 교체를 고려함.</p><p class="tiny" style="margin-top:12px"><strong>목표</strong> 가족이 안전하게 탈 수 있는 중고차 찾기</p></div>
  <div class="card"><span class="pill">Pain point</span><ul><li>산발적으로 흩어진 정보와 상충되는 주관적인 의견이 많아 판단이 어려움</li><li>특정 연식의 문제인지, 인접 연식까지 일일이 찾아보기 번거로움</li><li>각 차종을 따로 검색해 비교해야 해서 시간과 노력이 많이 듦</li></ul></div>
  <div class="card"><span class="pill" style="background:#16a36a">Solution</span><ul><li>공식 데이터 기반의 신뢰할 수 있는 정보 통합 제공</li><li>관심 차량 연식과 유사한 연식의 차량 함께 조회 가능한 시스템</li><li>관심 차량을 한 화면에서 비교하고 조회할 수 있는 시스템</li></ul></div>
</div>

---

<div class="titleline"><span class="num">4</span><h2>페르소나 설정 · #2 오세린</h2><span class="rule"></span></div>
<div class="persona">
  <div class="card soft"><div class="avatar">👩</div><h3>오세린 · 33세 여성</h3><p class="tiny">첫째 아이 임신 중 · 3인 가족 예정</p><p class="tiny" style="margin-top:15px"><strong>상황</strong> 첫 차로 중고차 구매를 고려하고 있으나 자동차 관련 지식이 없어 어려움을 겪고 있음. 자동차에 대한 지식이 많지 않으며 아직 구매하고자 하는 차종을 구체적으로 결정하지 못함.</p><p class="tiny" style="margin-top:12px"><strong>목표</strong> 가족이 안전하게 탈 수 있는 중고차 찾기</p></div>
  <div class="card"><span class="pill">Pain point</span><ul><li>아직 차종을 결정하지 못해 일반 중고차 사이트에서 구체적인 정보에 접근하기 어려움</li><li>리콜·결함 정보가 여러 사이트에 흩어져 있고 숫자와 전문용어가 많아 해석이 어려움</li><li>신고 건수, 리콜 횟수의 의미와 해석 방법을 몰라 이해하기 어려움</li></ul></div>
  <div class="card"><span class="pill" style="background:#16a36a">Solution</span><ul><li>여러 차종을 탐색할 수 있는 광범위한 조회 시스템</li><li>리콜 제도와 결함신고 건수의 의미 안내</li><li>안전 지표 해석 가이드 제시</li></ul></div>
</div>

---

<div class="titleline"><span class="num">4</span><h2>페르소나 설정 · #3 설재민</h2><span class="rule"></span></div>
<div class="persona">
  <div class="card soft"><div class="avatar">👨‍💼</div><h3>설재민 · 29세 남성</h3><p class="tiny">예비 신혼부부</p><p class="tiny" style="margin-top:15px"><strong>상황</strong> 출퇴근·여행용 차량이 필요하지만 신차 구매는 예산상 부담되어 중고차를 고려함. 넉넉하지 않은 예산으로 중고차 구매를 결심했지만 차량의 품질을 중요시 여김.</p><p class="tiny" style="margin-top:12px"><strong>목표</strong> 가성비가 좋으면서도 품질이 보장된 중고차</p></div>
  <div class="card"><span class="pill">Pain point</span><ul><li>산발적으로 흩어진 정보와 상충되는 주관적인 의견이 많아 판단이 어려움</li><li>안전성에 대한 확신이 없어 구매 결정이 불안함</li><li>잠재 위험 지표와 가격 정보가 흩어져 있어 시간과 노력이 많이 듦</li></ul></div>
  <div class="card"><span class="pill" style="background:#16a36a">Solution</span><ul><li>공식 데이터 기반의 신뢰할 수 있는 정보 통합 제공</li><li>잠재 위험 지표 제시 및 해석 가이드 제공</li><li>중고차 매물 사이트와 연동된 조회 사이트</li></ul></div>
</div>

---

<div class="titleline"><span class="num">4</span><h2>Pain Point</h2><span class="rule"></span></div>
<div class="card" style="padding:32px 38px">
  <span class="num">01</span><h3 style="display:inline-block;margin-left:15px">공식 리콜 대상이 아니면 사용자가 문제없다고 받아들이기 쉬움</h3>
  <ul style="margin-top:28px"><li>공식 리콜 대상 X가 반드시 문제 가능성 X를 의미하지 않음</li><li>아직 조사 중이거나 공식화되지 않은 위험 신호가 존재할 가능성</li><li>구매 초기에는 리콜 여부뿐 아니라 <strong>반복적인 결함 신고 여부도 함께 확인할 필요</strong>가 있음</li></ul>
</div>

---

<div class="titleline"><span class="num">4</span><h2>Pain Point</h2><span class="rule"></span></div>
<div class="grid2">
  <div class="card">
    <span class="num">02</span><h3 style="margin-top:18px">정보는 존재하지만 직접 연결하고 해석하기 어려움</h3>
    <p style="margin-top:16px">리콜 및 결함 관련 데이터는 공개되어 있으나, 데이터가 흩어져 있어 확인 과정이 복잡하고 번거로움</p>
    <p style="margin-top:12px"><strong>→ 통합 조회 사이트의 필요성 존재</strong></p>
  </div>
  <div class="card">
    <span class="num">03</span><h3 style="margin-top:18px">개별 차량 이력만으로 모델 전체의 반복 위험을 파악하기 어려움</h3>
    <p style="margin-top:16px">구매할 개별 차량의 과거 이력은 비교적 쉽게 확인 가능하지만, 구매 초기에는 아직 특정 차량이 정해지지 않은 경우가 많음</p>
  
<div class="mutedbox" style="margin-top:20px">
  <strong>이 단계에서 확인할 것</strong> ① 어떤 모델에서 신고가 많이 발생했는지 ② 특정 연식에 신고가 집중되는지 ③ 인접 연식이나 유사 차량에서도 비슷한 문제가 나타나는지
</div>

---

<div class="middle center">
  <div class="kicker">HOW MIGHT WE</div>
  <div class="bigq">?</div>
  <h2>안전에 민감한 패밀리카 중고차 구매자가<br>잠재적 위험 신호를 쉽게 조회하고 판단하게 할 수 없을까?</h2>
</div>


---

<!-- _class: section-cover -->
<div class="middle center"><h1>서비스 핵심 기능</h1><div class="mini-rule"></div></div>

---

<div class="titleline"><span class="num">1</span><h2>차량 조건을 선택하면 리콜과 결함 신고를 함께 조회합니다</h2><span class="rule"></span></div>
<div class="grid2">
  <div class="card soft">
    <div class="icon">⌕</div><h3 style="margin-top:18px">결함 정보 조회</h3>
    <ul><li>제조사·대표 차종·모델연도 기준 검색</li><li>리콜 횟수·대상 대수·주요 사유 확인</li><li>소비자 결함 신고 건수 동시 제공</li></ul>
  </div>
  <div class="card">
    <h3>잠재 위험 신호까지 확인</h3>
    <div class="flow" style="margin-top:45px"><div class="node">공식 리콜</div><span class="arrow">+</span><div class="node blue">결함 신고</div></div>
    <p class="center" style="margin-top:30px">공식 리콜 이전에 반복되는 신고를 함께 살펴봅니다.</p>
  </div>
</div>

---

<div class="titleline"><span class="num">2</span><h2>관심 차량은 비교하고, 결과는 올바르게 해석합니다</h2><span class="rule"></span></div>
<div class="grid2">
  <div class="card"><div class="icon">▦</div><h3 style="margin-top:18px">차량 비교 서비스</h3><p>관심 차량 최대 5대의 리콜 횟수와 소비자 결함 신고 건수를 한눈에 비교합니다.</p></div>
  <div class="card"><div class="icon">FAQ</div><h3 style="margin-top:18px">해석 가이드</h3><p>리콜과 결함 신고 건수의 의미, 차대번호 재확인 필요성, 조회 결과의 한계를 안내합니다.</p></div>
</div>
<div class="quote" style="margin-top:28px">조회 결과는 위험의 확정 판정이 아니라, 구매 전 추가 확인이 필요한 잠재 신호입니다.</div>

---

<!-- _class: section-cover -->
<div class="middle center"><h1>프로젝트 사전 데이터 타당성 검증</h1><div class="mini-rule"></div></div>

---

<!-- _class: dark -->
<div class="middle">
  <div class="kicker" style="color:#72adff">NHTSA 분석 · 1</div>
  <h1 style="margin-top:22px">신고는 리콜의<br>조기 신호인가?</h1>
  <p class="subtitle">NHTSA 소비자 신고 × 공식 리콜 · 2020–2024</p>
  <div class="flow" style="justify-content:flex-start"><div class="node navy">12개월 신고</div><span class="arrow">→</span><div class="node blue">향후 24개월 리콜</div></div>
</div>

---

<div class="titleline"><h2>미국 NHTSA 데이터로 사전 검증했습니다</h2><span class="rule"></span></div>
<div class="grid2 center" style="margin-top:80px">
  <div><div class="metric">418,806</div><p class="label">소비자 신고 원본 행</p></div>
  <div><div class="metric" style="color:var(--ink)">4,544</div><p class="label">고유 리콜 캠페인</p></div>
</div>
<div class="mutedbox center" style="margin:65px auto 0;width:620px"><strong>최종 분석 15,724 관측치</strong><br>제조사 + 차종 + 모델연도 + 기준일</div>
<div class="footer">NHTSA 분석 · 2</div>

---

<div class="titleline">
  <h2>과거의 신고를 미래의 리콜과 연결했습니다</h2>
  <span class="rule"></span>
</div>

<div class="flow" style="margin-top:90px">
  <div class="node">
    <strong>신고 12개월</strong><br>
    <span class="tiny">신고 건수</span>
  </div>

  <span class="arrow">→</span>

  <div class="node navy">
    <strong>기준일</strong><br>
    <span class="tiny" style="color:#b9c6d7;">
      2021·2022·2023
    </span>
  </div>

  <span class="arrow">→</span>

<div class="node blue">
  <span class="recall-title">
    리콜 24개월
  </span>

  <br>

  <span class="recall-subtitle">
    발생 여부
  </span>
</div>
</div>

<div class="quote center" style="margin-top:65px;">
  같은 차량 조합을 시간 순서로 비교
</div>

<div class="footer">NHTSA 분석 · 3</div>

---

<div class="titleline"><h2>신고 11건 이상 그룹의 리콜률은 2.1배였습니다</h2><span class="rule"></span></div>
<div class="grid2">
  <div class="chart">
    <div class="col"><div class="column" style="height:95px">17.3%</div><span>1–2건</span></div>
    <div class="col"><div class="column" style="height:133px">24.4%</div><span>3–5건</span></div>
    <div class="col"><div class="column" style="height:151px">27.8%</div><span>6–10건</span></div>
    <div class="col"><div class="column" style="height:220px">36.62%</div><span>11건 이상</span></div>
  </div>
  <div class="middle" style="padding-left:40px">
    <div class="metric">36.62%</div><p class="label">11건 이상 그룹</p>
    <div class="metric-sm" style="margin-top:35px;color:var(--ink)">2.11×</div><p class="label">1–2건 그룹 대비</p>
  </div>
</div>
<div class="footer">NHTSA 분석 · 4</div>

---

<!-- _class: dark -->
<div class="titleline"><h2>관계는 약하지만, 우연은 아니었습니다</h2><span class="rule"></span></div>
<div class="grid2" style="align-items:center;margin-top:55px">
  <div><div class="metric" style="color:#70b8ff">r = 0.164</div><p class="subtitle">약한 양의 상관</p></div>
  <div>
    <div class="barrow"><b>Pearson</b><div class="track"><div class="fill" style="width:16.46%"></div></div><b>0.1646</b></div>
    <div class="barrow"><b>Spearman</b><div class="track"><div class="fill" style="width:16.36%"></div></div><b>0.1636</b></div>
    <p style="text-align:right;color:#72adff;font-weight:800">p &lt; .001</p>
  </div>
</div>
<div class="mutedbox center" style="margin-top:70px;background:#18243a;color:#c9d5e5">통계적으로 명확 ≠ 강한 예측력</div>
<div class="footer">NHTSA 분석 · 5</div>

---

<div class="titleline"><h2>다른 조건을 통제해도 신고의 신호는 남았습니다</h2><span class="rule"></span></div>
<div class="grid2" style="align-items:center;margin-top:50px">
  <div><div class="metric">1.324×</div><p style="margin-top:18px">신고량이 2배일 때<br><strong>리콜 오즈 +32.4%</strong></p><p class="tiny" style="margin-top:24px">기준연도 · 모델연도 통제</p></div>
  <div class="card">
    <h3>95% 신뢰구간</h3>
    <div style="position:relative;height:100px;margin-top:35px">
      <div style="position:absolute;left:15%;right:15%;top:46px;height:4px;background:#9fc8ff"></div>
      <div style="position:absolute;left:15%;top:36px;width:24px;height:24px;border-radius:50%;background:#9fc8ff"></div>
      <div style="position:absolute;left:48%;top:32px;width:32px;height:32px;border-radius:50%;background:var(--blue)"></div>
      <div style="position:absolute;right:15%;top:36px;width:24px;height:24px;border-radius:50%;background:#9fc8ff"></div>
      <div style="position:absolute;left:11%;top:75px">1.284</div><div style="position:absolute;left:45%;top:75px"><strong>1.324</strong></div><div style="position:absolute;right:10%;top:75px">1.364</div>
    </div>
    <p class="center tiny">구간 전체가 1보다 큼</p>
  </div>
</div>
<div class="footer">NHTSA 분석 · 6</div>

---

<!-- _class: dark -->
<div class="middle">
  <div class="kicker" style="color:#72adff">리콜체크 · 1</div>
  <h1 style="margin-top:20px">전처리에서 조회까지<br><span style="color:#69a9ff">데이터가 연결되는 과정</span></h1>
  <p class="subtitle">주피터 전처리 순서 · ERD · JOIN 흐름</p>
  <p style="margin-top:40px;color:#c5d1e2">소비자 결함신고 + 공식 리콜</p>
</div>

---

<div class="titleline"><h2>전처리는 여섯 단계로 진행했습니다</h2><span class="rule"></span></div>
<div class="steps">
  <div class="step"><b>01</b><h3>원본 보존</h3><p class="tiny">두 CSV</p></div>
  <div class="step"><b>02</b><h3>범위 선택</h3><p class="tiny">SUV·MPV</p></div>
  <div class="step"><b>03</b><h3>형식 정리</h3><p class="tiny">날짜·연도</p></div>
  <div class="step"><b>04</b><h3>이름 통일</h3><p class="tiny">제조사 별칭</p></div>
  <div class="step"><b>05</b><h3>차종 구조화</h3><p class="tiny">대표·세부</p></div>
  <div class="step"><b>06</b><h3>검증·저장</h3><p class="tiny">원본 추적</p></div>
</div>
<div class="quote center" style="margin-top:75px">원본은 남기고 · 비교 기준만 정리하고 · 결과를 별도 저장</div>
<div class="footer">DATA FLOW · 2</div>

---

<div class="titleline"><h2>출발점은 구조가 다른 두 개의 공식 데이터입니다</h2><span class="rule"></span></div>
<div class="grid2 center" style="margin-top:65px">
  <div class="card"><div class="metric">64,807</div><h3 style="margin-top:15px">소비자 결함신고</h3><p class="tiny">접수일 · 제작사 · 차명 · 모델연도</p></div>
  <div class="card"><div class="metric" style="color:var(--ink)">13,560</div><h3 style="margin-top:15px">공식 리콜</h3><p class="tiny">생산기간 · 개시일 · 대상대수 · 사유</p></div>
</div>
<div class="quote center" style="margin-top:44px">두 데이터는 차명 문자열이 아니라 <strong>대표차종 ID</strong>로 연결</div>
<div class="footer">DATA FLOW · 3</div>

---

<div class="titleline"><h2>원본을 덮어쓰지 않아 결과를 다시 추적할 수 있습니다</h2><span class="rule"></span></div>
<div class="kicker">STEP 01 · 원본 보존</div>
<div class="flow" style="margin-top:70px">
  <div class="node navy">RAW CSV<br><span class="tiny" style="color:#b9c6d7">받은 파일 그대로</span></div><span class="arrow">→</span>
  <div class="node blue">전처리 DataFrame<br><span class="tiny" style="color:#dceaff">필터·정규화</span></div><span class="arrow">→</span>
  <div class="node">전처리 CSV<br><span class="tiny">별도 폴더 저장</span></div>
</div>
<div class="mutedbox center" style="margin-top:70px">원본파일 + 원본행번호 + 원본 제작사명 + 원본 차명</div>
<div class="footer">DATA FLOW · 4</div>

---

<div class="titleline"><h2>서비스 목적에 맞는 패밀리카만 남겼습니다</h2><span class="rule"></span></div>
<div class="kicker">STEP 02 · 범위 선택</div>
<div class="flow" style="margin-top:55px">
  <div class="node"><div class="metric-sm">78,367</div><span class="tiny">원본 행</span></div><span class="arrow">→</span>
  <div class="node blue">SUV · MPV · 미니밴<br><span class="tiny" style="color:#dceaff">세단·이륜·특수·대형상용 제외</span></div><span class="arrow">→</span>
  <div class="node"><div class="metric-sm">21,572</div><span class="tiny">서비스 범위</span></div>
</div>
<div class="grid2 center" style="margin-top:60px"><p>결함신고 <strong>64,807 → 19,248</strong></p><p>공식 리콜 <strong>13,560 → 2,324</strong></p></div>
<div class="footer">DATA FLOW · 5</div>

---

<div class="titleline"><h2>서로 다른 열의 형식을 먼저 맞췄습니다</h2><span class="rule"></span></div>
<div class="kicker">STEP 03 · 형식 정리</div>
<div class="grid2" style="margin-top:45px">
  <div class="card">한글 파일 인코딩 <strong style="float:right">같은 문자 체계</strong></div>
  <div class="card">날짜 문자열 <strong style="float:right">YYYY-MM-DD</strong></div>
  <div class="card">모델연도 <strong style="float:right">숫자 연도</strong></div>
  <div class="card">리콜대수·빈칸 <strong style="float:right">숫자·결측값</strong></div>
</div>
<div class="footer">DATA FLOW · 6</div>

---

<div class="titleline"><h2>여러 제조사 표기를 하나의 대표 이름으로 연결했습니다</h2><span class="rule"></span></div>
<div class="kicker">STEP 04 · 이름 통일</div>
<div class="flow" style="margin-top:65px">
  <div class="card" style="width:340px"><p>한국토요타자동차</p><p>토요타코리아</p><p>한국토요타자동차(주)</p></div>
  <span class="arrow">→</span><div class="node blue" style="width:260px;font-size:26px">토요타<br><span class="tiny" style="color:#dceaff">대표 제조사명</span></div>
</div>
<div class="quote center" style="margin-top:60px">원본 이름은 보존 · 검색과 JOIN에는 대표 이름·ID 사용</div>
<div class="footer">DATA FLOW · 7</div>

---

<div class="titleline">
  <h2>차명은 대표차종과 세부차명으로 나눴습니다</h2>
  <span class="rule"></span>
</div>

<div class="kicker">STEP 05 · 차종 구조화</div>

<div class="erd">
  <div class="entity primary">
    <strong style="color:#ffffff !important;">
      대표차종
    </strong>
    <br>
    카니발
  </div>

  <div class="erd-row">
    <div class="entity">카니발 YP</div>
    <div class="entity">카니발 KA4</div>
    <div class="entity">카니발 하이리무진</div>
  </div>
</div>

<div
  class="mutedbox center"
  style="margin:45px auto 0; width:420px;"
>
  검색·집계의 공통 기준
</div>

<div class="footer">DATA FLOW · 8</div>

---

<div class="titleline"><h2>애매한 값은 억지로 합치지 않고 검토 대상으로 남겼습니다</h2><span class="rule"></span></div>
<div class="kicker">STEP 06 · 검증·저장</div>
<div class="grid3" style="margin-top:60px">
  <div class="card center"><div class="metric-sm check">✓</div><h3>확실한 일치</h3><p class="tiny">대표차종으로 연결</p></div>
  <div class="card center"><div class="metric-sm orange">?</div><h3>애매한 유사명</h3><p class="tiny">검토중 상태 유지</p></div>
  <div class="card center"><div class="metric-sm">↓</div><h3>결과 저장</h3><p class="tiny">원본 추적값 포함</p></div>
</div>
<div class="quote center" style="margin-top:50px">전처리 CSV 21,572행 → 정리 후 DB 18,323행</div>
<div class="footer">DATA FLOW · 9</div>

---

<div class="titleline"><h2>전처리 결과는 조회하기 쉬운 SQLite 구조로 바뀝니다</h2><span class="rule"></span></div>
<div class="flow" style="margin-top:80px">
  <div class="node navy">전처리 CSV<br><span class="tiny" style="color:#b9c6d7">신고 19,248 · 리콜 2,324</span></div><span class="arrow">→</span>
  <div class="node blue">SQLite<br><span class="tiny" style="color:#dceaff">제조사·차종 ID 생성</span></div><span class="arrow">→</span>
  <div class="node">조회용 DB<br><span class="tiny">18,323행 · 2개 VIEW</span></div>
</div>
<div class="quote center" style="margin-top:70px">CSV 전체를 매번 읽지 않고 한 개의 DB에서 필요한 행만 조회</div>
<div class="footer">DATA FLOW · 10</div>

---

<div class="titleline"><h2>핵심 ERD는 다섯 테이블의 역할을 분리합니다</h2><span class="rule"></span></div>
<div class="erd">
  <div class="erd-row"><div class="entity">manufacturers<br><span class="tiny">제조사</span></div><div class="entity primary">vehicle_models<br><span class="tiny" style="color:#dceaff">대표차종 · 공통 연결점</span></div><div class="entity">vehicle_variants<br><span class="tiny">세부차명</span></div></div>
  <div class="erd-row"><div class="entity fact">defect_reports<br><span class="tiny">접수일 · 모델연도 · 원본명</span></div><div class="entity fact">recalls<br><span class="tiny">생산기간 · 개시일 · 사유</span></div></div>
</div>
<div class="footer">DATA FLOW · 11</div>

---

<div class="titleline"><h2>PK는 행을 구분하고, FK는 다른 표를 연결합니다</h2><span class="rule"></span></div>
<table class="table" style="margin-top:40px">
<thead><tr><th>vehicle_models</th><th>역할</th><th>defect_reports / recalls</th><th>역할</th></tr></thead>
<tbody><tr><td><strong>model_id</strong></td><td>대표차종의 PK</td><td><strong>model_id</strong></td><td>같은 대표차종을 가리키는 FK</td></tr><tr><td>manufacturer_id</td><td>제조사를 가리키는 FK</td><td>variant_id</td><td>세부차명 선택 시 사용</td></tr></tbody>
</table>
<div class="quote center" style="margin-top:55px">문자열 대신 ID로 연결하면 표기가 달라도 같은 차량으로 조회할 수 있습니다.</div>
<div class="footer">DATA FLOW · 12</div>

---

<div class="titleline"><h2>제조사를 선택하면 해당 제조사의 차종만 이어집니다</h2><span class="rule"></span></div>
<div class="flow" style="margin-top:95px">
  <div class="node">사용자 선택<br><strong>기아</strong></div><span class="arrow">→</span>
  <div class="node navy">manufacturers<br><span class="tiny" style="color:#b9c6d7">manufacturer_id</span></div><span class="arrow">→</span>
  <div class="node blue">vehicle_models<br><span class="tiny" style="color:#dceaff">같은 ID만 필터</span></div>
</div>
<div class="mutedbox center" style="margin-top:70px">제조사 ID가 같은 대표차종 목록 → 다음 선택창</div>
<div class="footer">DATA FLOW · 13</div>

---

<div class="titleline"><h2>선택 차종의 신고는 model_id와 모델연도로 조회합니다</h2><span class="rule"></span></div>
<div class="flow" style="margin-top:85px">
  <div class="node blue">vehicle_models<br><span class="tiny" style="color:#dceaff">선택 model_id</span></div><span class="arrow">→</span>
  <div class="node navy">defect_reports<br><span class="tiny" style="color:#b9c6d7">model_id + model_year</span></div><span class="arrow">→</span>
  <div class="node">화면 결과<br><span class="tiny">신고 수 · 연도별 막대</span></div>
</div>
<div class="metric-sm center" style="margin-top:60px">COUNT(*)</div><p class="center tiny">신고 한 행을 한 건으로 집계</p>
<div class="footer">DATA FLOW · 14</div>

---

<div class="titleline"><h2>공식 리콜도 같은 model_id에서 별도로 가져옵니다</h2><span class="rule"></span></div>
<div class="flow" style="margin-top:85px">
  <div class="node blue">vehicle_models<br><span class="tiny" style="color:#dceaff">선택 model_id</span></div><span class="arrow">→</span>
  <div class="node navy">recalls<br><span class="tiny" style="color:#b9c6d7">같은 model_id</span></div><span class="arrow">→</span>
  <div class="node">화면 결과<br><span class="tiny">생산기간 · 사유 · 대상대수</span></div>
</div>
<div class="quote center" style="margin-top:65px">신고 테이블과 직접 JOIN하지 않고 각각 조회</div>
<div class="footer">DATA FLOW · 15</div>

---

<!-- _class: dark -->
<div class="titleline"><h2>모델연도와 생산기간은 같은 기준이 아닙니다</h2><span class="rule"></span></div>
<div class="grid2 center" style="align-items:center;margin-top:80px">
  <div><div class="metric" style="color:#70b8ff">2020년형</div><p class="subtitle">신고 데이터의 모델연도</p></div>
  <div><div class="metric-sm" style="color:white">2019.08 ─ 2020.05</div><p class="subtitle">리콜 대상 차량의 생산기간</p></div>
</div>
<div class="center" style="font-size:60px;color:#72adff;margin-top:20px">≠</div>
<div class="mutedbox center" style="margin-top:25px;background:#18243a;color:#c9d5e5">공통 model_id 아래에서 각각 보여주되 ‘2020년형이 이 리콜 대상’이라고 단정하지 않습니다.</div>
<div class="footer">DATA FLOW · 16</div>

---

<div class="titleline"><h2>요약 화면은 신고와 리콜을 각각 센 뒤 합칩니다</h2><span class="rule"></span></div>
<div class="grid3" style="align-items:center;margin-top:55px">
  <div class="card center"><h3>defect_reports</h3><p>model_id별 신고 수</p></div>
  <div class="card soft center"><h3>model_overview</h3><p>대표차종 기준<br><strong>LEFT JOIN</strong></p></div>
  <div class="card center"><h3>recalls</h3><p>model_id별 기록 수·대수</p></div>
</div>
<div class="flow"><span class="pill">먼저 집계</span><span class="arrow">→</span><span class="pill">나중에 JOIN</span></div>
<div class="quote center" style="margin-top:40px">원본 행이 서로 곱해져 과다 집계되는 문제를 방지</div>
<div class="footer">DATA FLOW · 17</div>

---

<div class="titleline"><h2>화면에서는 선택값이 SQL 조건으로 전달됩니다</h2><span class="rule"></span></div>
<div class="flow" style="margin-top:95px;gap:8px">
  <div class="node">사용자 선택<br><span class="tiny">제조사·차종·연도</span></div><span class="arrow">→</span>
  <div class="node blue">Streamlit<br><span class="tiny" style="color:#dceaff">선택 ID 저장</span></div><span class="arrow">→</span>
  <div class="node">SQL 조건<br><span class="tiny">model_id 전달</span></div><span class="arrow">→</span>
  <div class="node navy">SQLite<br><span class="tiny" style="color:#b9c6d7">조건 행 검색</span></div><span class="arrow">→</span>
  <div class="node">표·그래프<br><span class="tiny">DataFrame</span></div>
</div>
<div class="quote center" style="margin-top:70px">CSV 전체를 다시 읽지 않고 필요한 행만 빠르게 반환</div>
<div class="footer">DATA FLOW · 18</div>

---

<!-- _class: dark -->
<div class="titleline"><h2>핵심은 ‘원본 보존, ID 연결, 분리 조회’입니다</h2><span class="rule"></span></div>
<div class="grid3" style="margin-top:80px">
  <div class="darkcard card center"><div class="metric-sm" style="color:#72adff">01</div><h3 style="margin-top:18px">원본 보존</h3><p class="tiny" style="color:#a9b7cd">출처와 원본명 유지</p></div>
  <div class="darkcard card center"><div class="metric-sm" style="color:#72adff">02</div><h3 style="margin-top:18px">대표차종 ID</h3><p class="tiny" style="color:#a9b7cd">신고·리콜의 공통 기준</p></div>
  <div class="darkcard card center"><div class="metric-sm" style="color:#72adff">03</div><h3 style="margin-top:18px">각각 조회</h3><p class="tiny" style="color:#a9b7cd">신고와 리콜을 섞지 않음</p></div>
</div>
<div class="mutedbox center" style="margin-top:70px;background:#18243a;color:#c9d5e5">전처리는 데이터를 줄이는 일이 아니라, 같은 기준으로 찾게 만드는 일</div>
<div class="footer">리콜체크 · 19</div>

---

<!-- _class: dark -->
<div class="titleline"><h2>부록 · 전체 ERD</h2><span class="rule"></span></div>
<div class="erd" style="transform:scale(.82);transform-origin:top center">
  <div class="erd-row"><div class="entity">manufacturers<br><span class="tiny">manufacturer_id · name</span></div><div class="entity primary">vehicle_models<br><span class="tiny" style="color:#dceaff">model_id · manufacturer_id · model_name</span></div><div class="entity">vehicle_variants<br><span class="tiny">variant_id · model_id · variant_name</span></div></div>
  <div class="erd-row"><div class="entity fact">defect_reports<br><span class="tiny">report_id · model_id · model_year · report_date</span></div><div class="entity fact">recalls<br><span class="tiny">recall_id · model_id · start_date · affected_count</span></div></div>
</div>
<div class="mutedbox center" style="margin-top:0;background:#18243a;color:#c9d5e5">발표에서는 핵심 5개 테이블을 설명하고, 질문이 나오면 전체 구조를 제시</div>
<div class="footer">APPENDIX · 20</div>

---

<!-- _class: section-cover -->
<div class="middle center"><h1><span class="num" style="vertical-align:middle;margin-right:15px">3</span>화면 설계 및 구현</h1><div class="mini-rule"></div></div>

---

<div class="titleline"><span class="num">3</span><h2>화면 설계</h2><span class="rule"></span></div>
<table class="table" style="margin-top:35px">
<thead><tr><th>상위 메뉴</th><th>메뉴명</th><th>Screen ID</th><th>Page Title</th></tr></thead>
<tbody><tr><td>공통</td><td>공통 헤더</td><td>UI-H-001</td><td>자동차 리콜 통합 안내</td></tr><tr><td>차량 조회</td><td>차량 조회</td><td>UI-M-001</td><td>차량 조회</td></tr><tr><td>차량 비교</td><td>차량 비교</td><td>UI-M-002</td><td>차량 비교</td></tr><tr><td>도움말</td><td>도움말</td><td>UI-M-003</td><td>도움말 · 데이터 안내</td></tr></tbody>
</table>
<div class="grid3" style="margin-top:35px"><div class="card center"><strong>리콜 조회</strong></div><div class="card center"><strong>차종 비교</strong></div><div class="card center"><strong>도움말</strong></div></div>

---

<div class="middle center">
  <div class="icon" style="margin:0 auto 24px;width:72px;height:72px;font-size:34px">↗</div>
  <h1>서비스 화면 확인</h1>
  <a href="http://localhost:8501/" style="display:inline-block;margin-top:32px;color:var(--blue);font-size:24px;font-weight:700">http://localhost:8501/</a>
  <p class="subtitle">Streamlit 로컬 실행 후 접속</p>
</div>

---

<div class="middle center">
  <div class="kicker">TEAM 4</div>
  <h1 style="margin-top:26px">감사합니다</h1>
  <div class="mini-rule"></div>
  <p class="subtitle">중고차 구매 전, 공식 리콜과 잠재 위험 신호를 함께 확인합니다.</p>
</div>
