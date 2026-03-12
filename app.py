import os
import json
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")
st.title("AI Chatbot Using Streamlit and Groq API")
st.caption("A simple multi-turn chatbot with model selection and persistent chat history")

CHAT_LOG_FILE = "chat_logs.json"
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."


# -----------------------------
# Helpers
# -----------------------------
def load_chat_history():
    if os.path.exists(CHAT_LOG_FILE):
        try:
            with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_chat_history(messages):
    try:
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.warning(f"Could not save chat history: {e}")


def fetch_models(api_key):
    if not api_key:
        return []

    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    excluded_keywords = [
        "guard",
        "safeguard",
        "moderation",
        "classifier",
        "classification",
        "whisper",
        "tts",
        "speech",
        "transcribe",
        "vision",
        "audio",
    ]

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        model_ids = [m["id"] for m in data.get("data", [])]
        filtered = [
            mid for mid in model_ids
            if not any(keyword in mid.lower() for keyword in excluded_keywords)
        ]

        return sorted(filtered)

    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Failed to fetch models: {e}")
        return []
    except Exception as e:
        st.sidebar.error(f"Unexpected error while fetching models: {e}")
        return []


def append_log(role, content):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_chat_history(st.session_state.messages)


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()


# -----------------------------
# Sidebar
# -----------------------------
api_key_env = os.getenv("GROQ_API_KEY", "")

with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input(
        "Groq API Key",
        value=api_key_env,
        type="password",
        help="Enter your Groq API key",
    )

    available_models = fetch_models(api_key)

    if not available_models:
        st.warning("No compatible chat models found. Check your API key.")
        model = None
    else:
        model = st.selectbox(
            "Select Model",
            options=available_models,
            help="Select a chat-capable model",
        )

    show_system_prompt = st.checkbox("Show system prompt", value=True)

    system_prompt = st.text_area(
        "System Prompt",
        value=DEFAULT_SYSTEM_PROMPT,
        disabled=not show_system_prompt
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Controls randomness",
    )

    top_p = st.slider(
        "Top P",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Controls diversity via nucleus sampling",
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=64,
        max_value=2048,
        value=512,
        step=64,
        help="Maximum number of tokens in the response",
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        save_chat_history(st.session_state.messages)
        st.rerun()


# -----------------------------
# Render old messages
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Chat input
# -----------------------------
user_message = st.chat_input("Ask me anything:")

if user_message:
    if not api_key:
        st.error("Please enter your Groq API key.")
    elif not model:
        st.error("Please select a compatible chat model.")
    else:
        append_log("user", user_message)

        with st.chat_message("user"):
            st.markdown(user_message)

        try:
            client = Groq(api_key=api_key)

            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend(
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ["user", "assistant"]
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chat = client.chat.completions.create(
                        model=model,
                        messages=api_messages,
                        temperature=temperature,
                        top_p=top_p,
                        max_tokens=max_tokens,
                    )

                    response_message = chat.choices[0].message.content or ""
                    st.markdown(response_message)

            append_log("assistant", response_message)

        except Exception as e:
            st.error(f"Groq API error: {e}")
