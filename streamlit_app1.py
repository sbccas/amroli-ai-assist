import streamlit as st
import pandas as pd
from openai import OpenAI

# Load your CSV (or Google Sheet as DataFrame)
df = pd.read_csv('allinone.csv')  # or load Google Sheet data into df
# Show title and description.
st.title("💬 AmroliAI ✨")
st.write("Welcome to AmroliAI,Your Smart Campus Companion. The official AI-powered chatbot of Amroli SFI College!")
st.write("Instantly get answers about admissions, courses, events, faculty, campus facilities, and more — all in a friendly, interactive way."
"Whether you're a student, parent, or visitor, AmroliAI is here 24/7 to guide you with accurate and up-to-date information about our institution."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Create an OpenAI client.
client = OpenAI(api_key=st.secrets["Openkey"])

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Whats your Query?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
