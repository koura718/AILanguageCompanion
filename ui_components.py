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

    with sidebar:
        st.title(i18n.get_text("settings"))

        # Language selection
        language = st.selectbox(
            i18n.get_text("language"),
            ["English", "日本語"],
            index=0 if i18n._current_language == "en" else 1,
            key="language_selector"
        )

        # Model selection
        model = st.selectbox(
            i18n.get_text("model_selection"),
            ["GPT-4", "Gemini-2.0", "Claude-3.5"],
            key="model_selection"
        )

        st.markdown("---")

        # Export section
        export_format = st.selectbox(
            i18n.get_text("export_format"),
            ["Markdown", "PDF"],
            key="export_format"
        )

        if st.button(i18n.get_text("export_chat"), key="export_button"):
            try:
                if export_format == "Markdown":
                    filename = chat_manager.save_markdown_file()
                    show_notification(f"{i18n.get_text('export_success')} ({filename})", "success")
                else:
                    # PDF export will be implemented later
                    show_notification("PDF export coming soon!", "info")
            except Exception as e:
                show_notification(f"{i18n.get_text('export_error')}: {str(e)}", "error")

        return language, model