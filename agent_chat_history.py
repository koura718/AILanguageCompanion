from datetime import datetime

def save_agent_chat_history(history):
    filename = f"agent_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Agent Chat History\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for entry in history:
                if "User:" in entry:
                    f.write(f"## User\n{entry.replace('User:', '').strip()}\n\n")
                elif "Editor:" in entry:
                    f.write(f"## Agent\n{entry.replace('Editor:', '').strip()}\n\n")
                    
        return filename
    except Exception as e:
        raise Exception(f"Failed to save agent chat history: {str(e)}")

# Extract chat history from the provided history
history = """
User: 最初のチャットで「モデルの切り替えに失敗しました」エラーです。改善してください
Editor: モデルの切り替えエラーの問題を改善します。

User: アプリケーションを停止してください。そして次の指示迄待機していてください
Editor: アプリケーションを停止します。
アプリケーションを停止し、次の指示をお待ちしています。

User: 開始から今までのチャット履歴をマークダウン形式でテキストファイルに保存してください
Editor: チャット履歴をマークダウン形式で保存するプログラムを実行します。
チャット履歴が正常にマークダウンファイルとして保存されました。直近のチャット履歴は `chat_export_20241224_032241.md` に保存されています。

User: 次の指示まで待機してください
この Agent と 僕の会話の履歴をマークダウン形式でテキストファイルに保存してください
"""

if __name__ == "__main__":
    try:
        saved_file = save_agent_chat_history(history.split('\n'))
        print(f"Chat history saved to: {saved_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
