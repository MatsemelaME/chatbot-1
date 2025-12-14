import streamlit as st
from openai import OpenAI

# ------------------------------
# App title and description
# ------------------------------
st.title("💬 Let's Talk")

st.write(
    "This is a simple chatbot that uses OpenAI to generate responses.\n\n"
    "You can choose a language, type your question, and click **Send Request**.\n\n"
    "After receiving an answer, you can click **Explain further** to get more details."
)

# ------------------------------
# Language selection
# ------------------------------
language = st.selectbox(
    "Choose response language:",
    ["English", "Afrikaans", "Xitsonga", "Sesotho", "Zulu"]
)

# ------------------------------
# API Key input
# ------------------------------
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=openai_api_key)

# ------------------------------
# Session state
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_user_prompt" not in st.session_state:
    st.session_state.last_user_prompt = ""

# ------------------------------
# Display chat history
# ------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------
# User input
# ------------------------------
user_input = st.text_area("Type your message here:")

# ------------------------------
# Send Request button
# ------------------------------
if st.button("📨 Send Request") and user_input.strip() != "":
    prompt_with_language = (
        f"Please respond in {language}.\n\n"
        f"User question: {user_input}"
    )

    st.session_state.last_user_prompt = user_input

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant responding in {language}."},
            *st.session_state.messages
        ]
    )

    assistant_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# ------------------------------
# Explain further button
# ------------------------------
if st.session_state.last_user_prompt:
    if st.button("🔍 Explain further"):
        follow_up_prompt = (
            f"Please explain the following answer in more detail and in {language}."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant responding in {language}."},
                *st.session_state.messages,
                {"role": "user", "content": follow_up_prompt}
            ]
        )

        explanation = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(explanation)

        st.session_state.messages.append(
            {"role": "assistant", "content": explanation}
        )
