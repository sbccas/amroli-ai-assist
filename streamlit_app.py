import streamlit as st
import pandas as pd
from openai import OpenAI
import base64
import os
st.set_page_config(
    page_title="Amroli AI",
    page_icon="💬",
    layout="centered"
)
# Load logo (optional but makes it polished)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = "logo.png"  # Update path if needed
if logo_path and os.path.exists(logo_path):
    logo_base64 = get_base64_image(logo_path)
    st.markdown(f"<img src='data:image/png;base64,{logo_base64}' width='80' style='margin-bottom: 10px;'>", unsafe_allow_html=True)


# Show title and description.
st.title("Amroli AI Assistant 💬")
st.write("Welcome to AmroliAI, Your Smart Campus Companion. The official AI-powered chatbot of Amroli SFI College!")
st.write("Instantly get answers about admissions, courses, events, faculty, campus facilities, and more — all in a friendly, interactive way."
         " Whether you're a student, parent, or visitor, AmroliAI is here 24/7 to guide you with accurate and up-to-date information about our institution."
)

# Create an OpenAI client.
client = OpenAI(api_key=st.secrets["Openkey"])

# --- NEW: Load CSV data into a DataFrame
@st.cache_data
def load_data():
    df = pd.read_csv("allinone_cleaned.csv")  # Make sure the CSV file is present
    return df

df = load_data()

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's your query?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- NEW: Try to find matching info from CSV
    def find_relevant_info(query):
        query_lower = query.lower()
        matching_rows = df[df.apply(lambda row: query_lower in row.astype(str).str.lower().to_string(), axis=1)]
        if not matching_rows.empty:
            return matching_rows.to_string(index=False)
        else:
            return "No direct information found in our records."

    relevant_info = find_relevant_info(prompt)

    # Generate a response using OpenAI API with context from CSV
    full_prompt = f"""
You are AmroliAI, an assistant for Amroli SFI College.
Use the following information extracted from college records to answer the user's question as accurately as possible.

Information from database:
{relevant_info}

Question: {prompt}

Answer:"""

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        stream=True,
    )

    # Stream the response to the chat
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
