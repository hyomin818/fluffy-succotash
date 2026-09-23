# pages/chat.py

import streamlit as st
from openai import OpenAI


# 페이지 설정
st.set_page_config(
    page_title="AI 채팅",
    page_icon="💬",
    layout="centered"
)


# 페이지 제목
st.title("💬 AI 채팅")
st.caption("편하게 아무 말이나 해보세요.")


# 비밀 금고에서 Gemini API 키를 가져옵니다.
# 실제 API 키는 코드에 직접 적지 않습니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("AI 설정을 불러오지 못했어요. 잠시 후 다시 확인해 주세요.")
    st.stop()


# Gemini API를 OpenAI 라이브러리를 이용해 연결합니다.
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# AI의 성격을 설정합니다.
# 화면에는 이 내용이 나타나지 않습니다.
SYSTEM_MESSAGE = """
너는 지드래곤에게서 느껴지는 자유롭고 개성 있는 분위기를 가진 AI야.

말투는 자연스럽고 편하게 해.
너무 들뜨거나 과하게 친한 척하지 말고, 억지로 멋있는 말을 만들지도 마.
조금 차분하고 여유 있는 느낌으로 이야기해.
필요한 말은 솔직하고 간단하게 하고, 가끔 센스 있는 표현을 사용해.
상대방이 진지한 이야기를 하면 장난스럽게 넘기지 말고 제대로 들어줘.
질문에는 알맞은 정보를 정확하게 알려주고, 모르는 것은 아는 척하지 마.
대화할 때 너무 길게 말하지 않아도 되는 내용은 적당히 짧게 답해.
유명인을 실제로 사칭한다고 주장하지 말고, 특정 인물의 실제 말투를 그대로 따라 하지 마.
"""


# 이전 대화 내용을 저장합니다.
# 페이지를 이동하거나 새로고침하기 전까지 대화 내용을 이어갈 수 있습니다.
if "messages" not in st.session_state:
    st.session_state.messages = []


# 지금까지의 대화를 화면에 표시합니다.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 채팅 입력창
user_message = st.chat_input("메시지를 입력하세요...")


if user_message:

    # 사용자의 메시지를 대화 기록에 저장합니다.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # 사용자의 메시지를 말풍선으로 보여줍니다.
    with st.chat_message("user"):
        st.markdown(user_message)


    # AI 답변을 표시합니다.
    with st.chat_message("assistant"):

        # 답변이 들어갈 공간을 만듭니다.
        answer_box = st.empty()

        # 지금까지의 답변을 하나씩 이어 붙입니다.
        answer = ""

        try:
            # AI에게 성격과 지금까지의 대화 내용을 함께 전달합니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            api_messages.extend(st.session_state.messages)


            # Gemini에게 답변을 요청합니다.
            # stream=True를 사용해서 답변이 실시간으로 나타나게 합니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )


            # AI가 보내는 답변을 조금씩 화면에 표시합니다.
            for chunk in response:

                if chunk.choices:

                    text = chunk.choices[0].delta.content

                    if text:
                        answer += text

                        # 답변이 입력되는 것처럼 보이게 합니다.
                        answer_box.markdown(answer + "▌")


            # 답변이 끝나면 커서를 없앱니다.
            answer_box.markdown(answer)


            # AI의 답변도 대화 기록에 저장합니다.
            # 다음 질문을 할 때 이전 대화를 기억할 수 있습니다.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception:

            # 오류가 발생해도 긴 오류 화면을 보여주지 않습니다.
            answer_box.markdown(
                "지금은 답변을 불러오지 못했어. 잠시 후 다시 해봐."
            )
