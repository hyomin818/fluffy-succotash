# pages/chat.py

import streamlit as st
from openai import OpenAI


# --------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="G-Chat",
    page_icon="✦",
    layout="centered"
)


# --------------------------------------------------
# 화면 전체 디자인
# --------------------------------------------------
# 검정색을 기본으로 하고 흰색 글씨와 큰 글자를 사용해서
# 패션 매거진 같은 분위기를 만듭니다.

st.markdown(
    """
    <style>

    /* 전체 페이지 배경 */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(255,255,255,0.12) 0%,
                rgba(255,255,255,0) 25%
            ),
            radial-gradient(
                circle at 85% 80%,
                rgba(255,255,255,0.08) 0%,
                rgba(255,255,255,0) 30%
            ),
            linear-gradient(
                135deg,
                #050505 0%,
                #111111 45%,
                #000000 100%
            );

        color: white;
    }


    /* 페이지 위쪽 여백 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 850px;
    }


    /* 위쪽 로고 */
    .gd-logo {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        letter-spacing: -5px;
        color: white;
        margin-bottom: 0px;
        line-height: 1;
    }


    /* 로고 아래 작은 글씨 */
    .gd-subtitle {
        text-align: center;
        color: #999999;
        font-size: 12px;
        letter-spacing: 5px;
        margin-top: 10px;
        margin-bottom: 30px;
    }


    /* 장식용 선 */
    .line {
        width: 100%;
        height: 1px;
        background: #444444;
        margin: 20px 0 30px 0;
    }


    /* 채팅 말풍선 */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 5px;
    }


    /* 사용자 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
    }


    /* AI 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
    }


    /* 입력창 */
    [data-testid="stChatInput"] {
        border-radius: 18px;
    }


    /* 입력창 안쪽 */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(255,255,255,0.08);
        color: white;
        border-radius: 18px;
    }


    /* 아래쪽 장식 문구 */
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


# --------------------------------------------------
# 화면 위쪽 제목
# --------------------------------------------------

st.markdown(
    """
    <div class="gd-logo">G</div>
    <div class="gd-subtitle">KEEP IT SIMPLE · KEEP IT YOURS</div>
    <div class="line"></div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Gemini API 설정
# --------------------------------------------------
# API 키는 코드에 직접 적지 않고 Streamlit의
# 비밀 금고에서 가져옵니다.

try:
    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    st.error("AI 설정을 불러오지 못했어요. 잠시 후 다시 확인해 주세요.")
    st.stop()


# --------------------------------------------------
# Gemini API 연결
# --------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# --------------------------------------------------
# AI 성격 설정
# --------------------------------------------------
# 이 내용은 화면에 표시되지 않습니다.
#
# 특정 인물의 실제 말투를 그대로 복사하지 않고,
# 자유롭고 차분한 분위기를 중심으로 설정합니다.

SYSTEM_MESSAGE = """
너는 자유롭고 개성 있는 분위기의 대화형 AI야.

말투는 차분하고 자연스럽게 해.
억지로 멋있는 말을 하거나 오글거리는 표현을 사용하지 마.
너무 과하게 친한 척하지도 마.

짧게 답해도 되는 질문에는 간결하게 답하고,
설명이 필요한 질문에는 이해하기 쉽게 설명해.

가끔 센스 있고 재치 있는 표현을 사용할 수 있지만
억지로 유행어를 사용하지 마.

상대방의 말에 맞춰 자연스럽게 대화하고,
진지한 이야기는 가볍게 넘기지 마.

모르는 내용은 아는 척하지 말고 솔직하게 말해.

실제 특정 유명인이라고 주장하거나
특정 유명인의 실제 말투를 그대로 따라 하지는 마.
"""


# --------------------------------------------------
# 대화 기록 만들기
# --------------------------------------------------
# session_state에 대화를 저장하면
# 사용자가 다음 질문을 했을 때 이전 대화를 함께 보낼 수 있습니다.

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# 이전 대화 화면에 표시
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# 채팅 입력창
# --------------------------------------------------

user_message = st.chat_input(
    "무슨 얘기든 해봐..."
)


# --------------------------------------------------
# 사용자가 메시지를 보냈을 때
# --------------------------------------------------

if user_message:

    # 사용자의 메시지를 대화 기록에 저장합니다.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # 사용자 메시지를 말풍선으로 표시합니다.
    with st.chat_message("user"):

        st.markdown(user_message)


    # --------------------------------------------------
    # AI 답변
    # --------------------------------------------------

    with st.chat_message("assistant"):

        # 답변을 실시간으로 표시할 공간입니다.
        answer_box = st.empty()

        # AI가 보내는 답변을 하나씩 이어 붙입니다.
        answer = ""


        try:

            # AI의 성격을 먼저 전달합니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]


            # 지금까지의 모든 대화를 함께 전달합니다.
            # 그래서 AI가 앞에서 나눈 이야기를 기억하고 이어서 답합니다.
            api_messages.extend(
                st.session_state.messages
            )


            # Gemini API에 답변을 요청합니다.
            # stream=True를 사용해서 답변을 실시간으로 받습니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )


            # 답변을 한 부분씩 받아서 화면에 보여줍니다.
            for chunk in response:

                if chunk.choices:

                    text = chunk.choices[0].delta.content

                    if text:

                        answer += text

                        # 답변이 입력되는 것처럼 보여줍니다.
                        answer_box.markdown(
                            answer + "▌"
                        )


            # 답변이 끝나면 커서를 제거합니다.
            answer_box.markdown(answer)


            # 완성된 답변을 대화 기록에 저장합니다.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception:

            # 오류가 발생해도 Streamlit의 빨간 오류 화면을
            # 사용자에게 그대로 보여주지 않습니다.
            answer_box.markdown(
                "지금은 답변을 불러오지 못했어. 잠시 후 다시 해봐."
            )


# --------------------------------------------------
# 화면 아래쪽 장식
# --------------------------------------------------

st.markdown(
    """
    <div class="bottom-text">
        ✦ NO RULES · JUST TALK ✦
    </div>
    """,
    unsafe_allow_html=True
)
