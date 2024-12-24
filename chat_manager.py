from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from config import Config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

@dataclass
class ChatSession:
    id: str
    messages: List[Dict[str, str]]
    system_prompt: str
    model: str
    created_at: str
    context_summary: Optional[str] = None
    context_messages: List[Dict[str, str]] = None

    def __post_init__(self):
        if self.context_messages is None:
            self.context_messages = []

class ChatManager:
    def __init__(self):
        self.current_session: ChatSession = self._create_new_session()
        self.history: List[ChatSession] = []
        self._setup_pdf_fonts()

    def _setup_pdf_fonts(self):
        """Set up CID fonts for PDF generation with Japanese support"""
        try:
            # Register the Japanese font
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
        except Exception as e:
            print(f"Warning: Could not register PDF fonts: {str(e)}")

    def _create_new_session(self, system_prompt: str = "", model: str = "gpt-4o") -> ChatSession:
        return ChatSession(
            id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            messages=[],
            system_prompt=system_prompt,
            model=model,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            context_summary=None,
            context_messages=[]
        )

    def new_chat(self, system_prompt: str, model: str) -> None:
        if self.current_session.messages:
            self.history.append(self.current_session)
            if len(self.history) > Config.MAX_HISTORY_CHATS:
                self.history.pop(0)
        self.current_session = self._create_new_session(system_prompt, model)

    def add_message(self, role: str, content: str) -> None:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.current_session.messages.append(message)
        self.current_session.context_messages.append(message)

        # Keep only the most recent context window messages
        if len(self.current_session.context_messages) > Config.CONTEXT_WINDOW_MESSAGES:
            self.current_session.context_messages.pop(0)

    def get_messages(self, include_system: bool = True) -> List[Dict[str, str]]:
        messages = []
        if include_system and self.current_session.system_prompt:
            messages.append({
                "role": "system",
                "content": self.current_session.system_prompt
            })

        # Add context summary if available
        if self.current_session.context_summary:
            messages.append({
                "role": "system",
                "content": f"Previous conversation context: {self.current_session.context_summary}"
            })

        # Add recent context messages
        messages.extend(self.current_session.context_messages)
        return messages

    def update_context_summary(self, summary: str) -> None:
        """Update the conversation context summary."""
        self.current_session.context_summary = summary

    def load_chat(self, session_id: str) -> bool:
        for session in self.history:
            if session.id == session_id:
                self.current_session = session
                return True
        return False

    def clear_current_chat(self) -> None:
        self.current_session = self._create_new_session(
            self.current_session.system_prompt,
            self.current_session.model
        )

    def export_chat_markdown(self) -> str:
        """Export current chat session as Markdown format."""
        md_content = []

        # Add header
        md_content.append(f"# Chat Session - {self.current_session.created_at}\n")
        md_content.append(f"Model: {self.current_session.model}\n")

        # Add system prompt if exists
        if self.current_session.system_prompt:
            md_content.append("## System Prompt\n")
            md_content.append(f"{self.current_session.system_prompt}\n")

        # Add context summary if exists
        if self.current_session.context_summary:
            md_content.append("## Context Summary\n")
            md_content.append(f"{self.current_session.context_summary}\n")

        # Add messages
        md_content.append("## Messages\n")
        for msg in self.current_session.messages:
            role = msg["role"].title()
            content = msg["content"].replace("\n", "\n  ")
            timestamp = msg.get("timestamp", "")
            md_content.append(f"### {role} ({timestamp})\n{content}\n")

        return "\n".join(md_content)

    def save_markdown_file(self) -> str:
        """Save current chat session as Markdown file and return the filename."""
        try:
            filename = f"chat_export_{self.current_session.id}.md"
            content = self.export_chat_markdown()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return filename
        except Exception as e:
            raise Exception(f"Failed to save markdown file: {str(e)}")

    def export_chat_pdf(self) -> str:
        """Export current chat session as PDF format."""
        try:
            filename = f"chat_export_{self.current_session.id}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()

            # Create custom styles with Japanese font support
            styles.add(ParagraphStyle(
                name='JapaneseText',
                parent=styles['Normal'],
                fontName='HeiseiMin-W3',
                fontSize=10,
                leading=14
            ))
            styles.add(ParagraphStyle(
                name='JapaneseHeading',
                parent=styles['Heading1'],
                fontName='HeiseiKakuGo-W5',
                fontSize=16,
                leading=20
            ))

            story = []

            # Add header
            story.append(Paragraph(f"Chat Session - {self.current_session.created_at}", styles['JapaneseHeading']))
            story.append(Paragraph(f"Model: {self.current_session.model}", styles['JapaneseText']))
            story.append(Spacer(1, 12))

            # Add system prompt if exists
            if self.current_session.system_prompt:
                story.append(Paragraph("System Prompt", styles['JapaneseHeading']))
                story.append(Paragraph(self.current_session.system_prompt, styles['JapaneseText']))
                story.append(Spacer(1, 12))

            # Add context summary if exists
            if self.current_session.context_summary:
                story.append(Paragraph("Context Summary", styles['JapaneseHeading']))
                story.append(Paragraph(self.current_session.context_summary, styles['JapaneseText']))
                story.append(Spacer(1, 12))

            # Add messages
            story.append(Paragraph("Messages", styles['JapaneseHeading']))
            for msg in self.current_session.messages:
                role = msg["role"].title()
                content = msg["content"]
                timestamp = msg.get("timestamp", "")

                story.append(Paragraph(f"{role} ({timestamp})", styles['JapaneseHeading']))
                story.append(Paragraph(content, styles['JapaneseText']))
                story.append(Spacer(1, 12))

            doc.build(story)
            return filename

        except Exception as e:
            raise Exception(f"Failed to save PDF file: {str(e)}")