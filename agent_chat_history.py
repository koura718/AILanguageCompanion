from datetime import datetime
import os
import pytz
from config import Config

def save_agent_chat_history(history):
    """Save agent chat history to a markdown file in the export directory."""
    try:
        # Create export directory if it doesn't exist
        os.makedirs("export", exist_ok=True)

        # Get current time in the configured timezone
        tz = pytz.timezone(Config.DEFAULT_TIMEZONE)
        current_time = datetime.now(tz)

        filename = f"export/agent_chat_{current_time.strftime('%Y%m%d_%H%M%S')}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("# エージェントチャット履歴\n\n")
            f.write(f"生成日時: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n")

            for entry in history:
                if "User:" in entry:
                    f.write(f"## ユーザー\n{entry.replace('User:', '').strip()}\n\n")
                elif "Editor:" in entry:
                    f.write(f"## エージェント\n{entry.replace('Editor:', '').strip()}\n\n")

        return filename
    except Exception as e:
        raise Exception(f"エージェントチャット履歴の保存に失敗しました: {str(e)}")

if __name__ == "__main__":
    # テスト用のチャット履歴
    history = """
    User: save_agent_chat_history の使い方を教えてください。
    Editor: はい、save_agent_chat_historyの使い方を説明します。このツールは会話履歴を保存するために使用します。

    User: 保存先はどこですか？
    Editor: exportディレクトリに保存されます。ディレクトリが存在しない場合は自動的に作成されます。
    """

    try:
        saved_file = save_agent_chat_history(history.split('\n'))
        print(f"チャット履歴を保存しました: {saved_file}")
    except Exception as e:
        print(f"エラー: {str(e)}")