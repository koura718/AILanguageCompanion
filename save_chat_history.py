from chat_manager import ChatManager
from datetime import datetime

def save_chat_history():
    chat_manager = ChatManager()
    filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    try:
        content = chat_manager.export_chat_markdown()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename
    except Exception as e:
        raise Exception(f"Failed to save chat history: {str(e)}")
