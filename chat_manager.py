from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ChatSession:
    id: str
    messages: List[Dict[str, str]]
    system_prompt: str
    model: str
    created_at: str

class ChatManager:
    def __init__(self):
        self.current_session: ChatSession = self._create_new_session()
        self.history: List[ChatSession] = []

    def _create_new_session(self, system_prompt: str = "", model: str = "gpt-4o") -> ChatSession:
        return ChatSession(
            id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            messages=[],
            system_prompt=system_prompt,
            model=model,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def new_chat(self, system_prompt: str, model: str) -> None:
        if self.current_session.messages:
            self.history.append(self.current_session)
            if len(self.history) > 10:
                self.history.pop(0)
        self.current_session = self._create_new_session(system_prompt, model)

    def add_message(self, role: str, content: str) -> None:
        self.current_session.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self, include_system: bool = True) -> List[Dict[str, str]]:
        messages = []
        if include_system and self.current_session.system_prompt:
            messages.append({
                "role": "system",
                "content": self.current_session.system_prompt
            })
        messages.extend(self.current_session.messages)
        return messages

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

        # Add messages
        md_content.append("## Messages\n")
        for msg in self.current_session.messages:
            role = msg["role"].title()
            content = msg["content"].replace("\n", "\n  ")
            md_content.append(f"### {role}\n{content}\n")

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