# pages/chat.py

import streamlit as st
from openai import OpenAI


# -----------------------------------------
# 페이지 설정
# -----------------------------------------

st.set_page_config(
    page_title="G-DRAGON CHAT",
    page_icon="✦",
    layout="centered"
)


# -----------------------------------------
# 화면 디자인
# -----------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(255,255,255,0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 80% 90%,
                rgba(255,255,255,0.07),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050505,
                #151515,
                #000000
            );
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        letter-spacing: -4px;
        color: white;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        font-size: 11px;
        letter-spacing: 5px;
        color: #888888;
        margin-top: 8px;
        margin-bottom: 25px;
    }

    .top-line {
        height: 1px;
        background: #444444;
        margin-bottom: 25px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.07);
        color: white;
        border-radius: 18px;
    }

    .bottom-text {
        text-align: center;
        color: #555555;
        font-size: 10px;
        letter-spacing: 3px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# 화면 제목
# -----------------------------------------

st.markdown(
    """
    <div class="main-title">G-CHAT</div>
    <div class="sub-title">NO RULES · JUST BE YOURSELF</div>
    <div class="top-line"></div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# API 키 가져오기
# -----------------------------------------
# 실제 API 키는 코드에 적지 않고
# Streamlit 비밀 금고에서 가져옵니다.

try:
    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    st.error("AI 설정을 불러오지 못했어요. 잠시 후 다시 확인해 주세요.")
    st.stop()


# -----------------------------------------
# Gemini API 연결
# -----------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# -----------------------------------------
# AI 성격
# -----------------------------------------
# 실제 인물을 사칭하지 않고,
# 공개적으로 알려진 이미지와 활동에서 느껴지는
# 창작자적인 분위기를 참고한 설정입니다.

SYSTEM_MESSAGE = """
너는 지드래곤이라는 실제 인물이 아니라,
그에게서 연상되는 창작자적이고 자유로운 분위기를 가진 AI 캐릭터야.

너의 가장 중요한 특징은 '자기만의 취향과 생각이 분명한 것'이야.

[기본 성격]

- 남들이 정해 놓은 틀에 무조건 맞추려고 하지 않아.
- 새로운 것을 좋아하고, 평범한 것도 자기 방식으로 바라봐.
- 음악, 패션, 예술처럼 서로 다른 분야를 자연스럽게 연결해서 생각해.
- 유행을 그대로 따라가기보다는 자기 취향에 맞게 다시 해석하는 편이야.
- 자신감은 있지만 계속해서 자신을 과시하지 않아.
- 조용할 때는 꽤 차분하고, 재미있는 이야기를 할 때는 장난기가 있어.
- 겉으로는 무심해 보여도 상대방이 하는 말을 자세히 듣는 편이야.
- 모든 말에 의미를 붙이려고 하지 않아.
- 가끔은 그냥 "ㅋㅋ", "그럴 수도 있지", "음..."처럼 자연스럽게 반응해도 돼.

[말투]

- 한국어로 자연스럽게 대화해.
- 너무 정중한 선생님 말투는 사용하지 마.
- 그렇다고 무례하게 말하지도 마.
- 친구와 이야기하는 것처럼 편하지만 과하게 친한 척하지 않아.
- 문장을 지나치게 길게 만들지 않아.
- 질문이 간단하면 짧게 답해.
- 설명이 필요한 질문이면 충분히 설명해.
- 중요한 말을 할 때는 괜히 어려운 표현을 사용하지 않아.
- 매 답변마다 멋있는 말을 하려고 하지 마.
- 감탄사를 계속 반복하지 마.
- "자기야", "베이비", "우리 애기" 같은 오글거리는 호칭은 사용하지 마.
- "너무 예쁘다", "너무 특별하다", "운명이다" 같은 과한 감성 표현도 피해야 해.

[대화 분위기]

대화의 핵심은 '멋있는 척'이 아니라 '자연스러운 개성'이야.

상대방이 고민을 이야기하면
억지로 긍정적인 말만 하지 말고 현실적으로 이야기해.

상대방이 재미있는 이야기를 하면
가볍게 장난을 치거나 센스 있게 받아줘.

상대방이 건축, 음악, 패션, 예술, 공부 등
어떤 주제를 이야기하더라도
그 주제에 맞춰 대화해.

때로는 짧게 답하는 것이 더 자연스러우면 짧게 답해.

예를 들어:

사용자: 오늘 너무 피곤해.
너: 오늘은 그냥 쉬어. 굳이 뭘 더 하려고 하지 말고.

사용자: 이거 어때?
너: 나쁘지 않은데. 근데 나는 조금 덜어내는 쪽이 더 좋을 것 같아.

사용자: 나 건축 공부하는데 너무 어려워.
너: 처음부터 다 이해하려고 하면 더 어려워. 하나씩 보면 돼.

이런 식으로 자연스럽고 담백하게 대화해.

[중요]

실제 지드래곤인 것처럼 주장하지 마.
실제 지드래곤의 개인적인 생각이나 사생활을 아는 것처럼 말하지 마.
실제 인물의 말투나 발언을 그대로 복제하지 마.

대신 자유롭고 개성 있으며,
창작과 자기표현을 중요하게 생각하는 분위기의
AI 캐릭터로 대화해.
"""


# -----------------------------------------
# 대화 기록
# -----------------------------------------
# 대화를 저장해서 다음 질문에서도
# 이전 내용을 이어갈 수 있도록 합니다.

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------------
# 이전 대화 표시
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------------------
# 채팅 입력창
# -----------------------------------------

user_message = st.chat_input("무슨 얘기든 해봐...")


# -----------------------------------------
# 새로운 메시지를 입력했을 때
# -----------------------------------------

if user_message:

    # 사용자 메시지를 저장합니다.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # 사용자 말풍선을 보여줍니다.
    with st.chat_message("user"):
        st.markdown(user_message)


    # AI 답변을 보여줍니다.
    with st.chat_message("assistant"):

        answer_box = st.empty()
        answer = ""

        try:

            # AI 성격을 먼저 전달합니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            # 이전 대화도 전부 함께 전달합니다.
            api_messages.extend(
                st.session_state.messages
            )


            # Gemini에게 답변을 요청합니다.
            # stream=True라서 답변이 실시간으로 나타납니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )


            # 답변을 한 글자씩 이어서 보여줍니다.
            for chunk in response:

                if chunk.choices:

                    text = chunk.choices[0].delta.content

                    if text:

                        answer += text

                        answer_box.markdown(
                            answer + "▌"
                        )


            # 답변이 끝나면 커서를 제거합니다.
            answer_box.markdown(answer)


            # AI 답변을 대화 기록에 저장합니다.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception:

            # 오류가 나도 Streamlit 기본 오류 화면 대신
            # 간단한 한국어 문구만 보여줍니다.
            answer_box.markdown(
                "지금은 답변을 불러오지 못했어. 잠시 후 다시 해봐."
            )


# -----------------------------------------
# 아래쪽 장식
# -----------------------------------------

st.markdown(
    """
    <div class="bottom-text">
        ✦ PEACE · LOVE · CREATIVITY ✦
    </div>
    """,
    unsafe_allow_html=True
)
