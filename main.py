import streamlit as st
import os
from chat_manager import ChatManager
from llm_client import LLMClient
from i18n_utils import I18nManager
from ui_components import render_message, render_sidebar, show_notification
from config import Config

# Page configuration
st.set_page_config(
    page_title="MyChatMe",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "MyChatMe - Multilingual AI Chat Application"
    }
)

# Initialize session state
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()
if "llm_client" not in st.session_state:
    st.session_state.llm_client = LLMClient()
if "i18n" not in st.session_state:
    st.session_state.i18n = I18nManager()
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "test_mode" not in st.session_state:
    st.session_state.test_mode = False

# Main application
def main():
    i18n = st.session_state.i18n
    chat_manager = st.session_state.chat_manager
    llm_client = st.session_state.llm_client

    st.title(i18n.get_text("app_title"))

    # Check API keys
    if not Config.get_openai_key():
        show_notification(i18n.get_text("error_missing_key") + " (OpenAI)", "warning")
    if not Config.get_openrouter_key():
        show_notification(i18n.get_text("error_missing_key") + " (OpenRouter)", "warning")

    # Sidebar
    language, model = render_sidebar(i18n, chat_manager)

    # Add test mode toggle in sidebar for development
    with st.sidebar:
        st.markdown("---")
        st.write("開発者モード")
        test_mode = st.checkbox("エラーテストモードを有効にする", value=st.session_state.test_mode)
        if test_mode != st.session_state.test_mode:
            st.session_state.test_mode = test_mode
            llm_client.set_test_mode(test_mode)
            if test_mode:
                show_notification("エラーテストモードが有効になりました。\nエラーをテストするには以下のコマンドを入力してください：\n- test_error api_key\n- test_error rate_limit\n- test_error network", "info")
            else:
                show_notification("エラーテストモードが無効になりました。", "info")

    # Update language
    if language == "English" and i18n._current_language != "en":
        i18n.set_language("en")
        st.rerun()
    elif language == "日本語" and i18n._current_language != "ja":
        i18n.set_language("ja")
        st.rerun()

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

    # Display chat messages
    for message in chat_manager.get_messages(include_system=False):
        render_message(message["role"], message["content"])

    # Chat input
    if prompt := st.chat_input(i18n.get_text("chat_placeholder")):
        # Add user message
        chat_manager.add_message("user", prompt)
        render_message("user", prompt)

        try:
            # Get AI response based on selected model
            messages = chat_manager.get_messages()
            response = None

            # Model selection logic
            model_map = {
                "GPT-4": llm_client.chat_openai,
                "Gemini-2.0": llm_client.chat_gemini,
                "Claude-3.5": llm_client.chat_claude
            }

            if model in model_map:
                try:
                    response = model_map[model](messages)
                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg:
                        if model == "GPT-4":
                            show_notification(i18n.get_text("error_model_switch_openai"), "error")
                        else:
                            show_notification(i18n.get_text("error_model_switch_openrouter"), "error")
                    elif "rate" in error_msg.lower():
                        show_notification(i18n.get_text("error_rate_limit"), "warning")
                    elif "network" in error_msg.lower():
                        show_notification(i18n.get_text("error_network"), "error")
                    else:
                        show_notification(f"{i18n.get_text('error_model_switch')}: {error_msg}", "error")
                    return
            else:
                show_notification(f"Invalid model selection: {model}", "error")
                return

            if response:
                # Add AI response
                chat_manager.add_message("assistant", response)
                render_message("assistant", response)

                # Generate and update context summary periodically
                if len(chat_manager.current_session.messages) % 5 == 0:  # Every 5 messages
                    try:
                        summary = llm_client.generate_context_summary(chat_manager.current_session.messages)
                        chat_manager.update_context_summary(summary)
                    except Exception as e:
                        print(f"Failed to generate context summary: {str(e)}")

            # Keep sidebar expanded after chat
            st.session_state.sidebar_state = "expanded"
        except Exception as e:
            show_notification(f"{i18n.get_text('error_api_call')}: {str(e)}", "error")

    # Clear chat button
    if st.button(i18n.get_text("clear_chat")):
        chat_manager.clear_current_chat()
        st.rerun()

if __name__ == "__main__":
    main()