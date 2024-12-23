import streamlit as st

def render_message(role: str, content: str):
    if role == "assistant":
        with st.chat_message(role, avatar="🤖"):
            st.write(content)
    elif role == "user":
        with st.chat_message(role, avatar="👤"):
            st.write(content)
    else:
        with st.chat_message(role):
            st.write(content)

def render_sidebar(i18n):
    with st.sidebar:
        st.title(i18n.get_text("settings"))
        
        # Language selection
        language = st.selectbox(
            i18n.get_text("language"),
            ["English", "日本語"],
            index=0 if i18n._current_language == "en" else 1
        )
        
        # Model selection
        model = st.selectbox(
            i18n.get_text("model_selection"),
            ["GPT-4", "Gemini-2.0"],
            key="model_selection"
        )
        
        # API Keys
        openai_key = st.text_input(
            i18n.get_text("api_key_openai"),
            type="password",
            key="openai_key"
        )
        openrouter_key = st.text_input(
            i18n.get_text("api_key_openrouter"),
            type="password",
            key="openrouter_key"
        )
        
        return language, model, openai_key, openrouter_key
