import streamlit as st
import requests

st.set_page_config(page_title="AI Teaching Assistant", page_icon="🎓", layout="wide")

API_URL = "http://localhost:8000/ask_assistant"  # Replace with your API if hosted

# --- Custom CSS for better readability ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .main {
        background-color: #F0F2F6;
        padding: 2rem;
    }

    .block-container {
        padding-top: 2rem !important;
    }

    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #ffffff;
        color: #000000;
    }

    .chat-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .stChatMessage {
        max-width: 100%;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.title("🎓 AI Teaching Assistant")
st.markdown("Ask your doubts about any video lecture!")

# --- Input Form ---
with st.form("ask_form"):
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("Student ID", placeholder="e.g. stu_123")
    with col2:
        video_title = st.text_input("Video Title", placeholder="e.g. Stack vs Queue")

    video_summary = st.text_area("Video Summary", placeholder="Paste the summary here...", height=200)
    student_question = st.text_input("Your Question", placeholder="e.g. Which one is used in browsers?")

    submit = st.form_submit_button("💬 Ask Assistant")

# --- API Integration ---
if submit:
    if not (student_id and video_title and video_summary and student_question):
        st.warning("⚠️ Please fill out all the fields.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={
                    "student_id": student_id,
                    "video_title": video_title,
                    "video_summary": video_summary,
                    "student_question": student_question
                })

                if response.status_code == 200:
                    data = response.json()

                    # Display chat-like interface
                    st.markdown("#### 💬 Chat Transcript")
                    st.chat_message("user").markdown(student_question)
                    st.chat_message("assistant").markdown(data["answer"])

                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"🚨 Internal Error: {str(e)}")
