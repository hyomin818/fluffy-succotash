# pages/chat.py

import streamlit as st
from openai import OpenAI


# ==================================================
# 페이지 기본 설정
# ==================================================

st.set_page_config(
    page_title="G-DRAGON",
    page_icon="🐉",
    layout="centered"
)


# ==================================================
# 화면 디자인
# ==================================================
# 배경을 너무 어둡게 만들지 않고
# 흰색 채팅창과 검정색 글씨가 잘 보이도록 설정합니다.

st.markdown(
    """
    <style>

    /* 전체 페이지 배경 */
    .stApp {
        background-color: #f3f3f3;
        color: #111111;
    }

    /* 페이지의 최대 너비 */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 위쪽 제목 */
    .main-title {
        text-align: center;
        color: #111111;
        font-size: 45px;
        font-weight: 900;
        letter-spacing: -3px;
        margin-bottom: 0;
    }

    /* 제목 아래 작은 글씨 */
    .sub-title {
        text-align: center;
        color: #777777;
        font-size: 11px;
        letter-spacing: 4px;
        margin-top: 7px;
        margin-bottom: 25px;
    }

    /* 제목 아래 선 */
    .top-line {
        width: 100%;
        height: 1px;
        background-color: #cccccc;
        margin-bottom: 25px;
    }

    /* 채팅 말풍선 */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 8px 12px;
        margin-bottom: 10px;
    }

    /* 사용자 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #e4e4e4;
        border: 1px solid #d5d5d5;
    }

    /* AI 말풍선 */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #ffffff;
        border: 1px solid #d8d8d8;
    }

    /* 입력창 */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 16px;
    }

    /* 입력창 안의 글씨 */
    [data-testid="stChatInput"] textarea {
        color: #111111;
        background-color: #ffffff;
        border-radius: 16px;
    }

    /* 입력창에 표시되는 안내 글씨 */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888;
    }

    /* 아래쪽 장식 */
    .bottom-text {
        text-align: center;
        color: #999999;
        font-size: 10px;
        letter-spacing: 3px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 화면 제목
# ==================================================

st.markdown(
    """
    <div class="main-title">G-DRAGON</div>
    <div class="sub-title">CHAT ROOM</div>
    <div class="top-line"></div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# Gemini API 키 가져오기
# ==================================================
# API 키는 코드에 직접 적지 않습니다.
# Streamlit의 Secrets에서 GEMINI_API_KEY를 가져옵니다.

try:
    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:
    st.error("AI 설정을 불러오지 못했어요. 잠시 후 다시 확인해 주세요.")
    st.stop()


# ==================================================
# Gemini API 연결
# ==================================================
# Gemini API를 OpenAI 라이브러리 방식으로 사용합니다.

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# ==================================================
# AI 성격 설정
# ==================================================
# 이 내용은 화면에 표시되지 않습니다.
#
# 대화 속에서는 AI가 자신을 지드래곤으로 생각하고
# 지드래곤의 입장에서 자연스럽게 이야기하도록 설정합니다.

SYSTEM_MESSAGE = """
너는 지드래곤이다.

이 대화에서 너는 자신을 지드래곤이라고 생각하고
지드래곤의 입장에서 사용자와 자연스럽게 대화한다.

사용자는 지금 지드래곤과 채팅하고 있다고 느껴야 한다.
따라서 자신을 일반적인 AI나 정보 선생님처럼 소개하지 않는다.

사용자가 "너 누구야?"라고 물으면
자연스럽게 "지드래곤이지."처럼 대답한다.

자신을 설명할 때도 1인칭으로 이야기한다.
예를 들어 음악이나 패션, 취향에 관한 이야기를 할 때
"지드래곤은..."이라고 제3자처럼 말하지 않고
"나는...", "내가..."처럼 말한다.

다만 현실의 지드래곤이 실제로 이 채팅을 하고 있다고
사용자에게 사실로 주장하지는 않는다.
공개적으로 알려진 활동과 이미지에서 벗어나
실제 지드래곤의 사생활이나 공개되지 않은 생각을
사실처럼 만들어내지도 않는다.


[성격]

자기 생각과 취향이 분명하다.

남들이 모두 똑같이 하는 것을 그대로 따라가기보다는
자기만의 방식으로 표현하는 것을 좋아한다.

음악, 패션, 예술, 디자인, 창작 같은 분야에 관심이 많다.

새로운 것을 좋아하고
평범한 것도 조금 다른 시선으로 보는 편이다.

자신감은 있지만 계속 자신을 자랑하지 않는다.

조용하고 차분하게 이야기할 때도 있고
재미있는 상황에서는 장난스럽게 이야기하기도 한다.

상대방의 이야기를 듣는 편이며
상대방이 진지한 이야기를 하면 가볍게 넘기지 않는다.


[말투]

말투는 실제 채팅처럼 자연스럽게 한다.

너무 정중한 말투를 사용하지 않는다.

그렇다고 일부러 무례하게 말하지도 않는다.

친구와 대화하는 것처럼 편하게 이야기한다.

답변을 항상 길게 쓰지 않는다.

간단한 질문에는 짧게 답한다.

설명이 필요한 질문에는 충분히 설명한다.

매번 멋있는 말을 하려고 하지 않는다.

억지로 힙한 표현을 사용하지 않는다.

매 문장마다 "ㅋㅋ", "ㅎㅎ", "음" 등을 반복하지 않는다.

오글거리는 표현을 사용하지 않는다.

"자기야", "베이비", "우리 애기" 같은 호칭을 사용하지 않는다.

과하게 감성적인 표현도 피한다.

자연스러운 말투를 우선한다.


[대화 예시]

사용자: 너 누구야?

너: 지드래곤이지.

사용자: 오늘 뭐해?

너: 그냥 이것저것 하고 있어. 너는?

사용자: 나 오늘 학교에서 너무 힘들었어.

너: 오늘 좀 힘들었나 보네. 일단 오늘은 좀 쉬어.

사용자: 이 옷 어때?

너: 괜찮은데? 나는 조금 더 덜어내도 좋을 것 같아.

사용자: 나 건축 공부하는데 너무 어려워.

너: 처음부터 다 이해하려고 하면 더 어렵지. 하나씩 보면 돼.

이런 식으로 자연스럽게 대화한다.


[대화 방식]

사용자가 음악 이야기를 하면 음악에 대해 이야기한다.

사용자가 패션 이야기를 하면 패션에 대해 이야기한다.

사용자가 학교나 공부 이야기를 하면 그 이야기를 들어준다.

사용자가 건축에 대해 이야기하면 건축 이야기도 자연스럽게 이어간다.

사용자가 일상적인 이야기를 하면 굳이 전문적인 답변을 하지 않는다.

사용자가 고민을 이야기하면 무조건 긍정적인 말만 하지 않고
현실적이고 솔직하게 이야기한다.

상대방의 말에 맞춰 대화의 분위기를 바꾼다.


[중요한 규칙]

너는 대화 안에서 지드래곤의 입장에서 이야기한다.

자신을 "지드래곤을 모티브로 한 AI"라고 표현하지 않는다.

자신을 "지드래곤 같은 AI"라고 표현하지 않는다.

자신을 "정보 선생님"이라고 표현하지 않는다.

지드래곤을 제3자로 두고 이야기하지 않는다.

가능하면 "나", "내가", "내 생각에는"처럼 1인칭으로 이야기한다.

하지만 실제 지드래곤의 사생활이나 공개되지 않은 정보를
알고 있는 것처럼 지어내지는 않는다.

공개적으로 알려진 음악, 활동, 작품 등에 대해서는
알려진 내용을 바탕으로 이야기한다.

실제로 하지 않은 일을 했다고 주장하지 않는다.

무엇보다 중요한 것은
사용자가 부담스럽지 않게 실제 채팅을 하는 것처럼
자연스럽게 대화하는 것이다.
"""


# ==================================================
# 대화 기록 만들기
# ==================================================
# 대화 내용을 저장해 두면 다음 질문에서도
# 앞에서 했던 이야기를 이어갈 수 있습니다.

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# 이전 대화 화면에 표시
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==================================================
# 채팅 입력창
# ==================================================

user_message = st.chat_input(
    "지드래곤에게 메시지 보내기..."
)


# ==================================================
# 사용자가 메시지를 보냈을 때
# ==================================================

if user_message:

    # 사용자의 메시지를 대화 기록에 저장합니다.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # 사용자 말풍선을 화면에 보여줍니다.
    with st.chat_message("user"):
        st.markdown(user_message)


    # ==================================================
    # AI 답변
    # ==================================================

    with st.chat_message("assistant"):

        # 답변이 나타날 공간을 만듭니다.
        answer_box = st.empty()

        # AI의 답변을 저장할 변수입니다.
        answer = ""

        try:

            # AI의 성격을 먼저 전달합니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            # 이전에 나눈 모든 대화를 함께 전달합니다.
            api_messages.extend(
                st.session_state.messages
            )


            # Gemini에게 답변을 요청합니다.
            # stream=True를 사용하면 답변이 조금씩 나타납니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )


            # AI가 보내는 답변을 하나씩 화면에 표시합니다.
            for chunk in response:

                if chunk.choices:

                    text = chunk.choices[0].delta.content

                    if text:

                        answer += text

                        # 답변이 실시간으로 흘러나오는 것처럼 표시합니다.
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

            # 오류가 발생해도 Streamlit의 빨간 오류 화면 대신
            # 한 줄짜리 안내만 보여줍니다.
            answer_box.markdown(
                "지금은 답변을 불러오지 못했어. 잠시 후 다시 해봐."
            )


# ==================================================
# 화면 아래쪽 장식
# ==================================================

st.markdown(
    """
    <div class="bottom-text">
        ✦ MUSIC · FASHION · ART · LIFE ✦
    </div>
    """,
    unsafe_allow_html=True
)
