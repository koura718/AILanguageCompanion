import streamlit as st
from datetime import datetime
import pytz
from config import Config

def render_message(role: str, content: str, timezone: str = Config.DEFAULT_TIMEZONE):
    """タイムゾーンを考慮してメッセージを表示"""
    if role == "assistant":
        with st.chat_message(role, avatar="🤖"):
            st.write(content)
    elif role == "user":
        with st.chat_message(role, avatar="👤"):
            st.write(content)
    else:
        with st.chat_message(role):
            st.write(content)

def show_notification(message: str, type: str = "info", duration: int = 3):
    """Show an elegant notification toast."""
    if type == "error":
        st.error(message, icon="🚨")
    elif type == "success":
        st.success(message, icon="✅")
    elif type == "warning":
        st.warning(message, icon="⚠️")
    else:
        st.info(message, icon="ℹ️")

def render_sidebar(i18n, chat_manager):
    # Create a persistent sidebar container
    sidebar = st.sidebar

    # Ensure sidebar is visible
    if "sidebar_visibility" not in st.session_state:
        st.session_state.sidebar_visibility = True

    # Initialize states
    if "timezone" not in st.session_state:
        st.session_state.timezone = Config.DEFAULT_TIMEZONE
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "light"

    with sidebar:
        st.title(i18n.get_text("settings"))

        # Theme selection
        theme_mode = st.selectbox(
            i18n.get_text("theme_mode"),
            ["Light", "Dark"],
            index=0 if st.session_state.theme_mode == "light" else 1,
            key="theme_selector"
        )

        # Update theme mode if changed
        if theme_mode == "Dark" and st.session_state.theme_mode != "dark":
            st.session_state.theme_mode = "dark"
            st.query_params["theme"] = "dark"
        elif theme_mode == "Light" and st.session_state.theme_mode != "light":
            st.session_state.theme_mode = "light"
            st.query_params["theme"] = "light"

        # Language selection - デフォルトを日本語に設定
        language = st.selectbox(
            i18n.get_text("language"),
            ["English", "日本語"],
            index=1,
            key="language_selector"
        )

        # Model selection - デフォルトをGemini-2.0に設定
        model = st.selectbox(
            i18n.get_text("model_selection"),
            ["GPT-4", "Gemini-2.0", "Claude-3.5"],
            index=1,
            key="model_selection"
        )

        # Timezone selection
        timezone = st.selectbox(
            i18n.get_text("timezone"),
            Config.SUPPORTED_TIMEZONES,
            index=Config.SUPPORTED_TIMEZONES.index(Config.DEFAULT_TIMEZONE),
            key="timezone_selector"
        )
        st.session_state.timezone = timezone

        st.markdown("---")

        # Export section
        export_format = st.selectbox(
            i18n.get_text("export_format"),
            ["Markdown", "PDF"],
            key="export_format"
        )

        if st.button(i18n.get_text("export_chat"), key="export_button"):
            try:
                timezone = st.session_state.get("timezone", Config.DEFAULT_TIMEZONE)
                if export_format == "Markdown":
                    filename = chat_manager.save_markdown_file(timezone=timezone)
                    show_notification(f"{i18n.get_text('export_success')} ({filename})", "success")
                else:
                    filename = chat_manager.export_chat_pdf(timezone=timezone)
                    show_notification(f"{i18n.get_text('export_success')} ({filename})", "success")
            except Exception as e:
                show_notification(f"{i18n.get_text('export_error')}: {str(e)}", "error")

        return language, model