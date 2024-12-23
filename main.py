import streamlit as st
import os
from chat_manager import ChatManager
from llm_client import LLMClient
from i18n_utils import I18nManager
from ui_components import render_message, render_sidebar, render_export_section

# Initialize session state
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()
if "llm_client" not in st.session_state:
    st.session_state.llm_client = LLMClient()
if "i18n" not in st.session_state:
    st.session_state.i18n = I18nManager()

# Main application
def main():
    i18n = st.session_state.i18n
    chat_manager = st.session_state.chat_manager
    llm_client = st.session_state.llm_client

    st.title(i18n.get_text("app_title"))

    # Sidebar
    language, model, openai_key, openrouter_key = render_sidebar(i18n, chat_manager)

    # Update language
    if language == "English" and i18n._current_language != "en":
        i18n.set_language("en")
        st.rerun()
    elif language == "日本語" and i18n._current_language != "ja":
        i18n.set_language("ja")
        st.rerun()

    # Update API keys
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key

    # System prompt
    system_prompt = st.text_area(
        i18n.get_text("system_prompt"),
        value=i18n.get_text("default_system_prompt"),
        key="system_prompt"
    )

    # Chat history selection
    if chat_manager.history:
        selected_chat = st.selectbox(
            i18n.get_text("chat_history"),
            ["New Chat"] + [f"Chat {session.created_at}" for session in chat_manager.history]
        )

        if selected_chat != "New Chat":
            chat_id = chat_manager.history[
                [f"Chat {session.created_at}" for session in chat_manager.history].index(selected_chat)
            ].id
            chat_manager.load_chat(chat_id)

    # Export section
    render_export_section(i18n, chat_manager)

    # Display chat messages
    for message in chat_manager.get_messages(include_system=False):
        render_message(message["role"], message["content"])

    # Chat input
    if prompt := st.chat_input(i18n.get_text("chat_placeholder")):
        # Add user message
        chat_manager.add_message("user", prompt)
        render_message("user", prompt)

        try:
            # Get AI response
            messages = chat_manager.get_messages()
            if model == "GPT-4":
                response = llm_client.chat_openai(messages)
            else:
                response = llm_client.chat_gemini(messages)

            # Add AI response
            chat_manager.add_message("assistant", response)
            render_message("assistant", response)
        except Exception as e:
            st.error(f"{i18n.get_text('error_api_call')}: {str(e)}")

    # Clear chat button
    if st.button(i18n.get_text("clear_chat")):
        chat_manager.clear_current_chat()
        st.rerun()

if __name__ == "__main__":
    main()