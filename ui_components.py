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
                    st.success(f"{i18n.get_text('export_success')} ({filename})")
                else:
                    # PDF export will be implemented later
                    st.info("PDF export coming soon!")
            except Exception as e:
                st.error(f"{i18n.get_text('export_error')}: {str(e)}")

        return language, model