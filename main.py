import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="Cinema Box Office",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------------
# 시네마틱 배경 디자인
# -----------------------------------
st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(
            rgba(5, 5, 10, 0.88),
            rgba(8, 8, 18, 0.94)
        ),
        radial-gradient(
            circle at 50% 0%,
            rgba(120, 80, 180, 0.25),
            transparent 45%
        ),
        radial-gradient(
            circle at 10% 80%,
            rgba(40, 80, 150, 0.18),
            transparent 40%
        ),
        #050509;
}

/* 위쪽 영화관 조명 효과 */
.stApp::before {
    content: "";
    position: fixed;
    top: -180px;
    left: 50%;
    transform: translateX(-50%);
    width: 700px;
    height: 450px;
    background: radial-gradient(
        ellipse,
        rgba(255, 220, 150, 0.10),
        transparent 65%
    );
    pointer-events: none;
    z-index: 0;
}

/* 전체 콘텐츠 */
.block-container {
    position: relative;
    z-index: 1;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* 메인 제목 */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 5px;
    color: #ffffff;
    text-shadow:
        0 0 10px rgba(255,255,255,0.25),
        0 0 30px rgba(120,100,255,0.25);
}

/* 부제목 */
.subtitle {
    text-align: center;
    color: #aaa9b8;
    font-size: 16px;
    margin-bottom: 35px;
}

/* 정보 카드 */
.metric-card {
    background: rgba(20, 20, 30, 0.72);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(12px);
    box-shadow:
        0 10px 35px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

/* 순위 테이블 영역 */
.table-box {
    background: rgba(15, 15, 23, 0.78);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 18px;
    margin-top: 20px;
    backdrop-filter: blur(10px);
}

/* 섹션 제목 */
.section-title {
    color: white;
    font-size: 24px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 10px;
}

/* 설명 */
.info-text {
    color: #9999a8;
    font-size: 14px;
}

/* Streamlit metric 글자 */
[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: #aaa9b8;
}

/* 데이터프레임 */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* 버튼 */
.stButton > button {
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    color: white;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# 제목
# -----------------------------------
st.markdown(
    '<div class="main-title">🎬 CINEMA BOX OFFICE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">어제의 영화 매출 순위를 한눈에 확인하세요</div>',
    unsafe_allow_html=True
)


# -----------------------------------
# KOBIS 인증키
# -----------------------------------
try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]
except Exception:
    st.error(
        "KOBIS_KEY가 설정되어 있지 않습니다. "
        "Streamlit Cloud의 Secrets에 KOBIS_KEY를 등록해주세요."
    )
    st.stop()


# -----------------------------------
# 한국 시간 기준 어제
# -----------------------------------
yesterday = (
    datetime.now(ZoneInfo("Asia/Seoul"))
    - timedelta(days=1)
)

target_dt = yesterday.strftime("%Y%m%d")

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#8f8e9c;
        margin-bottom:25px;
    ">
        📅 조회 기준일 : {yesterday.strftime('%Y년 %m월 %d일')}
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# KOBIS API
# -----------------------------------
url = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)

try:
    res = requests.get(
        url,
        params={
            "key": KOBIS_KEY,
            "targetDt": target_dt
        },
        timeout=10
    )

except requests.exceptions.RequestException as e:
    st.error("영화 정보를 불러오는 중 오류가 발생했습니다.")
    st.error(str(e))
    st.stop()


# -----------------------------------
# API 응답 확인
# -----------------------------------
if res.status_code != 200:
    st.error(
        f"요청이 실패했습니다. "
        f"(상태코드: {res.status_code})"
    )
    st.stop()


try:
    data = res.json()
except Exception:
    st.error("영화 API에서 올바른 데이터를 받지 못했습니다.")
    st.stop()


# 인증키 오류
if "faultInfo" in data:
    st.error(
        "인증키가 올바르지 않습니다. "
        "Streamlit Secrets의 KOBIS_KEY를 확인해주세요."
    )
    st.stop()


# -----------------------------------
# 영화 데이터
# -----------------------------------
box_list = (
    data
    .get("boxOfficeResult", {})
    .get("dailyBoxOfficeList", [])
)

if not box_list:
    st.warning("해당 날짜의 영화 자료가 없습니다.")
    st.stop()


df = pd.DataFrame(box_list)


# -----------------------------------
# 숫자 데이터 변환
# -----------------------------------
number_columns = [
    "rank",
    "rankInten",
    "salesAmt",
    "salesShare",
    "salesInten",
    "salesChange",
    "salesAcc",
    "audiCnt",
    "audiAcc",
    "scrnCnt",
    "showCnt"
]

for col in number_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# -----------------------------------
# 매출액 기준 순위
# -----------------------------------
df = df.sort_values(
    "salesAmt",
    ascending=False
).reset_index(drop=True)


# -----------------------------------
# 1위 영화
# -----------------------------------
top = df.iloc[0]


# -----------------------------------
# 상단 핵심 정보
# -----------------------------------
c1, c2, c3 = st.columns(3)


with c1:
    st.metric(
        "🏆 매출 1위",
        top["movieNm"]
    )


with c2:
    st.metric(
        "💰 일일 매출",
        f"{int(top['salesAmt']):,}원"
    )


with c3:
    st.metric(
        "🎞️ 누적 매출",
        f"{int(top['salesAcc']):,}원"
    )


# -----------------------------------
# 영화 매출 순위표
# -----------------------------------
st.markdown(
    '<div class="section-title">🏆 영화 매출 순위 TOP 10</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="info-text">'
    '전날 기준 영화별 일일 매출액을 기준으로 정렬한 순위입니다.'
    '</div>',
    unsafe_allow_html=True
)


table = df[
    [
        "rank",
        "movieNm",
        "openDt",
        "salesAmt",
        "salesAcc",
        "salesShare",
        "audiCnt"
    ]
].copy()


table.columns = [
    "순위",
    "영화명",
    "개봉일",
    "일일 매출",
    "누적 매출",
    "매출 점유율",
    "관객수"
]


# 원화와 % 표시
table["일일 매출"] = table["일일 매출"].apply(
    lambda x: f"{int(x):,}원"
)

table["누적 매출"] = table["누적 매출"].apply(
    lambda x: f"{int(x):,}원"
)

table["매출 점유율"] = table["매출 점유율"].apply(
    lambda x: f"{x:.1f}%"
)

table["관객수"] = table["관객수"].apply(
    lambda x: f"{int(x):,}명"
)


st.dataframe(
    table.head(10),
    use_container_width=True,
    hide_index=True,
    height=440
)


# -----------------------------------
# 매출 TOP 5 그래프
# -----------------------------------
st.markdown(
    '<div class="section-title">📊 매출액 TOP 5</div>',
    unsafe_allow_html=True
)

chart_df = df.head(5).copy()

chart_df["매출액"] = chart_df["salesAmt"]

chart_data = chart_df[
    ["movieNm", "매출액"]
].set_index("movieNm")


st.bar_chart(chart_data)


# -----------------------------------
# 영화별 추가 정보
# -----------------------------------
st.markdown(
    '<div class="section-title">🎞️ 영화별 관객 정보</div>',
    unsafe_allow_html=True
)

audience_df = df[
    ["movieNm", "audiCnt", "audiAcc"]
].head(10).copy()

audience_df.columns = [
    "영화명",
    "어제 관객수",
    "누적 관객수"
]

audience_df["어제 관객수"] = audience_df[
    "어제 관객수"
].apply(lambda x: f"{int(x):,}명")

audience_df["누적 관객수"] = audience_df[
    "누적 관객수"
].apply(lambda x: f"{int(x):,}명")


st.dataframe(
    audience_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------------
# 하단 안내
# -----------------------------------
st.markdown(
    """
    <div style="
        text-align:center;
        color:#686875;
        font-size:12px;
        margin-top:40px;
        padding-top:20px;
        border-top:1px solid rgba(255,255,255,0.07);
    ">
        🎬 KOBIS 영화관입장권통합전산망 데이터를 활용한 영화 매출 대시보드
    </div>
    """,
    unsafe_allow_html=True
)
