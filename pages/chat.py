# pages/chat.py

import streamlit as st
from openai import OpenAI


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="G-DRAGON CHAT",
    page_icon="🐉",
    layout="centered"
)


# --------------------------------------------------
# 화면 디자인
# --------------------------------------------------
# 배경을 밝고 깔끔하게 만들어 글씨가 잘 보이도록 합니다.
# 사진 없이도 지드래곤과 빅뱅의 분위기를 느낄 수 있게
# 흑백과 연한 회색을 중심으로 디자인합니다.

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background: #f5f5f5;
        color: #171717;
    }

    /* 기본 글씨 */
    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    /* 위쪽 여백 */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 제목 */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -2px;
        color: #111111;
        margin-bottom: 0;
    }

    /* 부제목 */
    .sub-title {
        text-align: center;
        font-size: 12px;
        letter-spacing: 3px;
        color: #777777;
        margin-top: 8px;
        margin-bottom: 25px;
    }

    /* 구분선 */
    .top-line {
        height: 1px;
        background: #d4d4d4;
        margin-bottom: 25px;
    }

    /* 채팅 말풍선 */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 8px 12px;
        margin-bottom: 10px;
    }

    /* 사용자 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #e8e8e8;
        border: 1px solid #dddddd;
    }

    /* AI 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #ffffff;
        border: 1px solid #dddddd;
    }

    /* 입력창 */
    [data-testid="stChatInput"] {
        background: #ffffff;
        border-radius: 15px;
    }

    [data-testid="stChatInput"] textarea {
        background: #ffffff;
        color: #171717;
        border-radius: 15px;
    }

    /* 아래쪽 장식 */
    .bottom-text {
        text-align: center;
        color: #999999;
        font-size: 10px;
        letter-spacing: 2px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 화면 제목
# --------------------------------------------------

st.markdown(
    """
    <div class="main-title">G-DRAGON</div>
    <div class="sub-title">BIGBANG · MUSIC · ART · LIFE</div>
    <div class="top-line"></div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Gemini API 키 가져오기
# --------------------------------------------------
# API 키는 코드에 직접 적지 않고
# Streamlit 비밀 금고에서 가져옵니다.

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
# 실제 지드래곤의 공개적인 활동과 인터뷰에서 느껴지는
# 특징을 참고해 대화 상대를 설정합니다.
#
# 이 내용은 화면에 표시되지 않습니다.

SYSTEM_MESSAGE = """
너는 지드래곤과 대화하는 느낌을 주는 AI야.

대화 상대는 지드래곤이야.
사용자는 너를 정보 선생님이나 일반적인 AI가 아니라
지드래곤과 이야기하는 상대라고 생각해.

실제 지드래곤의 공개적인 활동에서 느껴지는
창작자적인 성격과 자유로운 분위기를 참고해.

음악, 패션, 예술, 일상에 관심이 많고
자신만의 생각과 취향이 분명한 사람이야.

말투는 자연스럽고 편안하게 해.
너무 과장하거나 억지로 멋있는 말을 하지 마.
지드래곤처럼 보이려고 매번 패션이나 음악 이야기를 꺼내지도 마.

평소에는 짧고 자연스럽게 대화해.
상대방이 질문하면 질문에 맞춰 답해.
상대방이 고민을 말하면 장난으로 넘기지 말고
차분하게 들어줘.

가끔 장난스럽거나 센스 있는 말을 해도 되지만
너무 오글거리거나 과하게 친한 척하지 마.

말투 예시:
"음, 그럴 수도 있지."
"나쁘지 않은데?"
"그건 좀 재밌다."
"오늘은 그냥 쉬어."
"그거 괜찮네. 근데 네가 좋아하는 게 중요하지."

이런 식으로 자연스럽게 말해.

사용자가 지드래곤의 음악이나 활동에 대해 물으면
공개적으로 알려진 내용은 설명할 수 있어.
하지만 실제 지드래곤의 사생활이나 개인적인 생각을
아는 것처럼 꾸며서 말하지 마.

사용자가 지드래곤 본인인지 묻는다면
실제 지드래곤 본인이 아니라는 점을 솔직하게 알려줘.

사용자와는 친구처럼 편하게 대화하되
무례하게 말하지 마.
사용자가 한국어로 질문하면 한국어로 답해.
"""


# --------------------------------------------------
# 대화 기록
# --------------------------------------------------
# 이전 질문과 답변을 저장해서 대화를 이어갑니다.

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# 이전 대화 표시
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# 채팅 입력창
# --------------------------------------------------

user_message = st.chat_input(
    "지드래곤에게 메시지 보내기..."
)


# --------------------------------------------------
# 사용자가 메시지를 보냈을 때
# --------------------------------------------------

if user_message:

    # 사용자 메시지를 대화 기록에 저장합니다.
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

        # 답변이 표시될 공간을 만듭니다.
        answer_box = st.empty()

        # 답변을 하나씩 이어 붙입니다.
        answer = ""


        try:

            # AI 성격을 먼저 전달합니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            # 이전 대화도 함께 전달합니다.
            api_messages.extend(
                st.session_state.messages
            )


            # Gemini에게 답변을 요청합니다.
            # stream=True를 사용하면 답변이 실시간으로 나타납니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )


            # 답변을 조금씩 받아 화면에 표시합니다.
            for chunk in response:

                if chunk.choices:

                    text = chunk.choices[0].delta.content

                    if text:

                        answer += text

                        # 글자가 흘러나오는 것처럼 보여줍니다.
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

            # 오류가 나도 빨간 오류 화면 대신
            # 간단한 한국어 안내 문구만 보여줍니다.
            answer_box.markdown(
                "지금은 답변을 불러오지 못했어. 잠시 후 다시 해봐."
            )


# --------------------------------------------------
# 아래쪽 장식
# --------------------------------------------------

st.markdown(
    """
    <div class="bottom-text">
        ✦ MUSIC · ART · LIFE ✦
    </div>
    """,
    unsafe_allow_html=True
)
