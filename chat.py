# pages/chat.py

import streamlit as st
from openai import OpenAI


# 페이지 기본 설정
st.set_page_config(
    page_title="AI 채팅",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI 채팅")
st.caption("궁금한 내용을 편하게 질문해 보세요.")


# 비밀 금고에서 Gemini API 키를 가져옵니다.
# 실제 API 키를 코드에 직접 적지 않습니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("AI 설정을 불러오지 못했습니다. 관리자에게 문의해 주세요.")
    st.stop()


# Gemini API를 OpenAI 라이브러리 방식으로 연결합니다.
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# AI에게 항상 적용할 성격과 답변 방식을 설정합니다.
# 이 내용은 사용자 화면에는 표시되지 않습니다.
SYSTEM_MESSAGE = """
너는 중고등학생에게 설명하는 친절한 정보 선생님이야.
어려운 말은 쉬운 말로 바꿔 주고, 반드시 순수 한국어로만 답해.
"""


# 대화 내용을 저장합니다.
# 이렇게 저장해 두면 이전 질문과 답변을 다음 질문에도 함께 전달할 수 있습니다.
if "messages" not in st.session_state:
    st.session_state.messages = []


# 지금까지의 대화 내용을 화면에 보여줍니다.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자가 채팅 입력창에 메시지를 입력합니다.
user_message = st.chat_input("메시지를 입력하세요...")


if user_message:
    # 사용자가 입력한 내용을 대화 기록에 저장합니다.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # 사용자의 메시지를 바로 화면에 보여줍니다.
    with st.chat_message("user"):
        st.markdown(user_message)

    # AI의 답변이 표시될 공간을 미리 만듭니다.
    with st.chat_message("assistant"):
        answer_box = st.empty()
        answer = ""

        try:
            # AI에게 이전 대화 전체를 함께 전달합니다.
            # 가장 앞에는 AI의 성격을 알려주는 안내를 넣습니다.
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            api_messages.extend(st.session_state.messages)

            # 스트리밍 방식으로 답변을 요청합니다.
            # 답변이 완성될 때까지 기다리지 않고 글자가 조금씩 나타납니다.
            response = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=api_messages,
                stream=True
            )

            # AI가 보내주는 글자를 하나씩 이어 붙입니다.
            for chunk in response:
                if chunk.choices:
                    text = chunk.choices[0].delta.content

                    if text:
                        answer += text
                        answer_box.markdown(answer + "▌")

            # 마지막에는 커서를 제거하고 완성된 답변만 보여줍니다.
            answer_box.markdown(answer)

            # 완성된 AI 답변도 대화 기록에 저장합니다.
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception:
            # API 오류가 발생해도 긴 오류 화면 대신 안내 문구만 보여줍니다.
            answer_box.markdown(
                "AI와 연결하는 중 문제가 발생했어요. 잠시 후 다시 시도해 주세요."
            )
